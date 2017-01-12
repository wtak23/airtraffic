Create lookup-table
"""""""""""""""""""
The original ipython notebook can be downloaded from `here <http://nbviewer.jupyter.org/github/wtak23/airtraffic/blob/master/final_scripts/create_lookup_table.ipynb>`__ .


.. code:: python

    %matplotlib inline
    import pandas as pd
    import time
    import numpy as np
    
    from pprint import pprint
    from util import print_time

Aim of notebook
===============

-  The `airport traffic
   dataset <http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time>`__
   encodes the airport with unique ID numbers.

-  In this notebook, we'll create an *enhanced lookup-table* by taking
   the lookup table provided by the BTS (`download
   link <http://www.transtats.bts.gov/Download_Lookup.asp?Lookup=L_AIRPORT_ID>`__)
   and adding additional relevant information regarding the airport
   (such as latitude/longitutde info)

Load the main airport traffic data
==================================

-  Load 3 years worth of air-traffic data provided by BTS
   (`link <http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time>`__)
-  (from November 2013 to October 2016)

.. code:: python

    from util import load_airport_data_3years
    df_data = load_airport_data_3years()


.. parsed-literal::
    :class: myliteral

     ... load dataframe from 2013-11.zip 
     ... load dataframe from 2013-12.zip 
     ... load dataframe from 2014-01.zip 
     ... load dataframe from 2014-02.zip 
     ... load dataframe from 2014-03.zip 
     ... load dataframe from 2014-04.zip 
     ... load dataframe from 2014-05.zip 
     ... load dataframe from 2014-06.zip 
     ... load dataframe from 2014-07.zip 
     ... load dataframe from 2014-08.zip 
     ... load dataframe from 2014-09.zip 
     ... load dataframe from 2014-10.zip 
     ... load dataframe from 2014-11.zip 
     ... load dataframe from 2014-12.zip 
     ... load dataframe from 2015-01.zip 
     ... load dataframe from 2015-02.zip 
     ... load dataframe from 2015-03.zip 
     ... load dataframe from 2015-04.zip 
     ... load dataframe from 2015-05.zip 
     ... load dataframe from 2015-06.zip 
     ... load dataframe from 2015-07.zip 
     ... load dataframe from 2015-08.zip 
     ... load dataframe from 2015-09.zip 
     ... load dataframe from 2015-10.zip 
     ... load dataframe from 2015-11.zip 
     ... load dataframe from 2015-12.zip 
     ... load dataframe from 2016-01.zip 
     ... load dataframe from 2016-02.zip 
     ... load dataframe from 2016-03.zip 
     ... load dataframe from 2016-04.zip 
     ... load dataframe from 2016-05.zip 
     ... load dataframe from 2016-06.zip 
     ... load dataframe from 2016-07.zip 
     ... load dataframe from 2016-08.zip 
     ... load dataframe from 2016-09.zip 
     ... load dataframe from 2016-10.zip 
    

.. code:: python

    print df_data.shape
    df_data.head(n=5)


.. parsed-literal::
    :class: myliteral

    (17364696, 7)
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>YEAR</th>
          <th>QUARTER</th>
          <th>MONTH</th>
          <th>DAY_OF_MONTH</th>
          <th>DAY_OF_WEEK</th>
          <th>ORIGIN_AIRPORT_ID</th>
          <th>DEST_AIRPORT_ID</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2013</td>
          <td>4</td>
          <td>11</td>
          <td>3</td>
          <td>7</td>
          <td>12478</td>
          <td>10693</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2013</td>
          <td>4</td>
          <td>11</td>
          <td>4</td>
          <td>1</td>
          <td>12478</td>
          <td>10693</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2013</td>
          <td>4</td>
          <td>11</td>
          <td>5</td>
          <td>2</td>
          <td>12478</td>
          <td>10693</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2013</td>
          <td>4</td>
          <td>11</td>
          <td>6</td>
          <td>3</td>
          <td>12478</td>
          <td>10693</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2013</td>
          <td>4</td>
          <td>11</td>
          <td>7</td>
          <td>4</td>
          <td>12478</td>
          <td>10693</td>
        </tr>
      </tbody>
    </table>
    </div>



Load lookup table provided by BTS
=================================

.. code:: python

    df_lookup = pd.read_csv('../data/L_AIRPORT_ID.csv')
    print df_lookup.shape


.. parsed-literal::
    :class: myliteral

    (6409, 2)
    

