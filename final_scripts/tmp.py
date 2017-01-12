from tak import reset; reset()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn.apionly as sns

# libraries for network analysis
import networkx as nx
import bct

from geopy.distance import vincenty

import util
#%% === study edges ===
def get_main_data():
    df_data = util.load_airport_data()
    
    # make the "day_of_week" explicit
    hash_dayofweek = {1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'}
    df_data['DAY_OF_WEEK'] = df_data['DAY_OF_WEEK'].map(lambda key: hash_dayofweek[key])
    return df_data
#%% === data tidying: trips ===
def make_trip_counts():
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
    dist_ = []
    for code1,code2 in zip(trip_counts['code1'],trip_counts['code2']):
        coord1 = hash_lat[code1],hash_lon[code1]
        coord2 = hash_lat[code2],hash_lon[code2]
        dist_.append(vincenty(coord1,coord2).kilometers)
        
    trip_counts['distance'] = dist_
    return trip_counts
#%% === data tidying: routes ===
def make_route_counts(trip_counts=None):
    if trip_counts is None:
        trip_counts = make_trip_counts()
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
#%%
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
    
def make_nx_graph():
    pass
#%% === main ===
#if __name__ == '__main__':
df_data = get_main_data()
df_lookup = pd.read_csv('df_lookup.csv') # lookup table for the AIRPORT_ID above

# create a new column containing the *origin* and the *destination* airport
# (these will form the network "edges" in our graph, with airport being the nodes)
df_data['Trips'] = tuple(zip(df_data['ORIGIN_AIRPORT_ID'], df_data['DEST_AIRPORT_ID']))

# create hash-tables for later convenience (with map/appy functions)
# (maps Airport "ID_Code" to other quantities of interest)
hash_airport   = df_lookup.set_index('Code')['Airport'].to_dict()
hash_citystate = df_lookup.set_index('Code')['City_State'].to_dict()
hash_lat       = df_lookup.set_index('Code')['lat'].to_dict()
hash_lon       = df_lookup.set_index('Code')['lon'].to_dict()
hash_region    = df_lookup.set_index('Region')['lon'].to_dict()

trip_counts = make_trip_counts()
route_counts = make_route_counts()
#%% === create networkx objetc ===
# nodes must be unique... use City_State info

len(df_lookup['City_State'].unique()) == len(df_lookup['City_State'])

nodes = set(route_counts['code1'].unique().tolist() +
            route_counts['code2'].unique().tolist())

nodes_lat = {key:float(val) for key,val in hash_lat.iteritems() if key in nodes}
nodes_lon = {key:float(val) for key,val in hash_lon.iteritems() if key in nodes}
nodes_citystate = {key:val for key,val in hash_citystate.iteritems() if key in nodes}
nodes_region = {key:val for key,val in hash_region.iteritems() if key in nodes}

#nodes = df_lookup.Code 
#nodes_lat = {key:float(val) for key,val in hash_lat.iteritems()}
#nodes_lon = {key:float(val) for key,val in hash_lon.iteritems()}
#nodes_citystate = hash_citystate
G = nx.Graph()
G.add_nodes_from(nodes)

nx.set_node_attributes(G, 'lat', nodes_lat)
nx.set_node_attributes(G, 'lon', nodes_lon)
#nx.set_node_attributes(G, 'state',  nodes_citystate)
#%%
# to define edge, supply a 3-tuple of ``(node1,node2,dict(weight=edge))``
edges = map(lambda x:(x[0],x[1], dict(weight=x[2])), 
            zip(route_counts['code1'], route_counts['code2'], route_counts['counts']))

G.add_edges_from(edges)

G = nx.relabel_nodes(G,nodes_citystate)
#nx.write_gexf(G,'test.gexf')

#% compute measures
A = np.array(nx.to_numpy_matrix(G))

degree = A.sum(axis=0,dtype=int)
degree_bin = (A!=0).sum(axis=0)
module = bct.modularity_louvain_und(bct.normalize(A),seed=0)[0]

degree     = {node:deg for node,deg in zip(G.nodes(), degree)}
degree_bin = {node:deg for node,deg in zip(G.nodes(), degree_bin)}
module = {node:int(modu) for node,modu in zip(G.nodes(), module)}

pagerank = nx.pagerank(G)
deg_cent = nx.degree_centrality(G)
eig_cent = nx.eigenvector_centrality(G)
bet_cent = nx.betweenness_centrality(G)
clust_coef = nx.clustering(G,weight=G)

pd.DataFrame(dict(pagerank=pagerank))
df_cent = pd.DataFrame(dict(pagerank=pagerank,
                            eig_cent=eig_cent,
                            bet_cent=bet_cent,
                            clust_coef=clust_coef,
                            degree=degree,
                            degree_bin=degree_bin,
                            module=module,))
                       
#sns.pairplot(df_cent)
#plt.tight_layout()

G = G.copy()
nx.set_node_attributes(G, 'modu', module)

nx.write_gexf(G,'test2.gexf')
#%% === directed graph ===
D = nx.DiGraph()

nodes = set(trip_counts['code1'].unique().tolist() +
            trip_counts['code2'].unique().tolist())

D.add_nodes_from(nodes)

nodes_lat = {key:float(val) for key,val in hash_lat.iteritems() if key in nodes}
nodes_lon = {key:float(val) for key,val in hash_lon.iteritems() if key in nodes}
nx.set_node_attributes(D, 'lat', nodes_lat)
nx.set_node_attributes(D, 'lon', nodes_lon)

# to define edge, supply a 3-tuple of ``(node1,node2,dict(weight=edge))``
edges = map(lambda x:(x[0],x[1], dict(weight=x[2])), 
            zip(trip_counts['code1'], trip_counts['code2'], trip_counts['counts']))

D.add_edges_from(edges)


nodes_citystate = {key:val for key,val in hash_citystate.iteritems() if key in nodes}
D = nx.relabel_nodes(D,nodes_citystate)
nx.write_gexf(D,'test3.gexf')
#%%























