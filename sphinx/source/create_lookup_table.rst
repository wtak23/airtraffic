Create Lookup Table
"""""""""""""""""""

Aim of notebook
===============

-  The [airport traffic
   dataset]((http://www.transtats.bts.gov/DL\_SelectFields.asp?Table\_ID=236&DB\_Short\_Name=On-Time)
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

    from util import load_airport_data
    df_data = load_airport_data()


.. parsed-literal::
    :class: myliteral

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

    (5652973, 7)
    



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
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>4</td>
          <td>3</td>
          <td>14570</td>
          <td>13930</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>5</td>
          <td>4</td>
          <td>13930</td>
          <td>14057</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>6</td>
          <td>5</td>
          <td>13930</td>
          <td>14057</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>7</td>
          <td>6</td>
          <td>13930</td>
          <td>14057</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>8</td>
          <td>7</td>
          <td>13930</td>
          <td>14057</td>
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
    There are 319 unique airport-codes in our dataset
    

Let's filter/drop the rows/records that we do not need in our analysis

.. code:: python

    # only keep the items in the main dataframe
    _mask = df_lookup['Code'].isin( uniq_id )
    df_lookup = df_lookup[ _mask ].reset_index(drop=True)
    
    print df_lookup.shape
    df_lookup.head(10)


.. parsed-literal::
    :class: myliteral

    (319, 2)
    



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

    (319, 5)
    



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



Add airport latitude and longitude information using Google geocoder
--------------------------------------------------------------------

This information will be useful especially when making visualization
plots

.. code:: python

    import geocoder
    from util import print_time
    
    t = time.time()
    lat,lon = [],[]
    
    n_items = df_lookup.shape[0]
    for i,airport in enumerate(df_lookup['Airport']):
        if i%20==0: 
             print '({:3} out of {})'.format(i,n_items),print_time(t)
        loc = geocoder.google(airport)
        
        if loc is not None:
            lon.append(loc.lng)
            lat.append(loc.lat)
        else:
            # lookup failed
            lon.append(None)
            lat.append(None)
            
    # add as new columns
    df_lookup['lat'] = lat
    df_lookup['lon'] = lon
    
    n_nans = df_lookup['lat'].isnull().sum(axis=0)
    print "-- {} NANs out {} ({:.2f}%) --".format(n_nans,n_items,n_nans/float(n_items)*100)


.. parsed-literal::
    :class: myliteral

    (  0 out of 319) Elapsed time:  0.00 seconds
    ( 20 out of 319) Elapsed time:  1.52 seconds
    

::


    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-52-364727c36938> in <module>()
          9     if i%20==0:
         10          print '({:3} out of {})'.format(i,n_items),print_time(t)
    ---> 11     loc = geocoder.google(airport)
         12 
         13     if loc is not None:
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\geocoder\api.pyc in google(location, **kwargs)
        184         > elevation
        185     """
    --> 186     return get(location, provider='google', **kwargs)
        187 
        188 
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\geocoder\api.pyc in get(location, **kwargs)
        150         if method not in options[provider]:
        151             raise ValueError("Invalid method")
    --> 152     return options[provider][method](location, **kwargs)
        153 
        154 
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\geocoder\google.pyc in __init__(self, location, **kwargs)
         59         if self.client and self.client_secret:
         60             self._encode_params(**kwargs)
    ---> 61         self._initialize(**kwargs)
         62 
         63     def _encode_params(self, **kwargs):
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\geocoder\base.pyc in _initialize(self, **kwargs)
        122         self.content = None
        123         self.encoding = kwargs.get('encoding', 'utf-8')
    --> 124         self._connect(url=self.url, params=self.params, **kwargs)
        125         ###
        126         try:
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\geocoder\base.pyc in _connect(self, **kwargs)
         93                 headers=self.headers,
         94                 timeout=self.timeout,
    ---> 95                 proxies=self.proxies
         96             )
         97             self.status_code = r.status_code
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\geocoder\base.pyc in rate_limited_get(url, **kwargs)
         71     @staticmethod
         72     def rate_limited_get(url, **kwargs):
    ---> 73         return requests.get(url, **kwargs)
         74 
         75     def _get_api_key(self, base_key, **kwargs):
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\api.pyc in get(url, params, **kwargs)
         68 
         69     kwargs.setdefault('allow_redirects', True)
    ---> 70     return request('get', url, params=params, **kwargs)
         71 
         72 
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\api.pyc in request(method, url, **kwargs)
         54     # cases, and look like a memory leak in others.
         55     with sessions.Session() as session:
    ---> 56         return session.request(method=method, url=url, **kwargs)
         57 
         58 
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\sessions.pyc in request(self, method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
        486         }
        487         send_kwargs.update(settings)
    --> 488         resp = self.send(prep, **send_kwargs)
        489 
        490         return resp
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\sessions.pyc in send(self, request, **kwargs)
        607 
        608         # Send the request
    --> 609         r = adapter.send(request, **kwargs)
        610 
        611         # Total elapsed time of the request (approximately)
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\adapters.pyc in send(self, request, stream, timeout, verify, cert, proxies)
        421                     decode_content=False,
        422                     retries=self.max_retries,
    --> 423                     timeout=timeout
        424                 )
        425 
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\packages\urllib3\connectionpool.pyc in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, **response_kw)
        592                                                   timeout=timeout_obj,
        593                                                   body=body, headers=headers,
    --> 594                                                   chunked=chunked)
        595 
        596             # If we're going to release the connection in ``finally:``, then
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\packages\urllib3\connectionpool.pyc in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
        382         try:
        383             try:  # Python 2.7, use buffering of HTTP responses
    --> 384                 httplib_response = conn.getresponse(buffering=True)
        385             except TypeError:  # Python 2.6 and older, Python 3
        386                 try:
    

    C:\Users\takanori\Anaconda2\lib\httplib.pyc in getresponse(self, buffering)
       1134 
       1135         try:
    -> 1136             response.begin()
       1137             assert response.will_close != _UNKNOWN
       1138             self.__state = _CS_IDLE
    

    C:\Users\takanori\Anaconda2\lib\httplib.pyc in begin(self)
        451         # read until we get a non-100 response
        452         while True:
    --> 453             version, status, reason = self._read_status()
        454             if status != CONTINUE:
        455                 break
    

    C:\Users\takanori\Anaconda2\lib\httplib.pyc in _read_status(self)
        407     def _read_status(self):
        408         # Initialize with Simple-Response defaults
    --> 409         line = self.fp.readline(_MAXLINE + 1)
        410         if len(line) > _MAXLINE:
        411             raise LineTooLong("header line")
    

    C:\Users\takanori\Anaconda2\lib\socket.pyc in readline(self, size)
        478             while True:
        479                 try:
    --> 480                     data = self._sock.recv(self._rbufsize)
        481                 except error, e:
        482                     if e.args[0] == EINTR:
    

    C:\Users\takanori\AppData\Roaming\Python\Python27\site-packages\requests\packages\urllib3\contrib\pyopenssl.pyc in recv(self, *args, **kwargs)
        244         except OpenSSL.SSL.WantReadError:
        245             rd, wd, ed = select.select(
    --> 246                 [self.socket], [], [], self.socket.gettimeout())
        247             if not rd:
        248                 raise timeout('The read operation timed out')
    

    KeyboardInterrupt: 


Some lookup failed...but most succeeded

argh..hit daily google geocoding quota limit...come back later



.. code:: python

    # let's do lookup based city and state
    for i,(city,state) in enumerate(df_lookup['City'],df_lookup['State']):
        loc = geocoder.google(city+' '+state)
        if loc is None:
            # if airport lookup failed, lookup based on city and state info
            city  = df_lookup['City'].ix[i]
            state = df_lookup['State'].ix[i]
            loc = geocoder.google(city+' '+state)
    
        if loc is None:
            # even if that fails, append None for now
            lon.append(None)
            lat.append(None)
        else:
            # else, append the identified lat/lon informatino
            lon.append(loc.lng)
            lat.append(loc.lat)