Create *enhanced* lookuptable
=============================

.. code:: python

    df_lookup.head(n=10)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Code</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>10001</td>
          <td>Afognak Lake, AK: Afognak Lake Airport</td>
        </tr>
        <tr>
          <th>1</th>
          <td>10003</td>
          <td>Granite Mountain, AK: Bear Creek Mining Strip</td>
        </tr>
        <tr>
          <th>2</th>
          <td>10004</td>
          <td>Lik, AK: Lik Mining Camp</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10005</td>
          <td>Little Squaw, AK: Little Squaw Airport</td>
        </tr>
        <tr>
          <th>4</th>
          <td>10006</td>
          <td>Kizhuyak, AK: Kizhuyak Bay</td>
        </tr>
        <tr>
          <th>5</th>
          <td>10007</td>
          <td>Klawock, AK: Klawock Seaplane Base</td>
        </tr>
        <tr>
          <th>6</th>
          <td>10008</td>
          <td>Elizabeth Island, AK: Elizabeth Island Airport</td>
        </tr>
        <tr>
          <th>7</th>
          <td>10009</td>
          <td>Homer, AK: Augustin Island</td>
        </tr>
        <tr>
          <th>8</th>
          <td>10010</td>
          <td>Hudson, NY: Columbia County</td>
        </tr>
        <tr>
          <th>9</th>
          <td>10011</td>
          <td>Peach Springs, AZ: Grand Canyon West</td>
        </tr>
      </tbody>
    </table>
    </div>



Remove Code that is not present our dataset
-------------------------------------------

.. code:: python

    # unique ID's in the dataset
    uniq_orig = df_data['ORIGIN_AIRPORT_ID'].unique().tolist() 
    uniq_dest = df_data['DEST_AIRPORT_ID'].unique().tolist()
    
    # apply ``set`` function to get unique items in concatenated list
    uniq_id = list(set(uniq_orig + uniq_dest))
    
    print "There are {} Airport-Codes in the lookup table".format(df_lookup.shape[0])
    print "There are {} unique airport-codes in our dataset".format(uniq_id.__len__())


.. parsed-literal::
    :class: myliteral

    There are 6409 Airport-Codes in the lookup table
    There are 334 unique airport-codes in our dataset
    

Let's filter/drop the rows/records that we do not need in our analysis

.. code:: python

    # only keep the items in the main dataframe
    _mask = df_lookup['Code'].isin( uniq_id )
    df_lookup = df_lookup[ _mask ].reset_index(drop=True)
    
    print df_lookup.shape
    df_lookup.head(10)


.. parsed-literal::
    :class: myliteral

    (334, 2)
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Code</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>10135</td>
          <td>Allentown/Bethlehem/Easton, PA: Lehigh Valley ...</td>
        </tr>
        <tr>
          <th>1</th>
          <td>10136</td>
          <td>Abilene, TX: Abilene Regional</td>
        </tr>
        <tr>
          <th>2</th>
          <td>10140</td>
          <td>Albuquerque, NM: Albuquerque International Sun...</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10141</td>
          <td>Aberdeen, SD: Aberdeen Regional</td>
        </tr>
        <tr>
          <th>4</th>
          <td>10146</td>
          <td>Albany, GA: Southwest Georgia Regional</td>
        </tr>
        <tr>
          <th>5</th>
          <td>10154</td>
          <td>Nantucket, MA: Nantucket Memorial</td>
        </tr>
        <tr>
          <th>6</th>
          <td>10155</td>
          <td>Waco, TX: Waco Regional</td>
        </tr>
        <tr>
          <th>7</th>
          <td>10157</td>
          <td>Arcata/Eureka, CA: Arcata</td>
        </tr>
        <tr>
          <th>8</th>
          <td>10158</td>
          <td>Atlantic City, NJ: Atlantic City International</td>
        </tr>
        <tr>
          <th>9</th>
          <td>10165</td>
          <td>Adak Island, AK: Adak</td>
        </tr>
      </tbody>
    </table>
    </div>



Parse state,city, and airport-name from 'Description' field
-----------------------------------------------------------

-  Above we realize that the ``Description`` field contains information
   regarding the *city*, *state*, and *name* of the airport.

-  Let's create individual field for each information.

-  Fortunately, the ``Description`` column uses a comma (``,``) and
   colon (``:``) to delimit the City, State, Airport-name information,
   so splitting these are is straightforward.

