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
os.getcwd()

from util import *
#%%
#df = load_by_year_date('2015-02')
df = load_all_data()
cols = df.columns.tolist()
pprint(cols)
#%% any interesting patterns among Quarter? Month? Day of Month? Day of Week?
lookup_city,lookup_state,lookup_al,lookup_descr = get_lookup_tables(df)
#lookup_city_ = {key: lookup_city[key] for key in counts['ORIGIN_AIRPORT_ID']}
#df_air_id,df_seq_id,df_market = load_aux_data(df)
#%% ==== study overall counts ====
tw.purge()
#%
#tw.figure()
grpby = 'ORIGIN_CITY_MARKET_ID'
#grpby = 'DEST_AIRPORT_ID'
counts = pd.DataFrame(df.groupby(grpby).count().iloc[:,0])
counts.columns = ['COUNT']
#counts.plot()

counts.reset_index(inplace=True)
counts['STATE'] = counts[grpby].replace(lookup_state)
counts['CITY'] = counts[grpby].replace(lookup_city)
if 'MARKET' not in grpby:
    counts['AIRLINE'] = counts[grpby].replace(lookup_al)
    counts['DESCR'] = counts[grpby].replace(lookup_descr)
counts.set_index(grpby,inplace=True)

counts.groupby('STATE').sum().sort_values(by='COUNT',ascending=False)
counts.groupby('STATE').sum().sort_values(by='COUNT',ascending=False).plot(kind='barh',legend=False)
counts.groupby('CITY').sum().sort_values(by='COUNT',ascending=False)[:50].plot(kind='barh');plt.tight_layout()

if 'MARKET' not in grpby:
    counts.groupby('AIRLINE').sum().sort_values(by='COUNT',ascending=False)[:50].plot(kind='barh');plt.tight_layout()
    counts.groupby('DESCR').sum().sort_values(by='COUNT',ascending=False)[:50].plot(kind='barh');plt.tight_layout()
#%% === study counts by ... ====
counts2 = pd.DataFrame(df.groupby(['MONTH','ORIGIN_AIRPORT_ID']).count()).reset_index().iloc[:,:3]
counts2.columns = counts2.columns[:-1].tolist() + ['COUNT']

counts2['STATE'] = counts2['ORIGIN_AIRPORT_ID'].replace(lookup_state)
counts2['CITY'] = counts2['ORIGIN_AIRPORT_ID'].replace(lookup_city)
counts2['AIRLINE'] = counts2['ORIGIN_AIRPORT_ID'].replace(lookup_al)
counts2['DESCR'] = counts2['ORIGIN_AIRPORT_ID'].replace(lookup_descr)

tmp = counts2.groupby(['MONTH','STATE']).sum().sort_values(by='COUNT',ascending=False)#.reset_index(level=0)
del tmp['ORIGIN_AIRPORT_ID']
tmp[:70].plot(kind='barh')
tw.fig_set_geom('l')
#%%
#pd.DataFrame(counts)
#myplt()
#counts.groupby('STATE').sum().sort_values(by='COUNT',ascending=False).plot(kind='barh',legend=False)
#tw.figure();df.groupby('ORIGIN_AIRPORT_SEQ_ID').count().iloc[:,0].plot()
#tw.figure();df.groupby('ORIGIN_CITY_MARKET_ID').count().iloc[:,0].plot()


#%%
#t = time.time()
#tmp = df['ORIGIN_AIRPORT_ID'].replace(lookup_state)
##tmp = df['ORIGIN_AIRPORT_ID']
##for key in dict_city:
##    tmp.replace(key,dict_city[key], inplace=True)
#time.time() - t

#%%



#%%
save_all_figs(os.path.basename(__file__)[:-3])