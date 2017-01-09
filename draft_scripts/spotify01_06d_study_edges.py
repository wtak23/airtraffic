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
#%%
#df = load_by_year_date('2015-02')
df = load_all_data()
cols = df.columns.tolist()
pprint(cols)
#%% any interesting patterns among Quarter? Month? Day of Month? Day of Week?
df_air = load_airports()
#%%
col = 'Description'
myhash = get_hash(df,col)['air_id']
df_lookup = pd.DataFrame(myhash.values(),columns=[col])
df_lookup[['City','State','Airline']] = pd.DataFrame(df_lookup[col].str.split(r'(,\s|:\s)').tolist()).iloc[:,[0,2,4]]
#%%
dict_city,dict_state,dict_airline,descr_lookup = get_lookup_tables(df)

df['EDGES'] = tuple(zip(df['ORIGIN_AIRPORT_ID'], df['DEST_AIRPORT_ID']))
#%%
cnt_pairs = df['EDGES'].value_counts()


# --- remove round-trips --- 
#cnt_pairs = cnt_pairs.reset_index()
#cnt_pairs.columns = ['index_orig','counts']
#cnt_pairs['index_sorted'] = cnt_pairs['index_orig'].map(lambda x: (min(x),max(x)))
mask = pd.Index(cnt_pairs.index.map(lambda x: (min(x),max(x)))).duplicated(keep='first')
cnt_pairs = cnt_pairs[mask]

# --- replace code with city-name
cnt_pairs.index = cnt_pairs.index.map(lambda x: (dict_city[x[0]], dict_city[x[1]]))

# take top 50
cnt_pairs_top= cnt_pairs[:50]
#cnt_pairs= cnt_pairs[:200]
#tw.figure();cnt_pairs_top.plot(kind='barh')
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
df_lookup = pd.read_csv('df_lookup_from_0106d.csv')
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