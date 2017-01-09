# -*- coding: utf-8 -*-
"""
Same as part-c, but focus on cal/ny
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
#df = load_all_data_2years()

df_id = load_airport_idcode_shortcut()
hash_citystate= df_id.set_index('Code')['City_State'].to_dict()
#%% === create time-series trend of flight-counts per day ===
df['time'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY_OF_MONTH'].astype(str)
print df['time'][:5]
#%% top 10 used airport
df_top = df['ORIGIN_AIRPORT_ID'].value_counts()[:10]
df_top.index = df_top.index.map(lambda x: hash_citystate[x])

print df_top

df_top = df['DEST_AIRPORT_ID'].value_counts()[:10]
df_top.index = df_top.index.map(lambda x: hash_citystate[x])

print df_top
##%%
## create a new column containing both the *origin* and the *destination* airport
#df['Trips'] = tuple(zip(df['ORIGIN_AIRPORT_ID'], df['DEST_AIRPORT_ID']))
##%% top 20 flights
#trip_counts = get_roundtrips(df['Trips'].value_counts())[:20]
#trip_counts.index = trip_counts.index.map(lambda x: (hash_citystate[x[0]],
#                                                     hash_citystate[x[1]]))
##%% let's focus on the airports top 5 trips
#trip_counts[:5]
#%% === focus on top 10s ===
codes = df['ORIGIN_AIRPORT_ID'].value_counts()[:10].index

df_top = df[ df['ORIGIN_AIRPORT_ID'].isin(codes) ]
#%%
ts_flightcounts = {code:[] for code in codes}
for code in codes:
    mask = df_top['ORIGIN_AIRPORT_ID']==code 
    ts_flightcounts[code] = df_to_flightcount_ts(df_top[mask])

#ts_flights=pd.concat(ts_flightcounts).reset_index(level=0).rename(columns={'level_0':'Code'})
#%%
tw.sns_figure('f')
for code in codes:
    ts_flightcounts[code].plot(y='counts',label=hash_citystate[code],ax=plt.gca())
    
plt.legend()
#%% === get residual plots for each airports ===
from statsmodels.formula.api import ols

for code in codes:
    residual = ols(formula = 'counts ~ C(day_of_week) - 1',data=ts_flightcounts[code]).fit().resid
    ts_flightcounts[code]['residual']  = residual
    ts_flightcounts[code]['resid_lag'] = residual.shift(1) -  residual
    ts_flightcounts[code]['resid_lag_n'] = \
        ts_flightcounts[code]['resid_lag']/np.abs(ts_flightcounts[code]['resid_lag']).max()
#%% plot lagged residual
tw.sns_figure('f')
for code in codes[:5]:
    ts_flightcounts[code].plot(y='residual',label=hash_citystate[code],ax=plt.gca())
#%%
tw.purge()
tw.sns_figure('f')
for code in codes[-3:]:
    ts_flightcounts[code].plot(y='resid_lag',label=hash_citystate[code],ax=plt.gca(),lw=3)
#%%
ts = ts_flightcounts[code]
#%%
ts.groupby('week')
#%%
tw.purge()

win=7
for code in codes:
    tmp = pd.rolling_mean(ts_flightcounts[code]['counts'], win)
#    tmp = pd.rolling_sum(ts_flightcounts[code]['counts'], win)
    tmp.plot(label=hash_citystate[code],ax=plt.gca(),lw=3)
plt.legend()
#%%
ts_flightcounts[code]['counts']

#%% study correlation
tmp = {code:[] for code in codes}
for code in codes:
    tmp[code] = ts_flightcounts[code]['residual']
fu = pd.DataFrame(tmp).rename(columns=hash_citystate)
fu.plot()

tw.figure('f');sns.heatmap(fu.corr(),annot=True)
#%% === try top 100, and see correlation exists ===
codes = df['ORIGIN_AIRPORT_ID'].value_counts()[:100].index

df_top = df[ df['ORIGIN_AIRPORT_ID'].isin(codes) ]
#%%
ts_flightcounts = {code:[] for code in codes}
for code in codes:
    mask = df_top['ORIGIN_AIRPORT_ID']==code 
    ts_flightcounts[code] = df_to_flightcount_ts(df_top[mask])['counts']
#%%
df_count_cities = pd.DataFrame(ts_flightcounts).rename(columns=hash_citystate)
plt.matshow(df_count_cities.corr())
plt.colorbar()
#df['time'].value_counts()
tw.figure('f');sns.heatmap(df_count_cities.corr(), vmax=.8, square=True)
plt.yticks(rotation=0) 
plt.xticks(rotation=90)
plt.tight_layout()
plt.draw()
#%% create residual
from patsy import dmatrix

tmp = pd.DataFrame(ts_flightcounts[code].index.dayofweek)
tmp.columns = ['day_of_week']
mat = np.array(dmatrix('C(day_of_week)-1',tmp))
#%%
df_resid_cities = {code:[] for code in codes}
for code in codes:
    df_resid_cities[code] = sm.OLS(ts_flightcounts[code],mat).fit().resid

df_resid_cities = pd.DataFrame(df_resid_cities).rename(columns=hash_citystate)
df_resid_cities = df_resid_cities.shift(1) - df_resid_cities
tw.figure('f');sns.heatmap(df_resid_cities.corr(), vmax=.8, square=True)
plt.yticks(rotation=0) 
plt.xticks(rotation=90)
plt.tight_layout()