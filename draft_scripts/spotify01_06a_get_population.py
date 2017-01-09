# -*- coding: utf-8 -*-
"""
Here I realized I can download data separaetly for each month/year

Study just the global counts (no "AIRPORT" and "LOCAL" information)
"""
#%%
from tak import reset; reset()
from collections import OrderedDict
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
import requests
from util import *
import json
#%%
with open('state_hash.json') as data_file:    
    state_hash = json.load(data_file)
#%% === try to scrape state popuation info ===
#https://adesquared.wordpress.com/2013/06/16/using-python-beautifulsoup-to-scrape-a-wikipedia-table/
#http://stackoverflow.com/questions/13055208/httperror-http-error-403-forbidden
from bs4 import BeautifulSoup
import urllib2
wiki = "http://en.wikipedia.org/wiki/List_of_postcode_districts_in_the_United_Kingdom"
header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
req = urllib2.Request(wiki,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)
 
area = ""
district = ""
town = ""
county = ""
table = soup.find("table", { "class" : "wikitable sortable" })
print table
#%%
#http://stackoverflow.com/questions/26789042/obtaining-column-from-wikipedia-table-using-beautifulsoup
source_code = requests.get('http://en.wikipedia.org/wiki/Taylor_Swift_discography')
soup = BeautifulSoup(source_code.content)

table = soup.find('span', id='Singles').parent.find_next_sibling('table')
for single in table.find_all('th', scope='row'):
    print(single.text)
#%%
source_code = requests.get('https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population')
soup = BeautifulSoup(source_code.content)
with open('dump.txt','w') as f:
    f.write(soup.__str__())
#%% get first table in the page
table = soup.find('table',class_="wikitable sortable")
print table
with open('dump.txt','w') as f:
    f.write(table.__str__())
#%%
tmp = []
data = OrderedDict(state=[],population=[])
for i,row in enumerate(table.findAll("tr")):
    cells = row.findAll("td")
    if len(cells) == 9:
        data['state'].append(cells[2].a.contents[0])
        data['population'].append(cells[3].contents[0])
        if data['state'][-1] == 'Wyoming':
            break
#%%
data = pd.DataFrame(data)

# invert state lookup table (swap key/val)
state_hash2 = dict( zip(state_hash.values(),state_hash.keys()))
data['state'].replace(state_hash2,inplace=True)