.. code:: python

    # apply string "split" method to break information up
    df_parse = map(lambda splits: {'City':splits[0],'State':splits[2],'Airport':splits[4]},
                   df_lookup['Description'].str.split(r'(,\s|:\s)') )
    
    pprint(df_parse[:5])
    
    # convert dict to dataframe
    df_parse = pd.DataFrame(df_parse)
    df_parse.head(5)


.. parsed-literal::
    :class: myliteral

    [{'Airport': 'Lehigh Valley International',
      'City': 'Allentown/Bethlehem/Easton',
      'State': 'PA'},
     {'Airport': 'Abilene Regional', 'City': 'Abilene', 'State': 'TX'},
     {'Airport': 'Albuquerque International Sunport',
      'City': 'Albuquerque',
      'State': 'NM'},
     {'Airport': 'Aberdeen Regional', 'City': 'Aberdeen', 'State': 'SD'},
     {'Airport': 'Southwest Georgia Regional', 'City': 'Albany', 'State': 'GA'}]
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>Lehigh Valley International</td>
          <td>Allentown/Bethlehem/Easton</td>
          <td>PA</td>
        </tr>
        <tr>
          <th>1</th>
          <td>Abilene Regional</td>
          <td>Abilene</td>
          <td>TX</td>
        </tr>
        <tr>
          <th>2</th>
          <td>Albuquerque International Sunport</td>
          <td>Albuquerque</td>
          <td>NM</td>
        </tr>
        <tr>
          <th>3</th>
          <td>Aberdeen Regional</td>
          <td>Aberdeen</td>
          <td>SD</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Southwest Georgia Regional</td>
          <td>Albany</td>
          <td>GA</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # now we can readily add these information to our lookup table
    df_lookup = df_lookup.join(df_parse)
    
    print df_lookup.shape
    df_lookup.head()


.. parsed-literal::
    :class: myliteral

    (334, 5)
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Code</th>
          <th>Description</th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>10135</td>
          <td>Allentown/Bethlehem/Easton, PA: Lehigh Valley ...</td>
          <td>Lehigh Valley International</td>
          <td>Allentown/Bethlehem/Easton</td>
          <td>PA</td>
        </tr>
        <tr>
          <th>1</th>
          <td>10136</td>
          <td>Abilene, TX: Abilene Regional</td>
          <td>Abilene Regional</td>
          <td>Abilene</td>
          <td>TX</td>
        </tr>
        <tr>
          <th>2</th>
          <td>10140</td>
          <td>Albuquerque, NM: Albuquerque International Sun...</td>
          <td>Albuquerque International Sunport</td>
          <td>Albuquerque</td>
          <td>NM</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10141</td>
          <td>Aberdeen, SD: Aberdeen Regional</td>
          <td>Aberdeen Regional</td>
          <td>Aberdeen</td>
          <td>SD</td>
        </tr>
        <tr>
          <th>4</th>
          <td>10146</td>
          <td>Albany, GA: Southwest Georgia Regional</td>
          <td>Southwest Georgia Regional</td>
          <td>Albany</td>
          <td>GA</td>
        </tr>
      </tbody>
    </table>
    </div>



Add state 'region' information
------------------------------

I also would like to study patterns among the four-regions in the United
States:

(1) Northeast
(2) South
(3) West
(4) Midwest

I saved a json lookup file for this purpose

.. code:: python

    %%bash
    cat ../data/us_states_regions.json


.. parsed-literal::
    :class: myliteral

    {
    "Northeast" : ["Connecticut","Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont","New Jersey", "New York", "Pennsylvania"],
    "Midwest"   : ["Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin", "Iowa", "Kansas", "Minnesota", "Missouri", "Nebraska", "North Dakota", "South Dakota"],
    "South"     : [ "Delaware", "Florida", "Georgia", "Maryland", "North Carolina", "South Carolina", "Virginia", "District of Columbia", "West Virginia",             "Alabama", "Kentucky", "Mississippi", "Tennessee","Arkansas", "Louisiana", "Oklahoma", "Texas"],
    "West"      : ["Arizona", "Colorado", "Idaho", "Montana", "Nevada", "New Mexico", "Utah",  "Wyoming", "Alaska", "California", "Hawaii", "Oregon", "Washington"]
    }

.. code:: python

    import json
    with open('../data/us_states_regions.json','r') as f:
        regions = json.load(f)
    
    print regions.keys()
    print regions.values()


