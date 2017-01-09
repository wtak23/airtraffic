
Table of Contents
=================

.. raw:: html

   <p>

.. raw:: html

   <div class="lev1 toc-item">

1  Study the "carrier" spreadsheet

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

1.1  sort out the "nan" values

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

1.2  Filter away nans from the DataFrame

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

1.3  Realized some Code is treated as int...convert to string

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

1.4  What's the deal with the (1) appended to some of the entries?

.. raw:: html

   </div>

.. raw:: html

   <div class="lev1 toc-item">

2  Study airports spreadsheet

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

2.1  Study nans

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

2.2  Filter out non-USA airports

.. raw:: html

   </div>

.. raw:: html

   <div class="lev1 toc-item">

3  Todo list

.. raw:: html

   </div>

.. raw:: html

   <div class="lev1 toc-item">

4  Study "airports" state distribution

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

4.1  Plot bubble markers for all airports

.. raw:: html

   </div>

.. raw:: html

   <div class="lev2 toc-item">

4.2  Take a closer look at Michigan, my home state

.. raw:: html

   </div>

.. code:: python

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from pprint import pprint
    import os
    os.getcwd()
    
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    
    # limit output to avoid cluttering screen
    pd.options.display.max_rows = 20


Study the "carrier" spreadsheet
===============================

.. code:: python

    df_carr = pd.read_excel('../data/carriers.xls')
    print "df_carr.shape = ",df_carr.shape
    print df_carr.columns.tolist()
    df_carr.head(n=15)


.. parsed-literal::

    df_carr.shape =  (2982, 2)
    [u'Code', u'Description']
    



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
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>1</th>
          <td>02Q</td>
          <td>Titan Airways</td>
        </tr>
        <tr>
          <th>2</th>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>3</th>
          <td>04Q</td>
          <td>Tradewind Aviation</td>
        </tr>
        <tr>
          <th>4</th>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>5</th>
          <td>05Q</td>
          <td>Comlux Aviation, AG</td>
        </tr>
        <tr>
          <th>6</th>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>7</th>
          <td>06Q</td>
          <td>Master Top Linhas Aereas Ltd.</td>
        </tr>
        <tr>
          <th>8</th>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>9</th>
          <td>07Q</td>
          <td>Flair Airlines Ltd.</td>
        </tr>
        <tr>
          <th>10</th>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>11</th>
          <td>09Q</td>
          <td>Swift Air, LLC</td>
        </tr>
        <tr>
          <th>12</th>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>13</th>
          <td>0BQ</td>
          <td>DCA</td>
        </tr>
        <tr>
          <th>14</th>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



sort out the "nan" values
-------------------------

.. code:: python

    df_carr.isnull()




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
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>1</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>2</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>3</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>4</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>5</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>6</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>7</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>8</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>9</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2972</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>2973</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>2974</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>2975</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>2976</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>2977</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>2978</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>2979</th>
          <td>False</td>
          <td>False</td>
        </tr>
        <tr>
          <th>2980</th>
          <td>True</td>
          <td>True</td>
        </tr>
        <tr>
          <th>2981</th>
          <td>False</td>
          <td>False</td>
        </tr>
      </tbody>
    </table>
    <p>2982 rows × 2 columns</p>
    </div>



... appears like every-other rows are nans

.. code:: python

    df_carr.isnull().sum()




.. parsed-literal::

    Code           1492
    Description    1491
    dtype: int64



... one airline has extra nan values in the "Code" column.... anything
special about that entry?

.. code:: python

    # which record/row has Code NaN 
    _idx = np.where(df_carr.isnull().sum(axis=1) == 1)[0][0]
    
    df_carr.ix[_idx]




.. parsed-literal::

    Code                               NaN
    Description    North American Airlines
    Name: 1747, dtype: object



...so nothing exactly special looking...

Filter away nans from the DataFrame
-----------------------------------

-  remove row with *any* nans

.. code:: python

    df_carr = df_carr[~df_carr.isnull().any(axis=1)]
    print "df_carr.shape = ",df_carr.shape


.. parsed-literal::

    df_carr.shape =  (1490, 2)
    

.. code:: python

    # all record appears to be unique
    print df_carr['Code'].unique().shape
    print df_carr['Description'].unique().shape


.. parsed-literal::

    (1490L,)
    (1490L,)
    

