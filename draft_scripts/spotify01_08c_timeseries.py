# -*- coding: utf-8 -*-
"""
Code forked from spotify01_05b_global_2years.py (timeseries part)
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
from datetime import datetime

from util import *
#%%
#df = load_by_year_date('2015-02')
#df = load_all_data()
df = load_all_data_2years()

df_id = load_airport_idcode_shortcut()
#%%
#%% === create time-series trend of flight-counts per day ===
df['time'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY_OF_MONTH'].astype(str)
print df['time'][:5]
#%%
ts_flightcounts = pd.DataFrame(df['time'].value_counts()).rename(columns={'time':'counts'})
ts_flightcounts.index = ts_flightcounts.index.to_datetime()
ts_flightcounts.sort_index(inplace=True) # need to sort by date

# explicitly add extra date-info as dataframe columns (to apply `groupby` later)
ts_flightcounts['day']= ts_flightcounts.index.day
ts_flightcounts['month']= ts_flightcounts.index.month
ts_flightcounts['day_of_week'] = ts_flightcounts.index.dayofweek

from math import ceil
ts_flightcounts['quarter'] = ts_flightcounts['month'].map(lambda x: int(ceil(x/3.)))

# `dayofweek` uses encoding Monday=0 ... Sunday=6...make this explicit
print ts_flightcounts['day_of_week'][:5]
ts_flightcounts['day_of_week'] = ts_flightcounts['day_of_week'].map({0:'MON',
                                                                     1:'TUE',
                                                                     2:'WED',
                                                                     3:'THU',
                                                                     4:'FRI',
                                                                     5:'SAT',
                                                                     6:'SUN'})
print ts_flightcounts['day_of_week'][:5]
# %% let's use function for above
#from util import df_to_flightcount_ts
##%%
#ts_fc = df_to_flightcount_ts(df)
#%%
ts_flightcounts.plot(y='counts',legend=False)
ts_flightcounts.groupby('day_of_week').sum().plot(kind='bar',y='counts',legend=False)
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