.. parsed-literal::
    :class: myliteral

    [u'West', u'Northeast', u'Midwest', u'South']
    [[u'Arizona', u'Colorado', u'Idaho', u'Montana', u'Nevada', u'New Mexico', u'Utah', u'Wyoming', u'Alaska', u'California', u'Hawaii', u'Oregon', u'Washington'], [u'Connecticut', u'Maine', u'Massachusetts', u'New Hampshire', u'Rhode Island', u'Vermont', u'New Jersey', u'New York', u'Pennsylvania'], [u'Illinois', u'Indiana', u'Michigan', u'Ohio', u'Wisconsin', u'Iowa', u'Kansas', u'Minnesota', u'Missouri', u'Nebraska', u'North Dakota', u'South Dakota'], [u'Delaware', u'Florida', u'Georgia', u'Maryland', u'North Carolina', u'South Carolina', u'Virginia', u'District of Columbia', u'West Virginia', u'Alabama', u'Kentucky', u'Mississippi', u'Tennessee', u'Arkansas', u'Louisiana', u'Oklahoma', u'Texas']]
    

.. code:: python

    df_region = []
    for key in regions:
        _dftmp = pd.DataFrame( regions[key], columns=['State']  )
        _dftmp['Region'] = key
        df_region.append(_dftmp)
        
    df_region = pd.concat(df_region,ignore_index=True)
    
    df_region.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>State</th>
          <th>Region</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>Arizona</td>
          <td>West</td>
        </tr>
        <tr>
          <th>1</th>
          <td>Colorado</td>
          <td>West</td>
        </tr>
        <tr>
          <th>2</th>
          <td>Idaho</td>
          <td>West</td>
        </tr>
        <tr>
          <th>3</th>
          <td>Montana</td>
          <td>West</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Nevada</td>
          <td>West</td>
        </tr>
      </tbody>
    </table>
    </div>



Let's use a hash-table (source) to map state name to its abbreviation

.. code:: python

    from util import hash_state_to_abbrev
    hash_state = hash_state_to_abbrev()
    
    df_region['State'] = df_region['State'].map(lambda key: hash_state[key])
    df_region.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>State</th>
          <th>Region</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>AZ</td>
          <td>West</td>
        </tr>
        <tr>
          <th>1</th>
          <td>CO</td>
          <td>West</td>
        </tr>
        <tr>
          <th>2</th>
          <td>ID</td>
          <td>West</td>
        </tr>
        <tr>
          <th>3</th>
          <td>MT</td>
          <td>West</td>
        </tr>
        <tr>
          <th>4</th>
          <td>NV</td>
          <td>West</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # good, we're now ready to join this "Region" information to our lookup table
    df_lookup = df_lookup.merge(df_region,on='State',how='left')
    
    df_lookup.head(10)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Code</th>
          <th>Description</th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
          <th>Region</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>10135</td>
          <td>Allentown/Bethlehem/Easton, PA: Lehigh Valley ...</td>
          <td>Lehigh Valley International</td>
          <td>Allentown/Bethlehem/Easton</td>
          <td>PA</td>
          <td>Northeast</td>
        </tr>
        <tr>
          <th>1</th>
          <td>10136</td>
          <td>Abilene, TX: Abilene Regional</td>
          <td>Abilene Regional</td>
          <td>Abilene</td>
          <td>TX</td>
          <td>South</td>
        </tr>
        <tr>
          <th>2</th>
          <td>10140</td>
          <td>Albuquerque, NM: Albuquerque International Sun...</td>
          <td>Albuquerque International Sunport</td>
          <td>Albuquerque</td>
          <td>NM</td>
          <td>West</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10141</td>
          <td>Aberdeen, SD: Aberdeen Regional</td>
          <td>Aberdeen Regional</td>
          <td>Aberdeen</td>
          <td>SD</td>
          <td>Midwest</td>
        </tr>
        <tr>
          <th>4</th>
          <td>10146</td>
          <td>Albany, GA: Southwest Georgia Regional</td>
          <td>Southwest Georgia Regional</td>
          <td>Albany</td>
          <td>GA</td>
          <td>South</td>
        </tr>
        <tr>
          <th>5</th>
          <td>10154</td>
          <td>Nantucket, MA: Nantucket Memorial</td>
          <td>Nantucket Memorial</td>
          <td>Nantucket</td>
          <td>MA</td>
          <td>Northeast</td>
        </tr>
        <tr>
          <th>6</th>
          <td>10155</td>
          <td>Waco, TX: Waco Regional</td>
          <td>Waco Regional</td>
          <td>Waco</td>
          <td>TX</td>
          <td>South</td>
        </tr>
        <tr>
          <th>7</th>
          <td>10157</td>
          <td>Arcata/Eureka, CA: Arcata</td>
          <td>Arcata</td>
          <td>Arcata/Eureka</td>
          <td>CA</td>
          <td>West</td>
        </tr>
        <tr>
          <th>8</th>
          <td>10158</td>
          <td>Atlantic City, NJ: Atlantic City International</td>
          <td>Atlantic City International</td>
          <td>Atlantic City</td>
          <td>NJ</td>
          <td>Northeast</td>
        </tr>
        <tr>
          <th>9</th>
          <td>10165</td>
          <td>Adak Island, AK: Adak</td>
          <td>Adak</td>
          <td>Adak Island</td>
          <td>AK</td>
          <td>West</td>
        </tr>
      </tbody>
    </table>
    </div>