.. code:: python

    df_carr.head(n=10)




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
          <th>1</th>
          <td>02Q</td>
          <td>Titan Airways</td>
        </tr>
        <tr>
          <th>3</th>
          <td>04Q</td>
          <td>Tradewind Aviation</td>
        </tr>
        <tr>
          <th>5</th>
          <td>05Q</td>
          <td>Comlux Aviation, AG</td>
        </tr>
        <tr>
          <th>7</th>
          <td>06Q</td>
          <td>Master Top Linhas Aereas Ltd.</td>
        </tr>
        <tr>
          <th>9</th>
          <td>07Q</td>
          <td>Flair Airlines Ltd.</td>
        </tr>
        <tr>
          <th>11</th>
          <td>09Q</td>
          <td>Swift Air, LLC</td>
        </tr>
        <tr>
          <th>13</th>
          <td>0BQ</td>
          <td>DCA</td>
        </tr>
        <tr>
          <th>15</th>
          <td>0CQ</td>
          <td>ACM AIR CHARTER GmbH</td>
        </tr>
        <tr>
          <th>17</th>
          <td>0FQ</td>
          <td>Maine Aviation Aircraft Charter, LLC</td>
        </tr>
        <tr>
          <th>19</th>
          <td>0GQ</td>
          <td>Inter Island Airways, d/b/a Inter Island Air</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # reset index
    df_carr.reset_index(drop=True,inplace=True)

Realized some *Code* is treated as int...convert to string
----------------------------------------------------------

-  d

.. code:: python

    # convert columns to unicode (realized some elements are treated as 'int', which messes up some string tests below
    df_carr['Code'] = df_carr['Code'].apply(unicode)
    df_carr['Description'] = df_carr['Description'].apply(unicode)
    #df_carr['Code'] = df_carr['Code'].apply(str)

.. code:: python

    df_carr.dtypes




.. parsed-literal::

    Code           object
    Description    object
    dtype: object



What's the deal with the (1) appended to some of the entries?
-------------------------------------------------------------


.. code:: python

    mask1 = df_carr['Code'].str.endswith('(1)').astype(bool)
    mask2 = df_carr['Description'].str.endswith('(1)').astype(bool)
    
    df_carr[mask1].head()
    
    




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
          <th>66</th>
          <td>7G (1)</td>
          <td>Bellair Inc. (1)</td>
        </tr>
        <tr>
          <th>130</th>
          <td>ACT</td>
          <td>Air Central Inc. (1)</td>
        </tr>
        <tr>
          <th>231</th>
          <td>ASU</td>
          <td>Air South (1)</td>
        </tr>
        <tr>
          <th>292</th>
          <td>BHQ</td>
          <td>Turks Air Ltd. (1)</td>
        </tr>
        <tr>
          <th>407</th>
          <td>CSN</td>
          <td>Casino Airlines (1)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_carr[mask2].head()




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
          <th>66</th>
          <td>7G (1)</td>
          <td>Bellair Inc. (1)</td>
        </tr>
        <tr>
          <th>130</th>
          <td>ACT</td>
          <td>Air Central Inc. (1)</td>
        </tr>
        <tr>
          <th>231</th>
          <td>ASU</td>
          <td>Air South (1)</td>
        </tr>
        <tr>
          <th>292</th>
          <td>BHQ</td>
          <td>Turks Air Ltd. (1)</td>
        </tr>
        <tr>
          <th>407</th>
          <td>CSN</td>
          <td>Casino Airlines (1)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # more informative to print row just before...
    
    def interleave_index(mask):
        ind = np.where(mask)[0]
        ind = np.hstack((ind,ind - 1))
        ind.sort()
        return ind
    
    df_carr.iloc[interleave_index(mask1)]




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
          <th>33</th>
          <td>4E</td>
          <td>Tanana Air Service</td>
        </tr>
        <tr>
          <th>34</th>
          <td>4E (1)</td>
          <td>British Airtours Limited</td>
        </tr>
        <tr>
          <th>36</th>
          <td>4M</td>
          <td>LAN Argentina</td>
        </tr>
        <tr>
          <th>37</th>
          <td>4M (1)</td>
          <td>Lan Dominica</td>
        </tr>
        <tr>
          <th>40</th>
          <td>4S</td>
          <td>Sol Air (Aero Hunduras)</td>
        </tr>
        <tr>
          <th>41</th>
          <td>4S (1)</td>
          <td>Conner Air Lines Inc.</td>
        </tr>
        <tr>
          <th>49</th>
          <td>5G</td>
          <td>Skyservice Airlines, Inc.</td>
        </tr>
        <tr>
          <th>50</th>
          <td>5G (1)</td>
          <td>Queen Air</td>
        </tr>
        <tr>
          <th>65</th>
          <td>7G</td>
          <td>MK Airlines Ltd.</td>
        </tr>
        <tr>
          <th>66</th>
          <td>7G (1)</td>
          <td>Bellair Inc. (1)</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>1348</th>
          <td>VX</td>
          <td>Virgin America</td>
        </tr>
        <tr>
          <th>1349</th>
          <td>VX (1)</td>
          <td>Aces Airlines</td>
        </tr>
        <tr>
          <th>1355</th>
          <td>WA</td>
          <td>Worldwide Airlines Services</td>
        </tr>
        <tr>
          <th>1356</th>
          <td>WA (1)</td>
          <td>Western Air Lines Inc.</td>
        </tr>
        <tr>
          <th>1395</th>
          <td>WS</td>
          <td>Westjet</td>
        </tr>
        <tr>
          <th>1396</th>
          <td>WS (1)</td>
          <td>Suncoast Airlines Inc.</td>
        </tr>
        <tr>
          <th>1466</th>
          <td>Z3</td>
          <td>PM Air, LLC</td>
        </tr>
        <tr>
          <th>1467</th>
          <td>Z3 (1)</td>
          <td>Promech</td>
        </tr>
        <tr>
          <th>1486</th>
          <td>ZX</td>
          <td>Air Georgian</td>
        </tr>
        <tr>
          <th>1487</th>
          <td>ZX (1)</td>
          <td>Airbc Ltd.</td>
        </tr>
      </tbody>
    </table>
    <p>114 rows × 2 columns</p>
    </div>



