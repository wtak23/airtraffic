# -*- coding: utf-8 -*-
"""
Same as first part, but instead of 2015-2016, do 2014-2015
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
from util import (load_data_1year,load_airport_idcode,print_time,
                  load_airport_idcode_shortcut,make_networkx_graph)
#%%
#df = load_by_year_date('2015-02')
df = load_data_1year2014_2015()
#df = load_data_1year()

#df_id = load_airport_idcode(df)
df_id = load_airport_idcode_shortcut()

# create hash/lookup-tables mapping "Code" to City/State/Airport
# (for later convenience)
hash_city    = df_id.set_index('Code')['City'].to_dict()
hash_state   = df_id.set_index('Code')['State'].to_dict()
hash_airport = df_id.set_index('Code')['Airport'].to_dict()
hash_citystate= df_id.set_index('Code')['City_State'].to_dict()
hash_lat = df_id.set_index('Code')['lat'].to_dict()
hash_lon = df_id.set_index('Code')['lon'].to_dict()
#%% === study edges ===
# create a new column containing both the *origin* and the *destination* airport
df['Trips'] = tuple(zip(df['ORIGIN_AIRPORT_ID'], df['DEST_AIRPORT_ID']))
trip_counts = df['Trips'].value_counts()

trip_counts = get_roundtrips(trip_counts)
#trip_counts_.index = trip_counts_.index.map(lambda x: (hash_citystate[x[0]], hash_citystate[x[1]]))
#%%
from geopy.distance import vincenty
trip_dist = {code: [] for code in trip_counts.index}
for code1,code2 in trip_counts.index:
    coord1 = hash_lat[code1],hash_lon[code1]
    coord2 = hash_lat[code2],hash_lon[code2]
    trip_dist[code1,code2] = vincenty(coord1,coord2).kilometers

trip_dist = pd.Series(trip_dist)
trip_info = pd.DataFrame(trip_counts)
trip_info['distance'] = trip_dist

trip_info.index   = trip_counts.index.map(lambda x: (hash_citystate[x[0]], hash_citystate[x[1]]))
#%% create distance matrix (this will be a full dense matrix, so apply brute force loop)
n_nodes = df_id.shape[0]
distmat = np.zeros( (n_nodes,n_nodes) )
distvec = np.zeros( n_nodes*(n_nodes-1)/2)
distvec_ind = []
codes = df_id['Code'].tolist()

cnt = 0
for i in range(n_nodes):
    code1 = codes[i]
    coord1 = hash_lat[code1],hash_lon[code1]
    for j in range(i+1,n_nodes):
        code2 = codes[j]
        coord2 = hash_lat[code2],hash_lon[code2]
        distmat[i,j] = vincenty(coord1,coord2).kilometers
        distmat[j,i] = distmat[i,j]
        distvec[cnt] = distmat[i,j]
        distvec_ind.append( (code1,code2) )
        cnt += 1
        
distmat = pd.DataFrame(distmat, index=codes,columns=codes)
distmat.index   = distmat.index.map(lambda x: hash_citystate[x])
distmat.columns = distmat.index

distvec = pd.Series(distvec, index=distvec_ind)
distvec.name = 'distance'
distvec.index   = distvec.index.map(lambda x: (hash_citystate[x[0]], hash_citystate[x[1]]))
#%% create networkx object
#%%
#tw.figure('f')
#sns.heatmap(distmat, square=True,vmax=5000)#, cmap=plt.cm.hot)
#plt.yticks(rotation=0,fontsize=4) 
#plt.xticks(rotation=90)
#plt.tight_layout()
#%%
import networkx as nx
#%% === create physical distance graph ===
#%%
G = make_networkx_graph(trip_counts,df_id)
D = make_networkx_graph(distvec,df_id,apply_hash=False)
#nx.write_gexf(D,'dist.gexf')
df_D=pd.DataFrame(np.array(nx.to_numpy_matrix(D)), index=D.nodes(),columns=D.nodes())
df_G=pd.DataFrame(np.array(nx.to_numpy_matrix(G)), index=G.nodes(),columns=G.nodes())
#print list(nx.isolates(G))
#G.remove_nodes_from(nx.isolates(G))
#
#A = np.array(nx.to_numpy_matrix(G))
#deg = pd.Series(A.sum(axis=0).astype(int),index=list(G.nodes())).sort_index()
#G.remove_nodes_from(deg[deg < 5000].index.tolist())
#print len(G)
#%%
#G.remove_nodes_from(['Atlanta (GA)', "Chicago (IL) [O'Hare]"])

#nx.fiedler_vector(G)
print nx.algebraic_connectivity(G)

nodes = list(G.nodes())

pagerank = nx.pagerank(G)
deg_cent = nx.degree_centrality(G)
#nx.degree_assortativity_coefficient(G)
eig_cent = nx.eigenvector_centrality(G)
bet_cent = nx.betweenness_centrality(G)
clust_coef = nx.clustering(G,weight=G.we)

A = np.array(nx.to_numpy_matrix(G))
deg = pd.Series(A.sum(axis=0).astype(int),index=nodes).sort_index()

df_cent = pd.DataFrame([pagerank,deg,deg_cent,eig_cent,bet_cent,clust_coef],
                       index=['pagerank','degree','degcent','eig','bet','cc']).T
                       
sns.pairplot(df_cent)
plt.tight_layout()
#%%
import bct
A = np.array(nx.to_numpy_matrix(G))
deg = A.sum(axis=0)
An = bct.normalize(A)
D = bct.distance_wei(An)[0]

a1 = bct.clustering_coef_wu(An)
a2 = bct.betweenness_wei(An)
a3 = bct.eigenvector_centrality_und(An)
a4 = bct.pagerank_centrality(An,0.85)
a5 = bct.efficiency_wei(An,local=True)
df_bct = pd.DataFrame([a1,a2,a3,a4,a5,deg],columns=list(G.nodes()),
                      index=['cc','bc','ec','pr','ef','deg']).T

cpl,eff = bct.charpath(D)[0:2]
bct.efficiency_wei(An)
bct.modularity_louvain_und(An,seed=0)
bct.transitivity_wu(An)
#%%
sns.pairplot(df_bct)
tw.fig_get_geom('f')
plt.tight_layout()
#%%
An = bct.normalize(distmat.values)
eff = bct.efficiency_wei(An,local=True)
eff_ = pd.Series(eff,index=distmat.index)
#%% === study by regions ===
import json
with open('./data/us_states_regions.json','r') as f:
    regions = json.load(f)

us_state_abbrev = state_abbrev_dict()

for state in regions:
    regions[state] = map(lambda key: us_state_abbrev[key], regions[state])

df_region = []
for key in regions:
    _dftmp = pd.DataFrame( regions[key], columns=['State']  )
    _dftmp['Region'] = key
    df_region.append(_dftmp)

df_region = pd.concat(df_region,ignore_index=True)
        
df_id = df_id.merge(df_region,on='State',how='left')
#%%
regions = ['Northeast', 'South', 'West', 'Midwest']
nx.write_gexf(G,'graph_full_2014_2015.gexf')
#G_regions = {region:[] for region in regions}
#for region in regions:
#    GG = G.copy()
#    nodes_to_delete = df_id[df_id['Region'] != region ]['City_State'].tolist()
#    GG.remove_nodes_from(nodes_to_delete)
#    G_regions[region] = GG
#    print len(G_regions[region])
##    nx.write_gexf(GG,'graph_{}.gexf'.format(region))