# -*- coding: utf-8 -*-
#%%
from tak import reset; reset()

import tak as tw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import os
os.getcwd()

from geopy.geocoders import Nominatim
geolocator = Nominatim()
#lat,lon = df_airports.ix[0,['lat','long']].values
#location = geolocator.reverse("{},{}".format(lat,lon))
#print(location.address)
#print((location.latitude, location.longitude))
#pprint(location.raw)
#%% === study the "carrier.xls" spreadsheet ===
def load_carriers():
    df_carr = pd.read_excel('carriers.xls')
    
    # --- data cleansing ---
    # remove record containing any nans
    df_carr = df_carr.ix[~df_carr.isnull().any(axis=1)].reset_index(drop=True)
    
    # convert columns to unicode (realized some elements are treated as 'int'
    df_carr['Code'] = df_carr['Code'].apply(unicode)
    df_carr['Description'] = df_carr['Description'].apply(unicode)
    
    return df_carr

def load_airports():
    df_airports = pd.read_excel('airports new.xlt')
    
    # convert columns to unicode (realized some elements are treated as 'int'
    df_airports['iata'] = df_airports['iata'].apply(unicode)
    
    return df_airports
    
def myplt():
    # bring plot up front
    plt.gcf().canvas.manager.window.activateWindow()
#%% === study "airports" spreadsheet ===
df_carriers = load_carriers()
df_airports = load_airports()
#%%
#tw.figure('f')
#myplt()
#plt.scatter(x = df_airports['long'].values,y=df_airports['lat'].values)
#plt.grid('on')
#%% === new part from today ===
df = pd.read_csv('690907700_T_ONTIME.csv').iloc[:,:6]
pprint(df.dtypes)
pprint(df.columns.tolist())

#%% are the unique ORIGIN and DEST items all the same?
# YES!
test1 = np.array_equal(np.sort(df['ORIGIN_AIRPORT_ID'].unique()), 
                       np.sort(df['DEST_AIRPORT_ID'].unique()))
                       
test2 = np.array_equal(np.sort(df['ORIGIN_AIRPORT_SEQ_ID'].unique()), 
                       np.sort(df['DEST_AIRPORT_SEQ_ID'].unique()))
                       
test3 = np.array_equal(np.sort(df['ORIGIN_CITY_MARKET_ID'].unique()), 
                       np.sort(df['DEST_CITY_MARKET_ID'].unique()))
#%%
df_air_id = pd.read_csv('L_AIRPORT_ID.csv')
df_seq_id = pd.read_csv('L_AIRPORT_SEQ_ID.csv')
df_market = pd.read_csv('L_CITY_MARKET_ID.csv')

#%% any overlap in the auxiliary info files?
print df_air_id.describe().loc[['min','max']]
print df_seq_id.describe().loc[['min','max']]
print df_market.describe().loc[['min','max']]

# check if the "Code" column intersects (only a single point of intersection)
df_air_id[  df_air_id['Code'].isin(df_market['Code'])  ]
#%%
# only keep the items in the main dataframe
df_air_id = df_air_id[ df_air_id['Code'].isin( df['ORIGIN_AIRPORT_ID']) ].reset_index(drop=True)
df_seq_id = df_seq_id[ df_seq_id['Code'].isin( df['ORIGIN_AIRPORT_SEQ_ID']) ].reset_index(drop=True)
df_market = df_market[ df_market['Code'].isin( df['ORIGIN_CITY_MARKET_ID']) ].reset_index(drop=True)

# The 'Description' column uses a comma and colon to delimit the City,State,Airilne info...
# append info as three new columns 
df_air_id[['City','State','Airline']] = pd.DataFrame(df_air_id['Description'].str.split('[,:]').tolist())
df_seq_id[['City','State','Airline']] = pd.DataFrame(df_seq_id['Description'].str.split('[,:]').tolist())

# here there's only City and State information
df_market[['City','State']] = pd.DataFrame(df_market['Description'].str.split(',').tolist())

# some entry has superfluous info on top of the state abbrev...drop them
print df_market['State'].str.len().value_counts()
df_market['State'] = df_market['State'].str[:3]
#%% === add "Code" column to df_air_id ===
df_ = df.copy()

df_['hi'] = np.nan
for key in df['ORIGIN_AIRPORT_ID'].unique():
    tmp = df_air_id[ df_air_id['Code'] == key ]
    
    mask = df_['ORIGIN_AIRPORT_ID'] == key
    df_.loc[mask,'hi'] = tmp['Description']
#%%
#pd.melt(df,id_vars=['ORIGIN_AIRPORT_ID'])
# create hash-table for 
origin_code = {} 
origin_desc = {} 
for key in df['ORIGIN_AIRPORT_ID'].unique():
    origin_code[key] = df_air_id.loc[df_air_id['Code'] == key,'Code'].values[0]
    origin_desc[key] = df_air_id.loc[df_air_id['Code'] == key,'Description'].values[0]
#%%
sr_orig_cnt = df['ORIGIN_AIRPORT_ID'].value_counts()
sr_orig_cnt[:30].plot(kind='bar')
#%%
#df['ORIGIN_AIRPORT_ID'] = df['ORIGIN_AIRPORT_ID'].astype('category')
grp = df.groupby(['ORIGIN_AIRPORT_ID'])

df['ORIGIN_CITY_MARKET_ID'].value_counts()
#%%
