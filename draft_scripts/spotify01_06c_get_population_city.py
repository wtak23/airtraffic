# -*- coding: utf-8 -*-
"""
Create a function to get the desired result
"""
#%%
from tak import reset; reset()
from collections import OrderedDict
import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
#%%
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('http://httpbin.org/get', params=payload)
r.url
#lat: 39.961166
#lon: -75.230301
#%%
#url='http://api.geonames.org/citiesJSON'
#params = dict(username='demo',lang='en',country='US')
##r = requests.get('http://api.geonames.org/citiesJSON?north=44.1&south=-9.9&east=-22.4&west=55.2&lang=en&username=demo ')
#r = requests.get(url,params=params)
#print r.url