Add airport latitude and longitude information using geocoder
-------------------------------------------------------------

Next we'll query the geograhical location of each airport using
geocoders from ``geopy``
(`link <https://geopy.readthedocs.io/en/1.10.0/>`__).

This information will be useful especially when creating visualization
plots.

The cell below is going to take a while, so good time to brew a
coffee... (need to add breaks between API requests to avoid getting
timed-out)

.. code:: python

    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    
    t = time.time()
    lat,lon= [],[]
    n_items = df_lookup.shape[0]
    for i,airport in enumerate(df_lookup['Airport']):
        if i%20==0:
             print '({:3} out of {})'.format(i,n_items),print_time(t)
    
        loc = geolocator.geocode(airport)
        time.sleep(20) # add break to avoid api service timeouts
    
        if loc is not None:
            lon.append(loc[1][0])
            lat.append(loc[1][1])
        else:
            print '    lookup failed for: ' + airport
            lon.append(None)
            lat.append(None)
    
    


.. parsed-literal::
    :class: myliteral

    (  0 out of 334) Elapsed time:  0.00 seconds
    ( 20 out of 334) Elapsed time: 410.26 seconds
        lookup failed for: Western Neb. Regional/William B. Heilig Field
        lookup failed for: Greater Binghamton/Edwin A. Link Field
    ( 40 out of 334) Elapsed time: 818.81 seconds
        lookup failed for: Boise Air Terminal
        lookup failed for: Brownsville South Padre Island International
        lookup failed for: Baltimore/Washington International Thurgood Marshall
        lookup failed for: Akron-Canton Regional
    ( 60 out of 334) Elapsed time: 1227.76 seconds
        lookup failed for: Charleston AFB/International
        lookup failed for: Casper/Natrona County International
    ( 80 out of 334) Elapsed time: 1636.89 seconds
        lookup failed for: Dickinson - Theodore Roosevelt Regional
    (100 out of 334) Elapsed time: 2045.76 seconds
        lookup failed for: Northwest Florida Beaches International
        lookup failed for: Erie International/Tom Ridge Field
    (120 out of 334) Elapsed time: 2454.87 seconds
        lookup failed for: Green Bay Austin Straubel International
        lookup failed for: Robert Gray AAF
    (140 out of 334) Elapsed time: 2863.93 seconds
        lookup failed for: Huntsville International-Carl T Jones Field
    (160 out of 334) Elapsed time: 3273.42 seconds
        lookup failed for: Falls International Einarson Field
        lookup failed for: Jackson Medgar Wiley Evers International
    (180 out of 334) Elapsed time: 3682.23 seconds
        lookup failed for: Lafayette Regional Paul Fournet Field
        lookup failed for: Bill and Hillary Clinton Nat Adams Field
    (200 out of 334) Elapsed time: 4090.87 seconds
    (220 out of 334) Elapsed time: 4499.89 seconds
        lookup failed for: Modesto City-County-Harry Sham Field
        lookup failed for: Dane County Regional-Truax Field
        lookup failed for: Louis Armstrong New Orleans International
    (240 out of 334) Elapsed time: 4908.80 seconds
        lookup failed for: Newport News/Williamsburg International
    (260 out of 334) Elapsed time: 5317.79 seconds
        lookup failed for: Petersburg James A Johnson
        lookup failed for: Theodore Francis Green State
        lookup failed for: Roanoke Blacksburg Regional Woodrum Field
        lookup failed for: Roswell International Air Center
    (280 out of 334) Elapsed time: 5727.01 seconds
        lookup failed for: San Angelo Regional/Mathis Field
        lookup failed for: Santa Maria Public/Capt. G. Allan Hancock Field
    (300 out of 334) Elapsed time: 6135.91 seconds
        lookup failed for: Francisco C. Ada Saipan International
        lookup failed for: Sheppard AFB/Wichita Falls Municipal
        lookup failed for: Sioux Gateway/Col. Bud Day Field
        lookup failed for: Tri-Cities Regional TN/VA
    (320 out of 334) Elapsed time: 6544.53 seconds
        lookup failed for: Joslin Field - Magic Valley Regional
        lookup failed for: Texarkana Regional-Webb Field
        lookup failed for: Eglin AFB Destin Fort Walton Beach
        lookup failed for: Yuma MCAS/Yuma International
    

