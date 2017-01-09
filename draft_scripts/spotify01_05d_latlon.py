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
#%%
#df = load_by_year_date('2015-02')
df = load_all_data()
cols = df.columns.tolist()
pprint(cols)
#%% any interesting patterns among Quarter? Month? Day of Month? Day of Week?
df_air = load_airports()

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
#%%
col = 'Description'
myhash = get_hash(df,col)['air_id']
tmp = pd.DataFrame(myhash.values(),columns=[col])
tmp[['City','State','Airline']] = pd.DataFrame(tmp[col].str.split(r'(,\s|:\s)').tolist()).iloc[:,[0,2,4]]
del tmp['Description']
tmp[0:1]

df_air.query('state == "AK"')
mask = (tmp['City'] == 'King Salmon')
tmp[mask]
#%%
tmp['City'].value_counts()
#%%
tmp_ = tmp.ix[0]
tmp_['City'].lower() in df_air['city'].str.lower()
tmp['Airline'][4].lower() in df_air['airport'].str.lower()
from geopy.geocoders import Nominatim
geolocator = Nominatim()
#%%
_lat = []
_lon = []

t = time.time()

for i,(city,state) in enumerate(zip(tmp['City'],tmp['State'])):
    if i%10==0: tw.print_time(t);print i
    loc = geolocator.geocode(query = dict(city=city,state=state))
    if loc is not None:
        _lon.append(loc.longitude)
        _lat.append(loc.latitude)
    else:
        loc = geolocator.geocode(query = dict(state=state))
        if loc:
            _lon.append(loc.longitude)
            _lat.append(loc.latitude)
        else:
            # i give up...return None
            _lon.append(None)
            _lat.append(None)

#for i,(city,state) in enumerate(zip(tmp['City'],tmp['State'])):
#    if i%10==0: tw.print_time(t);print i
#    loc = geocoder.google('{}, {}'.format(city,state))
#    if loc is not None:
#        _lon.append(loc.lng)
#        _lat.append(loc.lat)
#    else:
#        _lon.append(None)
#        _lat.append(None)
tmp['lat'] = _lat
tmp['lon'] = _lon
#%%
airline = tmp['Airline']

ttt = df_air.query('state == "IN"')

#%%
t = time.time()
_lat = []
_lon = []
for i,aaa in enumerate(tmp['Airline']):
    if i%10==0: tw.print_time(t);print i
    loc = geocoder.google(aaa)
    if loc is not None:
        _lon.append(loc.lng)
        _lat.append(loc.lat)
    else:
        _lon.append(None)
        _lat.append(None)
        