.. code:: python

    df_carr.iloc[interleave_index(mask2)]




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
          <th>65</th>
          <td>7G</td>
          <td>MK Airlines Ltd.</td>
        </tr>
        <tr>
          <th>66</th>
          <td>7G (1)</td>
          <td>Bellair Inc. (1)</td>
        </tr>
        <tr>
          <th>129</th>
          <td>ACS</td>
          <td>Alamo Commuter Airlines</td>
        </tr>
        <tr>
          <th>130</th>
          <td>ACT</td>
          <td>Air Central Inc. (1)</td>
        </tr>
        <tr>
          <th>230</th>
          <td>AST</td>
          <td>Astro Airways</td>
        </tr>
        <tr>
          <th>231</th>
          <td>ASU</td>
          <td>Air South (1)</td>
        </tr>
        <tr>
          <th>291</th>
          <td>BHO</td>
          <td>Bighorn Airways Inc.</td>
        </tr>
        <tr>
          <th>292</th>
          <td>BHQ</td>
          <td>Turks Air Ltd. (1)</td>
        </tr>
        <tr>
          <th>406</th>
          <td>CSM</td>
          <td>Chisum Flying Service</td>
        </tr>
        <tr>
          <th>407</th>
          <td>CSN</td>
          <td>Casino Airlines (1)</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>1062</th>
          <td>RC</td>
          <td>Republic Airlines Inc.</td>
        </tr>
        <tr>
          <th>1063</th>
          <td>RCA</td>
          <td>Mid-South Aviation Inc. (1)</td>
        </tr>
        <tr>
          <th>1092</th>
          <td>ROE</td>
          <td>Roederer Aviation Inc.</td>
        </tr>
        <tr>
          <th>1093</th>
          <td>ROQ</td>
          <td>Aero Uruguay (1)</td>
        </tr>
        <tr>
          <th>1304</th>
          <td>UP</td>
          <td>Bahamasair Holding Limited</td>
        </tr>
        <tr>
          <th>1305</th>
          <td>UR</td>
          <td>Empire Airlines Inc. (1)</td>
        </tr>
        <tr>
          <th>1401</th>
          <td>WTA</td>
          <td>Westates Airlines</td>
        </tr>
        <tr>
          <th>1402</th>
          <td>WV</td>
          <td>Air South Inc. (1)</td>
        </tr>
        <tr>
          <th>1437</th>
          <td>XBZ</td>
          <td>Air Natl Aircraft Sal &amp; Ser</td>
        </tr>
        <tr>
          <th>1438</th>
          <td>XC</td>
          <td>Air Caribbean (1)</td>
        </tr>
      </tbody>
    </table>
    <p>38 rows × 2 columns</p>
    </div>



