# -*- coding: utf-8 -*-
"""
Here I realized I can download data separaetly for each month/year

Study just the global counts (no "AIRPORT" and "LOCAL" information)
"""
#%%
from tak import reset; reset()

import tak as tw
import pandas as pd
import numpy as np
import seaborn.apionly as sns
import matplotlib.pyplot as plt
from pprint import pprint
import os
import time
import statsmodels.api as sm
import geocoder
os.getcwd()

from util import *
from util import load_data_1year,load_airport_idcode
#%%
#df = load_by_year_date('2015-02')
df = load_data_1year()

df_id = load_airport_idcode(df)

# create hash/lookup-tables mapping "Code" to City/State/Airport
# (for later convenience)
hash_city    = df_id.set_index('Code')['City'].to_dict()
hash_state   = df_id.set_index('Code')['State'].to_dict()
hash_airport = df_id.set_index('Code')['Airport'].to_dict()

#%% === study edges ===
# create a new column containing both the *origin* and the *destination* airport
df['Trips'] = tuple(zip(df['ORIGIN_AIRPORT_ID'], df['DEST_AIRPORT_ID']))
#%%
cnt_pairs = df['Trips'].value_counts()
cnt_pairs.head(10)

# replace code with city-name
cnt_pairs.index = cnt_pairs.index.map(lambda x: (hash_city[x[0]], hash_city[x[1]]))
cnt_pairs.head(10)
#%%

# check if round-trip
#tmp = cnt_pairs.index.map(lambda x: (min(x),max(x)))
#tmp = map(lambda x: (min(x),max(x)), cnt_pairs.index)
# (below the result from the "map" is converted to pd.Index to use the "duplicated" method)
_mask1 = pd.Index(cnt_pairs.index.map(lambda x: (min(x),max(x)))).duplicated(keep='first')
_mask2 = pd.Index(cnt_pairs.index.map(lambda x: (min(x),max(x)))).duplicated(keep='last')
_mask = _mask1 | _mask2

print "{:.3f}% has round-trips".format( 100*_mask.sum()/float( len(_mask) ) )

# keep only the round-trips
#cnt_pairs[mask].head()
cnt_pairs2 = cnt_pairs[_mask]
#%% take the smallest counts of the "round-trip"
_mask = pd.Index(cnt_pairs2.index.map(lambda x: (min(x),max(x)))).duplicated(keep='first')

# get trip in one direction (eg, "outbound" trip)
trip_out = cnt_pairs2.index[_mask]

cnt_pairs3 = pd.Series(0,index=trip_out)
#%%
# create named function to swap a tuple (makes code more legible IMO)
swap = lambda x: (x[1],x[0])

for i in cnt_pairs3.index:
    cnt_pairs3[i] = min(cnt_pairs2[i], cnt_pairs2[swap(i)])
#%% === well that was a lot of work...let's define a function to achieve this
#%% networkx plots?
import networkx as nx

#node_key = map(lambda x: x, df['ORIGIN_AIRPORT_ID'].append(df['DEST_AIRPORT_ID']).unique())
#node_val = map(lambda x: dict_city[x], df['ORIGIN_AIRPORT_ID'].append(df['DEST_AIRPORT_ID']).unique())
#nodes = dict(zip(node_key,node_val))

nodes = map(lambda x: dict_city[x], df['ORIGIN_AIRPORT_ID'].append(df['DEST_AIRPORT_ID']).unique())
G = nx.Graph()
G.add_nodes_from(nodes)


# created list of weighted-edge (3-element tuple with the 3rd value being the weight)
edges = map(lambda x:(x[0][0],x[0][1],{'weight':x[1]}), zip(cnt_pairs.index,cnt_pairs.values))

#G.add_edges_from(cnt_pairs_tops.index)
G.add_edges_from(edges)
#%%
tw.figure();nx.draw_networkx(G) # use spring layout
#%%
tw.figure()
#pos=nx.spring_layout(G)

df_lookup['latlon'] = zip(df_lookup['lat'],df_lookup['lon'])
pos = df_lookup.set_index('City')['latlon'].to_dict()

nx.draw_networkx_nodes(G,pos) # use spring layout
nx.draw_networkx_edges(G,pos) # use spring layout
#nx.draw_networkx_labels(G,pos) # use spring layout
#%%
#nx.write_gexf(G,'test.gexf')
#%% set node attributes at once
df_lookup['lon'].fillna(df_lookup['lon'].mean(),inplace=True)
df_lookup['lat'].fillna(df_lookup['lat'].mean(),inplace=True)
df_lookup.isnull().sum()
#%%
# http://stackoverflow.com/questions/22037360/keyerror-when-writing-numpy-values-to-gexf-with-networkx
# Warning: cannot write to gexf...element from pandas is in numpy.float64....fix it to float (see SO above)
tmp = df_lookup.set_index('City')['lat'].to_dict()
print type(tmp['Yuma'])

lat_dict = {key:float(val) for key,val in df_lookup.set_index('City')['lat'].to_dict().iteritems()}
lon_dict = {key:float(val) for key,val in df_lookup.set_index('City')['lon'].to_dict().iteritems()}
print type(lat_dict['Yuma'])
#%%
#http://stackoverflow.com/questions/13698352/storing-and-accessing-node-attributes-python-networkx
nx.set_node_attributes(G, 'lat', lat_dict)
nx.set_node_attributes(G, 'lon', lon_dict)
#nx.set_node_attributes(G, 'lat',df_lookup.set_index('City')['lat'].to_dict())
#nx.set_node_attributes(G, 'lon',df_lookup.set_index('City')['lon'].to_dict())
nx.set_node_attributes(G, 'airport',df_lookup.set_index('City')['Airline'].to_dict())
nx.set_node_attributes(G, 'state',df_lookup.set_index('City')['State'].to_dict())

nx.get_node_attributes(G,'state')
nx.write_gexf(G,'test2.gexf')
#%% --- get latitude longitude information ---
#t = time.time()
#_lat = []
#_lon = []
#for i,aaa in enumerate(df_lookup['Airline']):
#    if i%10==0: tw.print_time(t);print i
#    loc = geocoder.google(aaa)
#    if loc is not None:
#        _lon.append(loc.lng)
#        _lat.append(loc.lat)
#    else:
#        _lon.append(None)
#        _lat.append(None)
#
#df_lookup['lat'] = _lat
#df_lookup['lon'] = _lon
#df_lookup.to_csv('df_lookup_from_0106d.csv',index=False)
#%% apply newmans
import bct
A = np.array(nx.to_numpy_matrix(G))
A = (A > 500 )
tw.imtakk(A)
ci = bct.modularity_und(A)[0]
idx_sort = np.argsort(ci)

A_ = A[np.ix_(idx_sort,idx_sort)]
tw.imtakk(A_)