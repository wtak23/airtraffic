import numpy as np
import pandas as pd
import seaborn.apionly as sns

# libraries for network analysis
import networkx as nx
import bct

from geopy.distance import vincenty

import util

def make_trip_counts(df_data, df_lookup=None):
    if df_lookup is None:
        df_lookup = pd.read_csv('df_lookup.csv')
    
    # create table of "trip_counts" (sorted by most frequent trips)
    trip_counts = df_data['Trips'].value_counts().to_frame('counts')
    
    # create two columns for the pair of nodes forming the edge
    trip_counts['code1'] = trip_counts.index.map(lambda x: x[0])
    trip_counts['code2'] = trip_counts.index.map(lambda x: x[1])
    
    trip_counts.reset_index(drop=True,inplace=True)
    
    # create columns with corresponding airport information
    columns = [u'Airport', u'City',u'State']
    
    for col in columns:
        # create hash-table for ID lookup
        hash_table = df_lookup.set_index('Code')[col].to_dict()
        
        trip_counts[col + '1'] = trip_counts['code1'].map(lambda code: hash_table[code])
        trip_counts[col + '2'] = trip_counts['code2'].map(lambda code: hash_table[code])
        
    # reorder columns (just personal preference)
    cols = trip_counts.columns.tolist()
    cols = [cols[0]] + cols[3:9] + cols[1:3]
    trip_counts = trip_counts[cols]
    
    # add distance associated with each trips (ie, distance between aiports)
    # see https://en.wikipedia.org/wiki/Vincenty's_formulae
    hash_lat = df_lookup.set_index('Code')['lat'].to_dict()
    hash_lon = df_lookup.set_index('Code')['lon'].to_dict()
    dist_ = []
    for code1,code2 in zip(trip_counts['code1'],trip_counts['code2']):
        coord1 = hash_lat[code1],hash_lon[code1]
        coord2 = hash_lat[code2],hash_lon[code2]
        dist_.append(vincenty(coord1,coord2).kilometers)
        
    trip_counts['distance'] = dist_
    return trip_counts
    
#%% === data tidying: routes ===
def make_route_counts(trip_counts):
    """ Convert to undirected graph
    """
    tmp = pd.Series(map(lambda pair: (min(pair), max(pair) ), 
                         zip(trip_counts['code1'],trip_counts['code2'])))
    
    # detect flights A->B and A<-B (flights sharing same pair of airport)
    mask_AB = tmp.duplicated(keep='first') # edges A -> B
    mask_BA = tmp.duplicated(keep='last')  # edges B -> A
    mask_    = ~(mask_AB|mask_BA)         # some trips only have one direction
    
    assert mask_AB.sum() == mask_BA.sum() 
    assert trip_counts.shape[0] == (mask_AB.sum() + mask_BA.sum() + mask_.sum())
    
    trips_AB = trip_counts[mask_AB]
    trips_BA = trip_counts[mask_BA]
    trip_neither = trip_counts[ ~(mask_AB|mask_BA)]
    
    trips_AB = trip_counts[mask_AB]
    trips_BA = trip_counts[mask_BA]
    trip_neither = trip_counts[ ~(mask_AB|mask_BA)]
    
    # this will serve as our final undirected graph
    trip_counts_und = trips_AB.copy()
    
    # to identify matching rows, swap code1,code2
    trips_BA = trips_BA.rename(columns={'code1':'code2','code2':'code1'})[['counts','code1','code2']]
    
    # now we can use the code pairs as merge-keys
    trip_counts_und = trips_AB.merge(trips_BA, on=['code1','code2'],suffixes=['','_'])
    
    # now we can sum both directions of the edge to create our undirected graph :)
    trip_counts_und['counts'] = trip_counts_und['counts'] + trip_counts_und['counts_']
    del trip_counts_und['counts_']
    
    # to complete, append the trips that only had one-way direction, and re-sort!
    route_counts = trip_counts_und.append(trip_neither).\
                          sort_values('counts',ascending=False).\
                          reset_index(drop=True)
                          
    return route_counts

def make_hash_tables(df_lookup):
    hash_tables = {}
    for col in df_lookup.columns:
        if col == 'Code':
            continue
        elif col in ['lat','lon']:
            """
            Warning: Pandas returns data type in numpy.float64 for floats,
            which is not supported in networkx.write_gexf. So typecast to float
            http://stackoverflow.com/questions/22037360/keyerror-when-writing-numpy-values-to-gexf-with-networkx
            """
            tmp_dict = df_lookup.set_index('Code')[col].to_dict()
            hash_tables[col] = {key:float(val) for key,val in tmp_dict.iteritems()}
        else:
            hash_tables[col] = df_lookup.set_index('Code')[col].to_dict()

    return hash_tables