.. code:: python

    # add as new columns
    df_lookup['lat'] = lat
    df_lookup['lon'] = lon
    
    n_nans = df_lookup['lat'].isnull().sum(axis=0)
    print "-- {} NANs out {} ({:.2f}%) --".format(n_nans,n_items,n_nans/float(n_items)*100)


.. parsed-literal::
    :class: myliteral

    -- 36 NANs out 334 (10.78%) --
    

-  So some lookup failed...but most succeeded

-  For airports that failed, search using City + State information (lose
   locality a bit but will suffice for our analysis)

.. code:: python

    idx_nan = [] # keep track of the index location that may fail yet again
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


.. parsed-literal::
    :class: myliteral

    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248     lookup failed for: Newport News/Williamsburg, VA
    249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302     lookup failed for: Saipan, TT
    303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333
    

.. code:: python

    # update columns
    df_lookup['lat'] = lat
    df_lookup['lon'] = lon
    
    n_nans = df_lookup['lat'].isnull().sum(axis=0)
    print "-- {} NANs out {} ({:.2f}%) --".format(n_nans,n_items,n_nans/float(n_items)*100)


.. parsed-literal::
    :class: myliteral

    -- 2 NANs out 334 (0.60%) --
    

.. code:: python

    df_lookup = pd.read_csv('df_lookup_tmp.csv')

-  So at this point, we have two lookup failures

-  Although unelegant, I'll just manually query these in the geocoder

.. code:: python

    print idx_nan
    df_lookup[df_lookup['lat'].isnull()]


.. parsed-literal::
    :class: myliteral

    [248, 302]
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Code</th>
          <th>Description</th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
          <th>Region</th>
          <th>lat</th>
          <th>lon</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>248</th>
          <td>14098</td>
          <td>Newport News/Williamsburg, VA: Newport News/Wi...</td>
          <td>Newport News/Williamsburg International</td>
          <td>Newport News/Williamsburg</td>
          <td>VA</td>
          <td>South</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>302</th>
          <td>14955</td>
          <td>Saipan, TT: Francisco C. Ada Saipan International</td>
          <td>Francisco C. Ada Saipan International</td>
          <td>Saipan</td>
          <td>TT</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    lat,lon = geolocator.geocode('Newport News, VA')[1]
    df_lookup['lat'].ix[248] = lat
    df_lookup['lon'].ix[248] = lon
    
    lat,lon = geolocator.geocode('Saipan')[1]
    df_lookup['lat'].ix[302] = lat
    df_lookup['lon'].ix[302] = lon
    
    print df_lookup.isnull().sum()


.. parsed-literal::
    :class: myliteral

    Code           0
    Description    0
    Airport        0
    City           0
    State          0
    Region         8
    lat            0
    lon            0
    dtype: int64
    

Add column with both city and state
-----------------------------------

-  Since I am not familiar with many names of the airport, I'd rather
   work with City and State names.

-  However, there may be multiple airports in the same city (eg, JKF and
   Laguardia in NYC), so uniqueness of "City/State" is not guaranteed.

-  Here, I'll create yet another (and final) column containing both the
   City and State information, and modify duplicates as needed.

