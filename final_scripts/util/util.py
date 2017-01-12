import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn.apionly as sns
import time
import bct
import networkx as nx

#%% === set plotting options ====
def sns_figure(style='darkgrid',**kwargs):
    """ Create new figure in seaborn with temporary style change
    
    A simple convenience function used to temporarily change figure style
    using seaborn (``'darkgrid'`` is my favorite style)
    
    Usage:
    
    >>> sns_figure("darkgrid")
    >>> plt.plot(np.random.randn(100,3))
    
    See http://seaborn.pydata.org/tutorial/aesthetics.html#temporarily-setting-figure-style
    
    Parameters
    ----------
    style : string
        One of the five preset styles in seaborn: 'darkgrid', 'whitegrid', 
        'dark', 'white', and 'ticks'
    **kwargs : dict
        Keyword arguments passed to ``pyplot.figure``
    """
    with sns.axes_style(style):
        plt.figure(**kwargs)
        plt.plot()

def sns_subplots(nrows,ncols,style='darkgrid',ravel=True,**kwargs):
    """ Create subplots in seaborn with temporary style change
    
    Used to temporaritly change figure style in seaborn
    
    ``**kwargs`` take arguments to :func:`plt.subplots`
    
    Usage:
    
    >>> fig,axes = sns_subplots(nrows=2,ncols=3,style='darkgrid',figsize=(16,8))
    >>> for ax in axes:
    >>>     ax.plot(np.random.randn(100))
    
    Parameters
    ----------
    nrows : int
        Number of rows to include in the subplot
    ncols : int
        Number of columns to include in the subplot
    style : string
        One of the five preset styles in seaborn: 'darkgrid', 'whitegrid', 
        'dark', 'white', and 'ticks'
    **kwargs : dict
        Keyword arguments passed to ``pyplot.subplots``
        
    Returns
    -------
    fig : plt.figure object
        ``plt.figure object``
    axes : plt.axes list-array
        ``plt.axes list-array``
    """
    from seaborn import axes_style
    with axes_style(style):
        fig,axes = plt.subplots(nrows,ncols,**kwargs)
    
    if ravel:
        # this way, i don't have to use 2-d indexing when individual axes
        axes = axes.ravel()
    return fig,axes
    
def sns_set_colorpalette():
    """ Set seaborn plotting  to my preferred style """
    tmp = sns.color_palette("muted")
    
    # swap red and green
    tmp[1],tmp[2] = tmp[2],tmp[1]
    
    sns.set_palette(tmp)
    
#%% === data loader ====
def load_airport_data(verbose=True):
    """ Load one year worth of airport traffic data (2015-11 to 2016-10) """
    df = None
    
    # create list of files.
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    # columns to read from zipped spreadsheet
    usecols = ['YEAR','QUARTER','MONTH','DAY_OF_MONTH','DAY_OF_WEEK',
               'ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID']
               
    df = None
    for filename in full_files:
        if verbose: print ' ... load dataframe from {} '.format(filename)
        if df is None:
            df = pd.read_csv('../data/'+filename,usecols=usecols)
        else:
            df = df.append(pd.read_csv('../data/'+filename,usecols=usecols))

    return df
    
def load_airport_data_3years(verbose=True):
    """ Load 3 years worth of airport traffic data (2013-11 to 2016-10) """
    # create list of files.
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2013-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2014-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    # columns to read from zipped spreadsheet
    usecols = ['YEAR','QUARTER','MONTH','DAY_OF_MONTH','DAY_OF_WEEK',
               'ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID']
               
    df = None
    for filename in full_files:
        if verbose: print ' ... load dataframe from {} '.format(filename)
        if df is None:
            df = pd.read_csv('../data/'+filename,usecols=usecols)
        else:
            df = df.append(pd.read_csv('../data/'+filename,usecols=usecols))

    return df
    
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
#%% === network analysis routine ===
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
#%% === other utility functions ===
def print_time(t):
    """ Return string indicating times elapsed wrt a time.time() instance

    Usage: 
    
    >>> import time
    >>> t = time.time()
    >>> time.sleep(2.5)
    >>> print_time(t)
    'Elapsed time:  2.50 seconds'
    
    Parameters
    ----------
    t : time object
        Instance of the time.time() object
        
    Returns
    -------
    time_str : string
        String with elapsed time
    """
    return "Elapsed time: {:>5.2f} seconds".format(time.time()-t)
#%%
def hash_state_to_abbrev():
    """ Return a hash-table mapping state name to its abbreviation.
    
    Credit: https://gist.github.com/rogerallen/1583593
    """
    return {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }
#%%
if __name__ == '__main__':
    df_data = load_airport_data()