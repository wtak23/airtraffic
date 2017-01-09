# -*- coding: utf-8 -*-

from datetime import datetime
#%%


#%%

def load_airport_idcode_shortcut():
    """ Based on spotify01_08a_study_edges_cleaned.py"""
    df_id = pd.read_csv('df_lookup_from_0107a.csv')

    df_id['City_State'] = df_id['City'] + ' (' + df_id['State'] + ')'

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
        df_id.loc[df_id['Airport'] == _airport, 'City_State'] = _replace
    
    return df_id