Study *airports* spreadsheet
============================

.. code:: python

    df_airports = pd.read_excel('../data/airports new.xlt')

.. code:: python

    print "df_airports.shape = ",df_airports.shape
    print df_airports.dtypes


.. parsed-literal::

    df_airports.shape =  (3376, 7)
    iata        object
    airport     object
    city        object
    state       object
    country     object
    lat        float64
    long       float64
    dtype: object
    

.. code:: python

    df_airports.head(n=10)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>iata</th>
          <th>airport</th>
          <th>city</th>
          <th>state</th>
          <th>country</th>
          <th>lat</th>
          <th>long</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>00M</td>
          <td>Thigpen</td>
          <td>Bay Springs</td>
          <td>MS</td>
          <td>USA</td>
          <td>31.953765</td>
          <td>-89.234505</td>
        </tr>
        <tr>
          <th>1</th>
          <td>00R</td>
          <td>Livingston Municipal</td>
          <td>Livingston</td>
          <td>TX</td>
          <td>USA</td>
          <td>30.685861</td>
          <td>-95.017928</td>
        </tr>
        <tr>
          <th>2</th>
          <td>00V</td>
          <td>Meadow Lake</td>
          <td>Colorado Springs</td>
          <td>CO</td>
          <td>USA</td>
          <td>38.945749</td>
          <td>-104.569893</td>
        </tr>
        <tr>
          <th>3</th>
          <td>01G</td>
          <td>Perry-Warsaw</td>
          <td>Perry</td>
          <td>NY</td>
          <td>USA</td>
          <td>42.741347</td>
          <td>-78.052081</td>
        </tr>
        <tr>
          <th>4</th>
          <td>01J</td>
          <td>Hilliard Airpark</td>
          <td>Hilliard</td>
          <td>FL</td>
          <td>USA</td>
          <td>30.688012</td>
          <td>-81.905944</td>
        </tr>
        <tr>
          <th>5</th>
          <td>01M</td>
          <td>Tishomingo County</td>
          <td>Belmont</td>
          <td>MS</td>
          <td>USA</td>
          <td>34.491667</td>
          <td>-88.201111</td>
        </tr>
        <tr>
          <th>6</th>
          <td>02A</td>
          <td>Gragg-Wade</td>
          <td>Clanton</td>
          <td>AL</td>
          <td>USA</td>
          <td>32.850487</td>
          <td>-86.611453</td>
        </tr>
        <tr>
          <th>7</th>
          <td>02C</td>
          <td>Capitol</td>
          <td>Brookfield</td>
          <td>WI</td>
          <td>USA</td>
          <td>43.087510</td>
          <td>-88.177869</td>
        </tr>
        <tr>
          <th>8</th>
          <td>02G</td>
          <td>Columbiana County</td>
          <td>East Liverpool</td>
          <td>OH</td>
          <td>USA</td>
          <td>40.673313</td>
          <td>-80.641406</td>
        </tr>
        <tr>
          <th>9</th>
          <td>03D</td>
          <td>Memphis Memorial</td>
          <td>Memphis</td>
          <td>MO</td>
          <td>USA</td>
          <td>40.447259</td>
          <td>-92.226961</td>
        </tr>
      </tbody>
    </table>
    </div>



Study nans
----------

.. code:: python

    # any nans?
    df_airports.isnull().sum()




.. parsed-literal::

    iata        0
    airport     0
    city       12
    state      12
    country     0
    lat         0
    long        0
    dtype: int64



.. code:: python

    # do the nans occur at the same place?
    #| yes
    np.alltrue(
        np.where(df_airports['city'].isnull())[0] == \
        np.where(df_airports['state'].isnull())[0]
    )




.. parsed-literal::

    True