.. code:: python

    df_lookup['City_State'] = df_lookup['City'] + ' (' + df_lookup['State'] + ')'
    
    df_lookup.sample(5)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Code</th>
          <th>Description</th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
          <th>Region</th>
          <th>lat</th>
          <th>lon</th>
          <th>City_State</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>269</th>
          <td>14520</td>
          <td>Rhinelander, WI: Rhinelander/Oneida County</td>
          <td>Rhinelander/Oneida County</td>
          <td>Rhinelander</td>
          <td>WI</td>
          <td>Midwest</td>
          <td>-89.412075</td>
          <td>45.636623</td>
          <td>Rhinelander (WI)</td>
        </tr>
        <tr>
          <th>160</th>
          <td>12320</td>
          <td>Wilmington, DE: New Castle</td>
          <td>New Castle</td>
          <td>Wilmington</td>
          <td>DE</td>
          <td>South</td>
          <td>-80.347009</td>
          <td>41.003672</td>
          <td>Wilmington (DE)</td>
        </tr>
        <tr>
          <th>322</th>
          <td>15401</td>
          <td>Texarkana, AR: Texarkana Regional-Webb Field</td>
          <td>Texarkana Regional-Webb Field</td>
          <td>Texarkana</td>
          <td>AR</td>
          <td>South</td>
          <td>-94.037692</td>
          <td>33.441795</td>
          <td>Texarkana (AR)</td>
        </tr>
        <tr>
          <th>31</th>
          <td>10577</td>
          <td>Binghamton, NY: Greater Binghamton/Edwin A. Li...</td>
          <td>Greater Binghamton/Edwin A. Link Field</td>
          <td>Binghamton</td>
          <td>NY</td>
          <td>Northeast</td>
          <td>-75.914341</td>
          <td>42.096968</td>
          <td>Binghamton (NY)</td>
        </tr>
        <tr>
          <th>212</th>
          <td>13303</td>
          <td>Miami, FL: Miami International</td>
          <td>Miami International</td>
          <td>Miami</td>
          <td>FL</td>
          <td>South</td>
          <td>-80.376289</td>
          <td>25.755338</td>
          <td>Miami (FL)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # check duplicates in "City_State"
    dups = df_lookup['City_State'].value_counts()
    dups = dups[dups != 1]
    
    dups




.. parsed-literal::
    :class: myliteral

    Houston (TX)       3
    Chicago (IL)       2
    Washington (DC)    2
    New York (NY)      2
    Name: City_State, dtype: int64



.. code:: python

    # create hash-table for airport name lookup
    hash_airport = df_lookup.set_index('Code')['Airport'].to_dict()
    pprint({k: hash_airport[k] for k in hash_airport.keys()[:5]})


.. parsed-literal::
    :class: myliteral

    {10245: 'King Salmon Airport',
     10754: 'Wiley Post/Will Rogers Memorial',
     11267: 'James M Cox/Dayton International',
     13830: 'Kahului Airport',
     14696: 'South Bend International'}
    

.. code:: python

    # check duplicates in "City_State"
    for dup in dups.index:
        print dup
        for i in df_lookup[df_lookup['City_State'] == dup].Code:
            print "    (Code = {:6}) Airport = {}".format((df_data['ORIGIN_AIRPORT_ID'] == i).sum(), hash_airport[i])


.. parsed-literal::
    :class: myliteral

    Houston (TX)
        (Code =      1) Airport = Ellington
        (Code = 171407) Airport = William P Hobby
        (Code = 478137) Airport = George Bush Intercontinental/Houston
    Chicago (IL)
        (Code = 264913) Airport = Chicago Midway International
        (Code = 853523) Airport = Chicago O'Hare International
    Washington (DC)
        (Code = 230760) Airport = Ronald Reagan Washington National
        (Code = 135697) Airport = Washington Dulles International
    New York (NY)
        (Code = 302634) Airport = John F. Kennedy International
        (Code = 314816) Airport = LaGuardia
    

Again, kinda hacky, but will create manual replacement on these
duplicates using the "cleaner" below

.. code:: python

    cleaner = [
        ('Houston (TX) [Ell]', 'Ellington'), 
        ('Houston (TX) [WP.Hobby]', 'William P Hobby'), 
        ('Houston (TX) [G.Bush]',  'George Bush Intercontinental/Houston'), 
        ('Chicago (IL) [Midway]',   'Chicago Midway International'),
        ("Chicago (IL) [O'Hare]",   "Chicago O'Hare International"),
        ('Washington (DC) [R.Reagan]',   'Ronald Reagan Washington National'),
        ('Washington (DC) [W.Dulles]',   'Washington Dulles International'),
        ("New York (NY) [JFK]",   "John F. Kennedy International"),
        ("New York (NY) [Lag]",   "LaGuardia"),
    ]
    
    for _replace, _airport in cleaner:
        df_lookup.loc[df_lookup['Airport'] == _airport, 'City_State'] = _replace
    
    # check duplicates are removed
    assert np.all(df_lookup['City_State'].value_counts() == 1)

