# -*- coding: utf-8 -*-
#%%
from geopy.distance import vincenty
trip_dist = {code: [] for code in trip_counts.index}
for code1,code2 in trip_counts.index:
    coord1 = hash_lat[code1],hash_lon[code1]
    coord2 = hash_lat[code2],hash_lon[code2]
    trip_dist[code1,code2] = vincenty(coord1,coord2).kilometers

trip_dist = pd.Series(trip_dist)
trip_info = pd.DataFrame(trip_counts)
trip_info['distance'] = trip_dist

trip_info.index   = trip_counts.index.map(lambda x: (hash_citystate[x[0]], hash_citystate[x[1]]))