def make_nx_graph(counts,df_lookup,digraph=False):
    """
    
    Parameters
    ----------
    counts : pandas.DataFrame
        Table containing the trip_counts (digraph) or route_counts (undirected graph)
        Use in network analysis scripts
    df_lookup : pandas.DataFrame
        Table 
    digraph : bool
        Is the graph directed? (default = False, so undirected)
    """
    if digraph:
        G = nx.DiGraph() # directed graph
    else: 
        G = nx.Graph()   # undirected graph

    # === provide node information === #
    # get unique set of nodes in the graph
    nodes = set(counts['code1'].unique().tolist() +
                counts['code2'].unique().tolist())
                
    G.add_nodes_from(nodes)
    
    # --- add airport name as node attribute (handy for analysis in Gephi) ---
    # --- to do this, need to pass a dictionary to networkx 
    hash_airport   = df_lookup.set_index('Code')['Airport'].to_dict()

    # filter away airport in the lookup-table not in the graph
    nodes_airport = {key:val for key,val in hash_airport.iteritems() if key in nodes}
    nx.set_node_attributes(G, 'airport', nodes_airport)
    
    # --- add airport latitude/longitude information --- 
    hash_lat       = df_lookup.set_index('Code')['lat'].to_dict()
    hash_lon       = df_lookup.set_index('Code')['lon'].to_dict()
    
    """ Warning (why the typecasting below is important)
    Pandas returns data type in numpy.float64 for floats, which is not 
    supported in ``networkx.write_gexf`` (learned this the hard way...)
    
    http://stackoverflow.com/questions/22037360/keyerror-when-writing-numpy-values-to-gexf-with-networkx
    """
    # apply filering with typecasting from numpy.float64 to float
    nodes_lat = {key:float(val) for key,val in hash_lat.iteritems() if key in nodes}
    nodes_lon = {key:float(val) for key,val in hash_lon.iteritems() if key in nodes}
    nx.set_node_attributes(G, 'lat', nodes_lat)
    nx.set_node_attributes(G, 'lon', nodes_lon)
    

    # === add weighted edge information (flight counts in our context) === #
    # to define edge, supply a 3-tuple of ``(node1,node2,dict(weight=edge))``
    edges = map(lambda x:(x[0],x[1], dict(weight=x[2])), 
                zip(counts['code1'], counts['code2'], counts['counts']))
    G.add_edges_from(edges)
    
    # === done! ready to return, except one more step! === 
    # instead of using the Airport_ID as the node-labels, let's instead use the
    # City+State information, which is unique so can be used as lookup-keys
    hash_citystate = df_lookup.set_index('Code')['City_State'].to_dict()
    nodes_citystate = {key:val for key,val in hash_citystate.iteritems() if key in nodes}
    G = nx.relabel_nodes(G,nodes_citystate)
    return G
    
def compute_network_measures(G,add_module_attr = True):
    
    A = np.array(nx.to_numpy_matrix(G))
    
    degree_wei = A.sum(axis=0,dtype=int) # weighted degree 
    degree_bin = (A!=0).sum(axis=0)      # binary degree
    
    # community detection -> compute modularity groups
    module = bct.modularity_louvain_und(bct.normalize(A),seed=0)[0]
    
    # convert numpy array into dictionary with node-label
    degree_wei = {node:deg for node,deg in zip(G.nodes(), degree_wei)}
    degree_bin = {node:deg for node,deg in zip(G.nodes(), degree_bin)}
    module = {node:int(modu) for node,modu in zip(G.nodes(), module)}
    
    if add_module_attr:
        # add community label as node attributes 
        # (handy when exporting .gexf file)
        nx.set_node_attributes(G, 'modu', module)
    
    # nodal centrality measures
    pagerank = nx.pagerank(G)               # google page-rank
    eig_cent = nx.eigenvector_centrality(G) # eigenvalue centrality
    bet_cent = nx.betweenness_centrality(G) # betweennes centrality
    
    # create dictionary of each of the measures computed above
    # (to be convertd to dataframe at end)
    df_network = dict(pagerank=pagerank,
                      eig_cent=eig_cent,
                      bet_cent=bet_cent,
                      degree_wei=degree_wei,
                      degree_bin=degree_bin,
                      module=module)
                      
    if not isinstance(G, nx.classes.digraph.DiGraph):
        # clustering coefficient (tendency of a node to cluster together)
        # (not implemented for digraphs)
        clust_coef = nx.clustering(G,weight=G)
        df_network.update(dict(clust_coef=clust_coef))
    
    # all set! convert dict to dataframe and return :)
    return pd.DataFrame(df_network)

if __name__ == '__main__':
    df_data   = util.load_airport_data()
    df_lookup = pd.read_csv('df_lookup.csv') 
    
    # create a new column containing the *origin* and the *destination* airport
    # (these will form the network "edges" in our graph, with airport being the nodes)
    df_data['Trips'] = tuple(zip(df_data['ORIGIN_AIRPORT_ID'], df_data['DEST_AIRPORT_ID']))
    
    # directed graph of flight counts 
    trip_counts = make_trip_counts(df_data)
    
    # undirected graph of flight counts (see jupyter notebook for details)
    route_counts = make_route_counts(trip_counts)
    
    # ===  undirected graph analysis ===
    # --- create networkx object ---
    # assert uniqueness of City_State info
    assert len(df_lookup['City_State'].unique()) == len(df_lookup['City_State'])
    
    G = make_nx_graph(route_counts, df_lookup, digraph=False)

    # compute key network measures
    df_network = compute_network_measures(G)
    
    # export .gexf file for later analysis in gephi
    nx.write_gexf(G,'airtraffic_network.gexf')
    
    # === directed graph ===
    D = make_nx_graph(trip_counts, df_lookup, digraph=True)
    df_network_dir = compute_network_measures(D)
    nx.write_gexf(D,'test_digraph.gexf')
