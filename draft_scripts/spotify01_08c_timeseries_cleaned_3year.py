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
df = load_data_3year()

df_id = load_airport_idcode_shortcut()
#%% === create time-series trend of flight-counts per day ===
df['time'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY_OF_MONTH'].astype(str)
print df['time'][:5]
#%%
#from util import df_to_flightcount_ts
##%%
ts_flightcounts = df_to_flightcount_ts(df)

# --- add period info ---
ts_flightcounts['period'] = np.nan
#ts_flightcounts.isnull().sum()
ts_flightcounts.loc[datetime(2013,11,1):datetime(2014,10,31), 'period'] = 'period1'
ts_flightcounts.loc[datetime(2014,11,1):datetime(2015,10,31), 'period'] = 'period2'
ts_flightcounts.loc[datetime(2015,11,1):datetime(2016,10,31), 'period'] = 'period3'
assert ts_flightcounts['period'].isnull().sum() == 0
#%%
tw.sns_figure('t')
ts_flightcounts.plot(y='counts',legend=False,ax=plt.gca())
#%%
#http://stackoverflow.com/questions/37596714/compare-multiple-year-data-on-a-single-plot-python
#http://man7.org/linux/man-pages/man3/strftime.3.html
ts_flightcounts['month'] = ts_flightcounts.index.to_series().dt.strftime('%b')
tw.sns_figure('t')
ts_flightcounts.query('period == "period1"').plot(x='month',y='counts',label='period1',ax=plt.gca())
ts_flightcounts.query('period == "period2"').plot(x='month',y='counts',label='period2',ax=plt.gca())
ts_flightcounts.query('period == "period3"').plot(x='month',y='counts',label='period3',ax=plt.gca())

myplt()
#%%
import statsmodels.formula.api as smf
mod = smf.ols(formula = 'counts ~ C(day_of_week) - 1',data=ts_flightcounts)
#mod = smf.ols(formula = 'COUNT ~ C(day_of_week)',data=tmp)

res = mod.fit()
print res.summary()

ts_flightcounts['residual'] = res.resid
ts_flightcounts['resid_lag'] = ts_flightcounts['residual'].shift(1) - ts_flightcounts['residual']
ts_flightcounts['count_lag'] = ts_flightcounts['counts'].shift(1) - ts_flightcounts['counts']

_,axes = tw.sns_subplots(3,1,'f')
for ax,col in zip(axes, ['counts','residual','resid_lag']):
    plt.sca(ax),plt.title(col)
    ts_flightcounts[col].plot(ax=ax)
    
#tw.figure('t');ts_flightcounts.plot(y='counts',ax=plt.gca())
##tw.figure('t');(resid + ts_flightcounts['counts'].mean()).plot()
#tw.figure('t');ts_flightcounts.plot(y='residual',ax=plt.gca())
#tw.figure('t');ts_flightcounts.plot(y='resid_lag',ax=plt.gca())
#%%
tw.sns_figure('t')
ts_flightcounts.query('period == "period1"').plot(x='month',y='resid_lag',label='period1',ax=plt.gca())
ts_flightcounts.query('period == "period2"').plot(x='month',y='resid_lag',label='period2',ax=plt.gca())
ts_flightcounts.query('period == "period3"').plot(x='month',y='resid_lag',label='period3',ax=plt.gca())
#%%
_,axes = tw.sns_subplots(3,1,'f')
for ax,col in zip(axes, ['counts','residual','resid_lag']):
    plt.sca(ax),plt.title(col)
    ts_flightcounts[col].plot(kind='hist',bins=80,ax=ax)
    
#ts_flightcounts['residual'].plot(kind='hist',bins=100,ax=axes[1])
#ts_flightcounts['resid_lag'].plot(kind='hist',bins=100,ax=axes[2])
#%%
tw.sns_figure('f')
ts_flightcounts['resid_lag'].plot()
plt.hlines(y = 1.5*ts_flightcounts['resid_lag'].std()*np.array([1,-1]), 
           xmin=plt.xlim()[0],xmax=plt.xlim()[1], color='r')
plt.title('resid_lag with 1.5 std')
#%%
_,axes = tw.sns_subplots(3,1,'f')
for ax,col in zip(axes, ['month','day_of_week','day']):
    plt.sca(ax),plt.title(col)
    ts_flightcounts.groupby(col)['counts'].sum().plot(kind='bar')
plt.tight_layout()
#ts_flightcounts.groupby('month')['counts'].sum().plot(kind='bar')
#tw.figure();ts_flightcounts.groupby('day_of_week')['counts'].sum().plot(kind='bar')
#tw.figure();ts_flightcounts.groupby('day')['counts'].sum().plot(kind='bar')
#%%
_,axes=tw.sns_subplots(2,2,'f')
sns.boxplot(x="month", y="counts",data=ts_flightcounts,ax=axes[0])
sns.swarmplot(x="month", y="counts",data=ts_flightcounts,alpha=0.5,ax=axes[0])

sns.boxplot(x="day_of_week", y="counts",data=ts_flightcounts,ax=axes[1])
sns.swarmplot(x="day_of_week", y="counts",data=ts_flightcounts,alpha=0.5,ax=axes[1])

sns.boxplot(x="quarter", y="counts",data=ts_flightcounts,ax=axes[2])
sns.swarmplot(x="quarter", y="counts",data=ts_flightcounts,alpha=0.5,ax=axes[2])

sns.boxplot(x="day_of_week", y="counts",hue='quarter',data=ts_flightcounts,ax=axes[3])
#%%
_,axes=tw.sns_subplots(2,2,'f')
sns.boxplot(x="month", y="counts",hue='period',data=ts_flightcounts,ax=axes[0])
sns.boxplot(x="day_of_week", y="counts",hue='period',data=ts_flightcounts,ax=axes[1])
sns.boxplot(x="quarter", y="counts",hue='period',data=ts_flightcounts,ax=axes[2])
#sns.swarmplot(x="quarter", y="counts",data=ts_flightcounts,alpha=0.5,ax=axes[2])
#sns.boxplot(x="day_of_week", y="counts",hue='quarter',data=ts_flightcounts,ax=axes[3])

#%%
tw.sns_figure();
for dayofweek in ts_flightcounts['day_of_week'].unique():
    sns.distplot(ts_flightcounts.query('day_of_week == @dayofweek')['counts'],
                 hist=False,label=dayofweek)
plt.legend()

tw.sns_figure();
for month in ts_flightcounts['month'].unique():
    sns.kdeplot(ts_flightcounts.query('month == @month')['counts'],
                label=month)#,shade=True,alpha=0.25)
plt.legend()

#%%
save_all_figs(os.path.basename(__file__)[:-3])