.. code:: python

    # anything special about the records with unknown city/state?
    df_airports[df_airports.isnull().any(axis=1)]




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>iata</th>
          <th>airport</th>
          <th>city</th>
          <th>state</th>
          <th>country</th>
          <th>lat</th>
          <th>long</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1136</th>
          <td>CLD</td>
          <td>MC Clellan-Palomar Airport</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>33.127231</td>
          <td>-117.278727</td>
        </tr>
        <tr>
          <th>1715</th>
          <td>HHH</td>
          <td>Hilton Head</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>32.224384</td>
          <td>-80.697629</td>
        </tr>
        <tr>
          <th>2251</th>
          <td>MIB</td>
          <td>Minot AFB</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>48.415769</td>
          <td>-101.358039</td>
        </tr>
        <tr>
          <th>2312</th>
          <td>MQT</td>
          <td>Marquette County Airport</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>46.353639</td>
          <td>-87.395361</td>
        </tr>
        <tr>
          <th>2752</th>
          <td>RCA</td>
          <td>Ellsworth AFB</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>44.145094</td>
          <td>-103.103567</td>
        </tr>
        <tr>
          <th>2759</th>
          <td>RDR</td>
          <td>Grand Forks AFB</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>47.961167</td>
          <td>-97.401167</td>
        </tr>
        <tr>
          <th>2794</th>
          <td>ROP</td>
          <td>Prachinburi</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>Thailand</td>
          <td>14.078333</td>
          <td>101.378334</td>
        </tr>
        <tr>
          <th>2795</th>
          <td>ROR</td>
          <td>Babelthoup/Koror</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>Palau</td>
          <td>7.367222</td>
          <td>134.544167</td>
        </tr>
        <tr>
          <th>2900</th>
          <td>SCE</td>
          <td>University Park</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>40.851206</td>
          <td>-77.846302</td>
        </tr>
        <tr>
          <th>2964</th>
          <td>SKA</td>
          <td>Fairchild AFB</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>USA</td>
          <td>47.615058</td>
          <td>-117.655803</td>
        </tr>
        <tr>
          <th>3001</th>
          <td>SPN</td>
          <td>Tinian International Airport</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>N Mariana Islands</td>
          <td>14.996111</td>
          <td>145.621384</td>
        </tr>
        <tr>
          <th>3355</th>
          <td>YAP</td>
          <td>Yap International</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>Federated States of Micronesia</td>
          <td>9.516700</td>
          <td>138.100000</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # most of the data are from USA...the 4 cases corresponds to the NANs above
    df_airports['country'].value_counts(0)




.. parsed-literal::

    USA                               3372
    Palau                                1
    N Mariana Islands                    1
    Thailand                             1
    Federated States of Micronesia       1
    Name: country, dtype: int64



Filter out non-USA airports
---------------------------

.. code:: python

    df_airports = df_airports.query('country == "USA"')

.. code:: python

    df_airports.country.unique()




.. parsed-literal::

    array([u'USA'], dtype=object)



Study "airports" state distribution
===================================

.. code:: python

    df_state = df_airports['state'].value_counts()
    df_state = df_state.reset_index()
    df_state.columns = ['state','counts']
    df_state.T




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
          <th>1</th>
          <th>2</th>
          <th>3</th>
          <th>4</th>
          <th>5</th>
          <th>6</th>
          <th>7</th>
          <th>8</th>
          <th>9</th>
          <th>...</th>
          <th>46</th>
          <th>47</th>
          <th>48</th>
          <th>49</th>
          <th>50</th>
          <th>51</th>
          <th>52</th>
          <th>53</th>
          <th>54</th>
          <th>55</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>state</th>
          <td>AK</td>
          <td>TX</td>
          <td>CA</td>
          <td>OK</td>
          <td>FL</td>
          <td>OH</td>
          <td>NY</td>
          <td>GA</td>
          <td>MI</td>
          <td>MN</td>
          <td>...</td>
          <td>NH</td>
          <td>VT</td>
          <td>PR</td>
          <td>RI</td>
          <td>DE</td>
          <td>VI</td>
          <td>CQ</td>
          <td>AS</td>
          <td>GU</td>
          <td>DC</td>
        </tr>
        <tr>
          <th>counts</th>
          <td>263</td>
          <td>209</td>
          <td>205</td>
          <td>102</td>
          <td>100</td>
          <td>100</td>
          <td>97</td>
          <td>97</td>
          <td>94</td>
          <td>89</td>
          <td>...</td>
          <td>14</td>
          <td>13</td>
          <td>11</td>
          <td>6</td>
          <td>5</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
        </tr>
      </tbody>
    </table>
    <p>2 rows × 56 columns</p>
    </div>



