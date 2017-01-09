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

code_ny = df_id.query('State == "NY"')['Code'].values
code_ca = df_id.query('State == "CA"')['Code'].values

_mask1 = df['ORIGIN_AIRPORT_ID'].isin(code_ny) & df['DEST_AIRPORT_ID'].isin(code_ca)
_mask2 = df['ORIGIN_AIRPORT_ID'].isin(code_ca) & df['DEST_AIRPORT_ID'].isin(code_ny)
df_nycal = df[ _mask1 | _mask2 ]
#%%
ts_flightcounts = df_to_flightcount_ts(df)
#%%
from datetime import datetime
ts_flightcounts['period'] = np.nan
#ts_flightcounts.isnull().sum()
ts_flightcounts.loc[datetime(2014,11,1):datetime(2015,10,31), 'period'] = 'period1'
ts_flightcounts.loc[datetime(2015,11,1):datetime(2016,10,31), 'period'] = 'period2'
assert ts_flightcounts['period'].isnull().sum() == 0
#%%
import statsmodels.formula.api as smf
mod = smf.ols(formula = 'counts ~ C(day_of_week) - 1',data=ts_flightcounts)
#mod = smf.ols(formula = 'COUNT ~ C(day_of_week)',data=tmp)

res = mod.fit()
print res.summary()
tw.figure('t');
#res.resid.plot()
resid = res.resid
ts_flightcounts.plot(y='counts')
tw.figure();(resid + ts_flightcounts['counts'].mean()).plot()
tw.figure();resid.plot()
tw.figure();plt.hist(resid,bins=100)
#%%
#save_all_figs(os.path.basename(__file__)[:-3])
tw.figure();plt.hist(resid,bins=50)
tw.figure();plt.hist(ts_flightcounts['counts'],bins=50)
#%%
tw.figure();resid.plot()
plt.hlines(y = 2*resid.std()*np.array([1,-1]), 
           xmin=plt.xlim()[0],xmax=plt.xlim()[1])
#%%
tw.figure();ts_flightcounts.groupby('month')['counts'].sum().plot(kind='bar')
tw.figure();ts_flightcounts.groupby('day_of_week')['counts'].sum().plot(kind='bar')
tw.figure();ts_flightcounts.groupby('day')['counts'].sum().plot(kind='bar')
#%%
tw.sns_figure()
sns.boxplot(x="month", y="counts",data=ts_flightcounts)
sns.swarmplot(x="month", y="counts",data=ts_flightcounts,alpha=0.5)

tw.sns_figure()
sns.boxplot(x="day_of_week", y="counts",data=ts_flightcounts)
sns.swarmplot(x="day_of_week", y="counts",data=ts_flightcounts,alpha=0.5)

tw.sns_figure()
sns.boxplot(x="quarter", y="counts",data=ts_flightcounts)
sns.swarmplot(x="quarter", y="counts",data=ts_flightcounts,alpha=0.5)

tw.sns_figure()
sns.boxplot(x="day_of_week", y="counts",hue='quarter',data=ts_flightcounts)

#%%
tw.sns_figure();
for dayofweek in ts_flightcounts['day_of_week'].unique():
    sns.distplot(ts_flightcounts.query('day_of_week == @dayofweek')['counts'],
                 hist=False,label=dayofweek)
plt.legend()

tw.sns_figure();
for dayofweek in ts_flightcounts['day_of_week'].unique():
    sns.distplot(ts_flightcounts.query('day_of_week == @dayofweek')['counts'],
                 hist=False,label=dayofweek)
plt.legend()
#%%
tw.sns_figure();
for month in ts_flightcounts['month'].unique():
    sns.kdeplot(ts_flightcounts.query('month == @month')['counts'],
                label=month)#,shade=True,alpha=0.25)
plt.legend()

#%%
save_all_figs(os.path.basename(__file__)[:-3])