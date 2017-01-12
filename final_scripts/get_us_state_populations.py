# -*- coding: utf-8 -*-
"""
Web-scrape US state population from wikipedia using BeautifulSoup
"""
#%%
from collections import OrderedDict
import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
#%%
def get_state_population():
        with open('../data/state_hash.json') as data_file:    
        state_hash = json.load(data_file)
        
    # swap key/val (want to map state name to abbreviation)
    state_hash_inv = dict( zip(state_hash.values(),state_hash.keys()))
    
    url = 'https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population'
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.content)
    
    # get first table in the page
    table = soup.find('table',class_="wikitable sortable")
    
    # store state and 2016 population in dict (to be converted to DataFrame at end)
    df_state_popu = OrderedDict(state=[],population=[])
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 9:
            _state = cells[2].a.contents[0]
            print _state
            if _state in state_hash_inv:
                # only keep 50 states + DC
                df_state_popu['state'].append(_state)
                df_state_popu['population'].append(int(cells[3].contents[0].replace(',', '')))
            
            # get 52 states (50 + DC)
            if len(df_state_popu['state']) == 51:
                break
    
    df_state_popu = pd.DataFrame(df_state_popu)

    # replace state with its abbreviation
    df_state_popu['state'].replace(state_hash_inv,inplace=True)

    return df_state_popu
    
if __name__ == '__main__':
    df_state = get_state_population()
    df_state.to_csv('df_state_populations.csv',index=False)