.. code:: python

    # define data/trace object
    trace = dict(
            type='choropleth',
            #colorscale = scl,
            #autocolorscale = False,
            autocolorscale = True,
            locations = df_state['state'],
            z = df_state['counts'],
            locationmode = 'USA-states',
            #text = df['text'],
            marker = dict(line = dict (color = 'rgb(255,255,255)',width = 2) ),
            colorbar = dict(title = "counts")
    )
    data = [trace]
    
    # define layout object
    geo = dict(scope='usa',
               projection=dict( type='albers usa' ),
               showlakes = True,
               lakecolor = 'rgb(255, 255, 255)')
    layout = dict(geo=geo,title = 'State Frequency chart (hover over for number)')
    
    fig = dict( data=data, layout=layout )
    # py.iplot( fig, filename='d3-cloropleth-map' )
    
    import plotly.plotly as py

.. code:: python

    py.iplot( fig, filename='spotify-tmp1', sharing = 'secret')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1345.embed?share_key=HXSygiLDpJTyDMXMN7lIa6" height="525px" width="100%"></iframe>



From the above plot, it looks like the number of aiports in a state is
proportional to the land-area of the state...

Plot bubble markers for all airports
------------------------------------

This will give an idea of the airport distribution around the country

.. code:: python

    data = [ dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_airports['long'],
            lat = df_airports['lat'],
            text = df_airports['airport'] + ' ' + df_airports['city'],
            mode = 'markers',
            marker = dict( 
                size = 5, 
                opacity = 0.5,
                reversescale = True,
                symbol = 'circle',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                autocolorscale = True,
            ))]
    
    layout = dict(
            title = 'Airports in the United States<br>(Scroll mouse to zoom)',
            colorbar = True,   
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                showlakes = True,     
            ),
        )
    
    fig = dict( data=data, layout=layout )
    py.iplot( fig, filename='spotify-tmp2', sharing = 'secret',validate=False)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1349.embed?share_key=lPM6X5p9K50zOVqNgTUPqg" height="525px" width="100%"></iframe>



**Some personal remarks** - airport-density is high in the Northeastern
regions, which was expected, as these are economically developed and
densely populated region. - airport-density in the Western area is low
outside of California, which was again expected. - I did not expect
there are

Take a closer look at Michigan, my home state
---------------------------------------------

-  https://plot.ly/python/bubble-maps/

.. code:: python

    df_airports.query('state=="MI"').head(5)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>iata</th>
          <th>airport</th>
          <th>city</th>
          <th>state</th>
          <th>country</th>
          <th>lat</th>
          <th>long</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>23</th>
          <td>07G</td>
          <td>Fitch H Beach</td>
          <td>Charlotte</td>
          <td>MI</td>
          <td>USA</td>
          <td>42.574509</td>
          <td>-84.811431</td>
        </tr>
        <tr>
          <th>45</th>
          <td>0D1</td>
          <td>South Haven Municipal</td>
          <td>South Haven</td>
          <td>MI</td>
          <td>USA</td>
          <td>42.350833</td>
          <td>-86.256139</td>
        </tr>
        <tr>
          <th>106</th>
          <td>13C</td>
          <td>Lakeview</td>
          <td>Lakeview</td>
          <td>MI</td>
          <td>USA</td>
          <td>43.452137</td>
          <td>-85.264803</td>
        </tr>
        <tr>
          <th>143</th>
          <td>1D2</td>
          <td>Canton -Plymouth -  Mettetal</td>
          <td>Plymouth</td>
          <td>MI</td>
          <td>USA</td>
          <td>42.350037</td>
          <td>-83.458268</td>
        </tr>
        <tr>
          <th>302</th>
          <td>35D</td>
          <td>Padgham</td>
          <td>Allegan</td>
          <td>MI</td>
          <td>USA</td>
          <td>42.530983</td>
          <td>-85.825136</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_mi = df_airports.query('state=="MI"')
    
    # update dict appropriately
    data[0]['lat'] = df_mi['lat']
    data[0]['lon'] = df_mi['long']
    data[0]['text'] = df_mi['airport'] + ' ' + df_mi['city']
    
    layout['title'] = 'Airports in Michigan<br>(Hover for airport names. Mouse scroll to zoom, right-click to pan)'
    
    fig = dict( data=data, layout=layout )
    py.iplot( fig, filename='spotify-tmp3', sharing = 'secret',validate=False)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1351.embed?share_key=boE8CXijf20MKcLBq8PbW9" height="525px" width="100%"></iframe>


