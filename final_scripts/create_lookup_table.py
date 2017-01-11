# -*- coding: utf-8 -*-

import pandas as pd
import json
import time
import geocoder
from geopy.geocoders import Nominatim
geolocator = Nominatim()

from util import load_airport_data,load_airport_data_3years, hash_state_to_abbrev,print_time
#%%
if __name__ == '__main__':
#    df_data = load_airport_data_3years()
    df_data = load_airport_data()
    #%%
    df_lookup = pd.read_csv('../data/L_AIRPORT_ID.csv')
    
    # unique ID's in the dataset
    uniq_orig = df_data['ORIGIN_AIRPORT_ID'].unique().tolist() 
    uniq_dest = df_data['DEST_AIRPORT_ID'].unique().tolist()
    
    # apply ``set`` function to get unique items in concatenated list
    uniq_id = list(set(uniq_orig + uniq_dest))
    
    print "There are {} Airport-Codes in the lookup table".format(df_lookup.shape[0])
    print "There are {} unique airport-codes in our dataset".format(uniq_id.__len__())
    
    # filter/drop the rows that we do not need in our analysis
    _mask = df_lookup['Code'].isin( uniq_id )
    df_lookup = df_lookup[ _mask ].reset_index(drop=True)

    # --- parse state/city/airport-name from "Description" column
    # apply string "split" method to break information up
    df_parse = map(lambda splits: {'City':splits[0],'State':splits[2],'Airport':splits[4]},
                   df_lookup['Description'].str.split(r'(,\s|:\s)') )
    
    # convert dict to dataframe
    df_parse = pd.DataFrame(df_parse)

    # now we can readily add these information to our lookup table
    df_lookup = df_lookup.join(df_parse)
    
    #%% === add region information ===
    with open('../data/us_states_regions.json','r') as f:
        regions = json.load(f)

    df_region = []
    for key in regions:
        _dftmp = pd.DataFrame( regions[key], columns=['State']  )
        _dftmp['Region'] = key
        df_region.append(_dftmp)
        
    df_region = pd.concat(df_region,ignore_index=True)
    
    # --- use a hash-table (source) to map state name to its abbreviation ---
    hash_state = hash_state_to_abbrev()
    df_region['State'] = df_region['State'].map(lambda key: hash_state[key])
    
    # --- now we are all set to join ---
    df_lookup = df_lookup.merge(df_region,on='State',how='left')
    #%%
    t = time.time()
    lat,lon= [],[]
    n_items = df_lookup.shape[0]
    for i,airport in enumerate(df_lookup['Airport']):
        if i%20==0:
             print '({:3} out of {})'.format(i,n_items),print_time(t)
             
        loc = geolocator.geocode(airport)
        time.sleep(3) # add break to avoid api service timeouts
    
        if loc is not None:
            lon.append(loc[1][0])
            lat.append(loc[1][1])
        else:
            print '    lookup failed for: ' + airport
            lon.append(None)
            lat.append(None)
            
    # add as new columns
    df_lookup['lat'] = lat
    df_lookup['lon'] = lon
    
    n_nans = df_lookup['lat'].isnull().sum(axis=0)
    print "-- {} NANs out {} ({:.2f}%) --".format(n_nans,n_items,n_nans/float(n_items)*100)
    #%%
    idx_nan = []
    for i in xrange(n_items):
        print i,
        if lat[i] is not None:
            continue
        city,state = df_lookup['City'].ix[i], df_lookup['State'].ix[i]
        loc = geolocator.geocode(city+', '+state)
        time.sleep(10) # add break to avoid api service timeouts
    
        if loc is not None:
            lon[i],lat[i] = loc[1]
        else:
            print '    lookup failed for: {}, {}'.format(city,state)
            idx_nan.append(i)
            
    n_nans = df_lookup['lat'].isnull().sum(axis=0)
    print "-- {} NANs out {} ({:.2f}%) --".format(n_nans,n_items,n_nans/float(n_items)*100)
    #%% -- manually look up the two cities that failed
    lat1_,lon1_ = geolocator.geocode('Newport News, VA')[1]
    lat2_,lon2_ = geolocator.geocode('Saipan')[1]
    
    #%%
#    df_lookup.to_csv('df_lookup_from_0106d.csv',index=False)
    