All done. Save dataframe on disk
================================

-  We have created our *enhanced* lookup table.

-  Let's save this on disk for later analysis.

.. code:: python

    print df_lookup.shape
    df_lookup.sample(10).sort_index()


.. parsed-literal::
    :class: myliteral

    (334, 9)
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Code</th>
          <th>Description</th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
          <th>Region</th>
          <th>lat</th>
          <th>lon</th>
          <th>City_State</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>12</th>
          <td>10208</td>
          <td>Augusta, GA: Augusta Regional at Bush Field</td>
          <td>Augusta Regional at Bush Field</td>
          <td>Augusta</td>
          <td>GA</td>
          <td>South</td>
          <td>-81.965064</td>
          <td>33.372302</td>
          <td>Augusta (GA)</td>
        </tr>
        <tr>
          <th>25</th>
          <td>10434</td>
          <td>Scranton/Wilkes-Barre, PA: Wilkes Barre Scrant...</td>
          <td>Wilkes Barre Scranton International</td>
          <td>Scranton/Wilkes-Barre</td>
          <td>PA</td>
          <td>Northeast</td>
          <td>-75.722549</td>
          <td>41.337135</td>
          <td>Scranton/Wilkes-Barre (PA)</td>
        </tr>
        <tr>
          <th>42</th>
          <td>10721</td>
          <td>Boston, MA: Logan International</td>
          <td>Logan International</td>
          <td>Boston</td>
          <td>MA</td>
          <td>Northeast</td>
          <td>-77.030034</td>
          <td>38.893329</td>
          <td>Boston (MA)</td>
        </tr>
        <tr>
          <th>112</th>
          <td>11624</td>
          <td>Key West, FL: Key West International</td>
          <td>Key West International</td>
          <td>Key West</td>
          <td>FL</td>
          <td>South</td>
          <td>-81.756229</td>
          <td>24.554654</td>
          <td>Key West (FL)</td>
        </tr>
        <tr>
          <th>120</th>
          <td>11721</td>
          <td>Flint, MI: Bishop International</td>
          <td>Bishop International</td>
          <td>Flint</td>
          <td>MI</td>
          <td>Midwest</td>
          <td>-1.516735</td>
          <td>52.407220</td>
          <td>Flint (MI)</td>
        </tr>
        <tr>
          <th>154</th>
          <td>12255</td>
          <td>Hays, KS: Hays Regional</td>
          <td>Hays Regional</td>
          <td>Hays</td>
          <td>KS</td>
          <td>Midwest</td>
          <td>-99.273037</td>
          <td>38.845476</td>
          <td>Hays (KS)</td>
        </tr>
        <tr>
          <th>205</th>
          <td>13241</td>
          <td>Meridian, MS: Key Field</td>
          <td>Key Field</td>
          <td>Meridian</td>
          <td>MS</td>
          <td>South</td>
          <td>-0.833914</td>
          <td>53.690169</td>
          <td>Meridian (MS)</td>
        </tr>
        <tr>
          <th>230</th>
          <td>13577</td>
          <td>Myrtle Beach, SC: Myrtle Beach International</td>
          <td>Myrtle Beach International</td>
          <td>Myrtle Beach</td>
          <td>SC</td>
          <td>South</td>
          <td>-78.929060</td>
          <td>33.680641</td>
          <td>Myrtle Beach (SC)</td>
        </tr>
        <tr>
          <th>277</th>
          <td>14635</td>
          <td>Fort Myers, FL: Southwest Florida International</td>
          <td>Southwest Florida International</td>
          <td>Fort Myers</td>
          <td>FL</td>
          <td>South</td>
          <td>-80.376289</td>
          <td>25.755338</td>
          <td>Fort Myers (FL)</td>
        </tr>
        <tr>
          <th>285</th>
          <td>14709</td>
          <td>Deadhorse, AK: Deadhorse Airport</td>
          <td>Deadhorse Airport</td>
          <td>Deadhorse</td>
          <td>AK</td>
          <td>West</td>
          <td>-148.465705</td>
          <td>70.195843</td>
          <td>Deadhorse (AK)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_lookup.to_csv('df_lookup.csv',index=False)
