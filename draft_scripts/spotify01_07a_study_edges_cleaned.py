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
from util import load_data_1year,load_airport_idcode,print_time
#%%
#df = load_by_year_date('2015-02')
df = load_data_1year()

df_id = load_airport_idcode(df)

# create hash/lookup-tables mapping "Code" to City/State/Airport
# (for later convenience)
hash_city    = df_id.set_index('Code')['City'].to_dict()
hash_state   = df_id.set_index('Code')['State'].to_dict()
hash_airport = df_id.set_index('Code')['Airport'].to_dict()
#%% add lat/lon info
#t = time.time()
#_lat,_lon = [],[]
#for i,airport in enumerate(df_id['Airport']):
#    if i%20==0:
#        print '({:3} out of {})'.format(i,df_id.shape[0]),print_time(t)
#    loc = geocoder.google(airport)
#    if loc is not None:
#        _lon.append(loc.lng)
#        _lat.append(loc.lat)
#    else:
#        _lon.append(None)
#        _lat.append(None)
#
#df_id['lat'],df_id['lon'] = _lat,_lon
##%%
#df_null = df_id[ df_id.isnull().any(axis=1) ]
#for idx,city,state in zip(df_null.index,df_null['City'],df_null['State']):
#    loc = geocoder.google(city+' '+state)
#    if loc is not None:
#        df_id['lon'][idx] = loc.lng
#        df_id['lat'][idx] = loc.lat
##%% one more time
#df_null = df_id[ df_id.isnull().any(axis=1) ]
#for idx,city,state in zip(df_null.index,df_null['City'],df_null['State']):
#    loc = geocoder.google(city.split('/')[0]+' '+state)
#    if loc is not None:
#        df_id['lon'][idx] = loc.lng
#        df_id['lat'][idx] = loc.lat
#df_id['latlon'] = zip(df_id['lat'],df_id['lon'])
#df_id.to_csv('df_lookup_from_0107a.csv',index=False)
df_id = pd.read_csv('df_lookup_from_0107a.csv')
#%% === study edges ===
# create a new column containing both the *origin* and the *destination* airport
df['Trips'] = tuple(zip(df['ORIGIN_AIRPORT_ID'], df['DEST_AIRPORT_ID']))
#%%
trip_counts = df['Trips'].value_counts()
trip_counts.head(10)

"""
the trip "mirrors" each other....makes sense, as most flights tend to be round-trips,
unless you're moving out long-term or other rather rare circumstances

for this anaylsis, let's focus on "round-trips" by assuming ...
"""
# first drop *counts* not involved in two-way-trips
# (the min/max are applied to intentionally create *duplicate* entries, which 
#  allowing us to identify the trips that has both "outbound" and "return-bound" flights)
# (below the result from the "map" is converted to pd.Index to use the "duplicated" method)
_mask1 = pd.Index(trip_counts.index.map(lambda x: (min(x),max(x)))).duplicated(keep='first')
_mask2 = pd.Index(trip_counts.index.map(lambda x: (min(x),max(x)))).duplicated(keep='last')
_mask = _mask1 | _mask2

print "{:d} had only one-way trip ({:.3f}% from `trip_counts`))".format(
     (~_mask).sum(),100*(~_mask).sum()/float( len(_mask) ) )

# keep only round trips
trip_counts = trip_counts[_mask]
#%% === take the smallest counts of the "round-trip" ===
# get one of the direction in the round-trip to use as Index (say, an outbound flight)
_mask = pd.Index(trip_counts.index.map(lambda x: (min(x),max(x)))).duplicated(keep='first')

# create Series containing round-trip counts...which is an undirected graph
trip_counts_und = pd.Series(0,index = trip_counts.index[_mask],name='Counts')

# take the smaller of the trips to eliminate "one-way-flights"
swap = lambda x: (x[1],x[0])
for i in trip_counts_und.index:
    trip_counts_und[i] = min(trip_counts[i], trip_counts[swap(i)])
    
trip_counts_und.head()
#%% === well that was a lot of work...let's define a function to achieve this
from util import get_roundtrips
    
trip_counts = get_roundtrips( df['Trips'].value_counts() )

#% now let us analyze the trip counts
trip_counts.head(5)

# replace code with city-name for interpretation
trip_counts_ = trip_counts.copy()
trip_counts_.index = trip_counts.index.map(lambda x: (hash_city[x[0]], hash_city[x[1]]))

# check top-20
trip_counts_.head(20)

tw.figure()
trip_counts_[:50][::-1].plot(kind='barh')
plt.tight_layout()

"""
seems like many of the round-trip counts are influenced by "distance" and
city "population"...if time permits would like to run a quick
regression analysis to dig in a bit more on this...
"""
#%% networkx plots
import networkx as nx

# replace code with city-name for interpretation
trip_counts_ = trip_counts.copy()
trip_counts_.index = trip_counts.index.map(lambda x: (hash_airport[x[0]], hash_airport[x[1]]))

nodes = df_id['Airport'].tolist()
pprint(nodes[:5])
G = nx.Graph()
G.add_nodes_from(nodes)
print len(G)
# --- next add edges ---
# created list of weighted-edge (3-element tuple with the 3rd value being the weight)
edges = map(lambda x:(x[0][0],x[0][1],{'weight':x[1]}), zip(trip_counts_.index,trip_counts_.values))
pprint(edges[:5])
G.add_edges_from(edges)

print len(G)
#%%
# --- also add lat/lon information to the node attributes ---
# create dictionary (dict-comprehension used to convert numpy.float64 to float...
# see http://stackoverflow.com/questions/22037360/keyerror-when-writing-numpy-values-to-gexf-with-networkx for why
lat_dict = {key:float(val) for key,val in df_id.set_index('Airport')['lat'].to_dict().iteritems()}
lon_dict = {key:float(val) for key,val in df_id.set_index('Airport')['lon'].to_dict().iteritems()}

nx.set_node_attributes(G, 'lat', lat_dict)
nx.set_node_attributes(G, 'lon', lon_dict)

nx.set_node_attributes(G, 'city',df_id.set_index('Airport')['City'].to_dict())
nx.set_node_attributes(G, 'state',df_id.set_index('Airport')['State'].to_dict())
#%%
tw.figure();nx.draw_networkx(G) 
#%%
#%%
#tw.figure()
#pos=nx.spring_layout(G)

#nx.draw_networkx_nodes(G,pos) # use spring layout
#nx.draw_networkx_edges(G,pos) # use spring layout
#nx.draw_networkx_labels(G,pos) # use spring layout
#%%
nx.write_gexf(G,'test_0107.gexf')
#%% set node attributes at once
#%% apply newmans
#import bct
#A = np.array(nx.to_numpy_matrix(G))
#A = A!=0
#ci = bct.modularity_und(A)[0]
#idx_sort = np.argsort(ci)
#
#A_ = A[np.ix_(idx_sort,idx_sort)]
#tw.imtakk(A_)
#
##%%
#tw.figure();nx.draw_networkx(G,node_color=ci) 