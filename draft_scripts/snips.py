# -*- coding: utf-8 -*-
"""
['YEAR',
 'QUARTER',
 'MONTH',
 'DAY_OF_MONTH',
 'DAY_OF_WEEK',
 'ORIGIN_AIRPORT_ID',
 'ORIGIN_AIRPORT_SEQ_ID',
 'ORIGIN_CITY_MARKET_ID',
 'DEST_AIRPORT_ID',
 'DEST_AIRPORT_SEQ_ID',
 'DEST_CITY_MARKET_ID']
 """
 #%%
 {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'June',
  7:'July',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
#%%
from tak import reset; reset()

import tak as tw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import os
import time
os.getcwd()

from util import *
#%%
df = load_all_data()
df_carr = load_carriers()
df_airp = load_airports()
#dict_city,dict_state,dict_airline = get_lookup_tables()
#%%
myhash = get_hash(df,'Description')['air_id']
df_ = pd.DataFrame(myhash.values(),columns=['Description'])
df_[['City','State','Airline']] = pd.DataFrame(df_['Description'].str.split(r'(,\s|:\s)').tolist()).iloc[:,[0,2,4]]

df_['City'] = df_['City'].str.lower()

#%%
#%% some manual cleanup
city_replace = {
    'dallas/fort worth':'fort worth',
}
df_['City'].replace(city_replace,inplace=True)

# final apply requried as "split" returns a list for each dataframe elemenet
df_['City'] = df_['City'].str.split('/').apply(lambda s:s[0]) 
#df_['City'] = df_['City'].str.split('/').map(lambda s:s[0]) 


#%%
#df_ = pd.DataFrame(map(lambda s:s.lower(),myhash.values()),columns=['city'])
df2 = pd.read_csv('uscitiespop.txt')
#df2.rename(columns={u'City':'city'},inplace=True)
df2.rename(columns={u'Region':'State'},inplace=True)
df2 = df2[['City','State','Population']]
print "{:.2f}% of data available".format(100*df_.City.isin(df2.City).sum()/float( df_.shape[0]))

#df_.join(df2,on='City',how='inner', lsuffix='fuck',rsuffix='me')
df_id['City'] = df_id['City'].str.lower()
#dfdf=pd.merge(df_,df2, on=['City','State'],how='left')
df_test = pd.merge(df_id,df2,on=['City','State'],how='left')

#%%
df_null = df_test[df_test.isnull().any(axis=1)]