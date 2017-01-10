# -*- coding: utf-8 -*-

import pandas as pd
import json
import time
import geocoder
import numpy as np

from util import load_airport_data,load_airport_data_3years, hash_state_to_abbrev,print_time
#%%
if __name__ == '__main__':
#    df_data = load_airport_data_3years()
    df_data = load_airport_data()
    #%%
    df_lookup = pd.read_csv('df_lookup_from_0107a.csv')
    hash_airport = df_lookup.set_index('Code')['Airport'].to_dict()
    #%% get unique
    df_lookup['City_State'] = df_lookup['City'] + ' (' + df_lookup['State'] + ')'
    cnts = df_lookup['City_State'].value_counts()
    dups = cnts[cnts != 1]
    
    for dup in dups.index:
        print dup
        
        tmp = df_lookup[df_lookup['City_State'] == dup].Code
    
        for i in tmp.values:
            print "{:8},{}".format((df_data['ORIGIN_AIRPORT_ID'] == i).sum(), hash_airport[i])
    #%%
    cleaner = [
        ('Houston (TX) [Ell]', 'Ellington'), 
        ('Houston (TX) [WP.Hobby]', 'William P Hobby'), 
        ('Houston (TX) [G.Bush]',  'George Bush Intercontinental/Houston'), 
        ('Washington (DC) [R.Reagan]',   'Ronald Reagan Washington National'),
        ('Washington (DC) [W.Dulles]',   'Washington Dulles International'),
        ('Chicago (IL) [Midway]',   'Chicago Midway International'),
        ("Chicago (IL) [O'Hare]",   "Chicago O'Hare International"),
        ("New York (NY) [JFK]",   "John F. Kennedy International"),
        ("New York (NY) [Lag]",   "LaGuardia"),
    ]
    
    for _replace, _airport in cleaner:
        df_lookup.loc[df_lookup['Airport'] == _airport, 'City_State'] = _replace
        
    assert np.all(df_lookup['City_State'].value_counts() == 1)
    #%%
    df_lookup.to_csv('df_lookup.csv',ignore_index=True)