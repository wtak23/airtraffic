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
dict_counts = {}
plt.close('all')
_,axes = plt.subplots(2,2,figsize=(24,12))
axes = axes.ravel()
myplt()
for i,col in enumerate(['QUARTER','MONTH','DAY_OF_MONTH','DAY_OF_WEEK']):
    #dict_counts[col] = df.groupby(col)[col].count()
    plt.sca(axes[i])
    df.groupby(col)[col].count().plot(kind='bar')
#%%
# do this for each month
_,axes = plt.subplots(3,4,figsize=(24,12),sharex=True,sharey=True)
plt.tight_layout()
axes = axes.ravel()

for month in range(1,13):
    plt.sca(axes[month-1])
    df.query('MONTH == @month').groupby('DAY_OF_WEEK').count().iloc[:,0].plot(kind='bar')
    plt.title(month)
    plt.grid('on')
    
    
# do this for each day-of-week
_,axes = plt.subplots(2,4,figsize=(24,12),sharex=True,sharey=True)
axes = axes.ravel()

for week in range(1,7+1):
    plt.sca(axes[week-1])
    df.query('DAY_OF_WEEK == @week').groupby('MONTH').count().iloc[:,0].plot(kind='bar')
    plt.title(week)
    plt.grid('on')
#%%
# create dataframe summarizing counts
df_counts = df.groupby(['MONTH','DAY_OF_WEEK']).count().iloc[:,0].reset_index()
df_counts.columns = ['MONTH','DAY_OF_WEEK','COUNT']
#df_counts.plot(kind='bar',x='MONTH',y='COUNT')

#%% plot using seaborn
plt.figure();myplt()
sns.countplot(x='MONTH',data=df,hue='DAY_OF_WEEK')

plt.figure();myplt()
sns.countplot(x='DAY_OF_WEEK',data=df,hue='MONTH')

_,axes=plt.subplots(2,1)
sns.countplot(x='DAY_OF_MONTH',data=df.query('1<=DAY_OF_MONTH<=15'),hue='DAY_OF_WEEK',ax=axes[0])
sns.countplot(x='DAY_OF_MONTH',data=df.query('16<=DAY_OF_MONTH<=31'),hue='DAY_OF_WEEK',ax=axes[1])
#%%
plt.figure()
sns.countplot(x='QUARTER',data=df.query('1<=DAY_OF_MONTH<=15'),hue='DAY_OF_WEEK')
plt.figure()
sns.countplot(x='QUARTER',data=df.query('1<=DAY_OF_MONTH<=15'))
#%% === create time-series trend of trips per day ===
#df['time'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY_OF_MONTH'].astype(str)
df['time'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY_OF_MONTH'].astype(str)
tmp = df.groupby('time').count().iloc[:,0]
tmp.index = tmp.index.to_datetime()
tmp = tmp.sort_index()
tw.figure();tmp.plot()
#%%
t=time.time()
df['time'] = df['YEAR'].astype(str) + '-' + df['MONTH'].astype(str) + '-' + df['DAY_OF_MONTH'].astype(str)
print time.time() - t
#%%
tmp = pd.DataFrame(df.groupby('time').count().iloc[:,0])
tmp.columns = ['COUNT']
# convert index to Date_Time index
tmp.index = tmp.index.to_datetime()
tmp = tmp.sort_index()

tmp['day']= tmp.index.dayofweek

hash_dayofweek = dict( zip(range(7), ['MON','TUE','WED','THU','FRI','SAT','SUN'] ))
tmp['day_of_week'] = tmp['day'].replace(hash_dayofweek)
#%%
tw.figure();tmp.plot(y='COUNT')
#%%
tmp.groupby('day_of_week').sum().plot(kind='bar',y='COUNT')
#%%
import statsmodels.formula.api as smf
#mod = smf.ols(formula = 'COUNT ~ C(day_of_week) - 1',data=tmp)
mod = smf.ols(formula = 'COUNT ~ C(day_of_week)',data=tmp)

res = mod.fit()
print res.summary()
tw.figure('t');
res.resid.plot()
resid = res.resid
(resid + 1.638e+04).plot()
tmp.plot(y='COUNT')
#%%
save_all_figs(os.path.basename(__file__)[:-3])






 








