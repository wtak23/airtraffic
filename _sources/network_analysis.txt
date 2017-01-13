Part3: Network analysis of 2016 US Air Traffic
""""""""""""""""""""""""""""""""""""""""""""""
The original Jupyter notebook can be downloaded from `here <http://nbviewer.jupyter.org/github/wtak23/airtraffic/blob/master/final_scripts/network_analysis.ipynb>`__ .

.. contents:: `Page Contents`
   :depth: 2
   :local:

Overview: network view of the US Airtraffic System
==================================================

-  In this final part of the project, we'll view the US Airline system
   as a large network (graph) system consisting of nodes (airports)
   whose interactions/connections are described by edges (flights
   between airports).
-  More precisely, we will view the airport graph as a `complex
   network <https://en.wikipedia.org/wiki/Complex_network>`__ system,
   which exhibits non-trivial topology that are absent in random graphs
   (such as hub nodes with high degre of centrality)
-  Complex network is a heavily researched field, and we fortunately
   have access to rich set of both theoretical and practical tools

-  tools I will relying on for this work:

-  `NetworkX <networkx.readthedocs.org/en/networkx-1.11/>`__ and `Brain
   Connectivity Toolbox <https://sites.google.com/site/bctnet/>`__ for
   computing collections of `**complex network
   measures** <https://arxiv.org/pdf/cond-mat/0505185v5.pdf>`__ that
   characterizes the topological struture of the network
-  `Gephi <https://gephi.org/>`__ for visualizing the graph data saved
   as a ``.gexf`` file

This part of the analysis was by far mar favorite part!

Outline of the analysis
-----------------------

-  we'll again begin by **tidying** the US passenger travel data into a
   graph structure
-  For any airport pair, say ``A`` and ``B``, we'll measure the **edge**
   in two ways:

(1) **trips**: ``A -> B`` is distinguished from ``B -> A``;
    directionality matters here (**directed graph**)

(2) **routes**: ``A -> B`` and ``B -> A`` are not distuishable, so both
    landings and take-offs are counted; (**undirected graph**)

-  once we have the normalized data, we'll first identify the pairs of
   airports with the largest edge values

-  we will then compute a collection of key network measures that
   characterizes the topologicla property of the US air-traffic system,
   such as the level of centrality/important of an airport, as well as
   the **community structure** formed among the US airports (ie, set of
   airports that tend to be tightly connected with each other)

The remainder of the section loads the dataset in the exact same way as
part1 and 2.

.. code:: python

    %matplotlib inline

.. code:: python

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly
    import plotly.plotly as py
    
    # libraries for network analysis
    import networkx as nx
    import bct
    
    from pprint import pprint
    from IPython.display import display
    
    import cufflinks as cf
    cf.set_config_file(theme='ggplot',sharing='secret')
    
    # utility functions for this project
    # see https://github.com/wtak23/airtraffic/blob/master/final_scripts/util/util.py
    import util
    
    # limit output to avoid cluttering screen
    pd.options.display.max_rows = 20

.. code:: python

    period = '11/1/2015 to 10/31/2016'
    outfile = 'network_analysis'

.. code:: python

    df_data = util.load_airport_data()
    df_data.head()


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



.. code:: python

    df_lookup = pd.read_csv('df_lookup.csv') # lookup table for the AIRPORT_ID above
    
    display(df_lookup.head())



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
          <th>0</th>
          <td>10135</td>
          <td>Allentown/Bethlehem/Easton, PA: Lehigh Valley ...</td>
          <td>Lehigh Valley International</td>
          <td>Allentown/Bethlehem/Easton</td>
          <td>PA</td>
          <td>Northeast</td>
          <td>40.651650</td>
          <td>-75.434746</td>
          <td>Allentown/Bethlehem/Easton (PA)</td>
        </tr>
        <tr>
          <th>1</th>
          <td>10136</td>
          <td>Abilene, TX: Abilene Regional</td>
          <td>Abilene Regional</td>
          <td>Abilene</td>
          <td>TX</td>
          <td>South</td>
          <td>32.448736</td>
          <td>-99.733144</td>
          <td>Abilene (TX)</td>
        </tr>
        <tr>
          <th>2</th>
          <td>10140</td>
          <td>Albuquerque, NM: Albuquerque International Sun...</td>
          <td>Albuquerque International Sunport</td>
          <td>Albuquerque</td>
          <td>NM</td>
          <td>West</td>
          <td>35.043333</td>
          <td>-106.612909</td>
          <td>Albuquerque (NM)</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10141</td>
          <td>Aberdeen, SD: Aberdeen Regional</td>
          <td>Aberdeen Regional</td>
          <td>Aberdeen</td>
          <td>SD</td>
          <td>Midwest</td>
          <td>45.453458</td>
          <td>-98.417726</td>
          <td>Aberdeen (SD)</td>
        </tr>
        <tr>
          <th>4</th>
          <td>10146</td>
          <td>Albany, GA: Southwest Georgia Regional</td>
          <td>Southwest Georgia Regional</td>
          <td>Albany</td>
          <td>GA</td>
          <td>South</td>
          <td>31.535671</td>
          <td>-84.193905</td>
          <td>Albany (GA)</td>
        </tr>
      </tbody>
    </table>
    </div>


Create directed graph: **trips**
================================

-  we first define a directed graph, where flights ``A->B`` is
   distinguished from ``B-A``

-  I'll refer to these edges as ``trips``

Data tidying
------------

.. code:: python

    # create a new column containing the *origin* and the *destination* airport
    # (these will form the network "edges" in our graph, with airport being the nodes)
    df_data['Trips'] = tuple(zip(df_data['ORIGIN_AIRPORT_ID'], df_data['DEST_AIRPORT_ID']))
    df_data.head()




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
          <th>Trips</th>
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
          <td>(14570, 13930)</td>
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
          <td>(13930, 14057)</td>
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
          <td>(13930, 14057)</td>
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
          <td>(13930, 14057)</td>
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
          <td>(13930, 14057)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # create table of "trip_counts" (sorted by most frequent trips)
    trip_counts = df_data['Trips'].value_counts().to_frame('counts')
    trip_counts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>(14771, 12892)</th>
          <td>17757</td>
        </tr>
        <tr>
          <th>(12892, 14771)</th>
          <td>17409</td>
        </tr>
        <tr>
          <th>(12892, 12478)</th>
          <td>12463</td>
        </tr>
        <tr>
          <th>(12478, 12892)</th>
          <td>12461</td>
        </tr>
        <tr>
          <th>(12892, 12889)</th>
          <td>11317</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # create two columns for the pair of nodes forming the edge
    trip_counts['code1'] = trip_counts.index.map(lambda x: x[0])
    trip_counts['code2'] = trip_counts.index.map(lambda x: x[1])
    
    trip_counts.reset_index(drop=True,inplace=True)
    trip_counts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>code1</th>
          <th>code2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>17757</td>
          <td>14771</td>
          <td>12892</td>
        </tr>
        <tr>
          <th>1</th>
          <td>17409</td>
          <td>12892</td>
          <td>14771</td>
        </tr>
        <tr>
          <th>2</th>
          <td>12463</td>
          <td>12892</td>
          <td>12478</td>
        </tr>
        <tr>
          <th>3</th>
          <td>12461</td>
          <td>12478</td>
          <td>12892</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11317</td>
          <td>12892</td>
          <td>12889</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # create columns with corresponding airport information
    columns = [u'Airport', u'City',u'State']
    
    for col in columns:
        # create hash-table for ID lookup
        hash_table = df_lookup.set_index('Code')[col].to_dict()
        
        trip_counts[col + '1'] = trip_counts['code1'].map(lambda code: hash_table[code])
        trip_counts[col + '2'] = trip_counts['code2'].map(lambda code: hash_table[code])
        
    # reorder columns (just personal preference)
    cols = trip_counts.columns.tolist()
    cols = [cols[0]] + cols[3:9] + cols[1:3]
    trip_counts = trip_counts[cols]
    trip_counts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>17757</td>
          <td>San Francisco International</td>
          <td>Los Angeles International</td>
          <td>San Francisco</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>CA</td>
          <td>14771</td>
          <td>12892</td>
        </tr>
        <tr>
          <th>1</th>
          <td>17409</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
        </tr>
        <tr>
          <th>2</th>
          <td>12463</td>
          <td>Los Angeles International</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles</td>
          <td>New York</td>
          <td>CA</td>
          <td>NY</td>
          <td>12892</td>
          <td>12478</td>
        </tr>
        <tr>
          <th>3</th>
          <td>12461</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11317</td>
          <td>Los Angeles International</td>
          <td>McCarran International</td>
          <td>Los Angeles</td>
          <td>Las Vegas</td>
          <td>CA</td>
          <td>NV</td>
          <td>12892</td>
          <td>12889</td>
        </tr>
      </tbody>
    </table>
    </div>



-  add distance associated with each trips (ie, distance between aiports
   in kilometers)
-  to do this, we convert the pairs of lat/lon into distance using
   `Vincent's
   formula <https://en.wikipedia.org/wiki/Vincenty's_formulae>`__

.. code:: python

    # add distance associated with each trips (ie, distance between aiports)
    # see https://en.wikipedia.org/wiki/Vincenty's_formulae
    from geopy.distance import vincenty
    dist_ = []
    
    hash_lat = df_lookup.set_index('Code')['lat'].to_dict()
    hash_lon = df_lookup.set_index('Code')['lon'].to_dict()
    for code1,code2 in zip(trip_counts['code1'],trip_counts['code2']):
        coord1 = hash_lat[code1],hash_lon[code1]
        coord2 = hash_lat[code2],hash_lon[code2]
        dist_.append(vincenty(coord1,coord2).kilometers)
        
    trip_counts['distance'] = dist_
    trip_counts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>17757</td>
          <td>San Francisco International</td>
          <td>Los Angeles International</td>
          <td>San Francisco</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>CA</td>
          <td>14771</td>
          <td>12892</td>
          <td>543.531637</td>
        </tr>
        <tr>
          <th>1</th>
          <td>17409</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
          <td>543.531637</td>
        </tr>
        <tr>
          <th>2</th>
          <td>12463</td>
          <td>Los Angeles International</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles</td>
          <td>New York</td>
          <td>CA</td>
          <td>NY</td>
          <td>12892</td>
          <td>12478</td>
          <td>3983.079400</td>
        </tr>
        <tr>
          <th>3</th>
          <td>12461</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
          <td>3983.079400</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11317</td>
          <td>Los Angeles International</td>
          <td>McCarran International</td>
          <td>Los Angeles</td>
          <td>Las Vegas</td>
          <td>CA</td>
          <td>NV</td>
          <td>12892</td>
          <td>12889</td>
          <td>380.413047</td>
        </tr>
      </tbody>
    </table>
    </div>



Most frequent "trips" in US during the past year
------------------------------------------------

-  now that we have an appropriate table, let's start exploring which
   trip (pair of airports) took place the most during Nov-1-2015 to
   Oct-31-2016

-  let's first see the top 10 trips

.. code:: python

    print "{} unique trips made".format(trip_counts.shape[0])
    print ' the top 10 flights during {} '.format(period).center(80,'=')
    trip_counts.head(n=10)


.. parsed-literal::
    :class: myliteral

    4637 unique trips made
    ============== the top 10 flights during 11/1/2015 to 10/31/2016 ===============
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>17757</td>
          <td>San Francisco International</td>
          <td>Los Angeles International</td>
          <td>San Francisco</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>CA</td>
          <td>14771</td>
          <td>12892</td>
          <td>543.531637</td>
        </tr>
        <tr>
          <th>1</th>
          <td>17409</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
          <td>543.531637</td>
        </tr>
        <tr>
          <th>2</th>
          <td>12463</td>
          <td>Los Angeles International</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles</td>
          <td>New York</td>
          <td>CA</td>
          <td>NY</td>
          <td>12892</td>
          <td>12478</td>
          <td>3983.079400</td>
        </tr>
        <tr>
          <th>3</th>
          <td>12461</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
          <td>3983.079400</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11317</td>
          <td>Los Angeles International</td>
          <td>McCarran International</td>
          <td>Los Angeles</td>
          <td>Las Vegas</td>
          <td>CA</td>
          <td>NV</td>
          <td>12892</td>
          <td>12889</td>
          <td>380.413047</td>
        </tr>
        <tr>
          <th>5</th>
          <td>11298</td>
          <td>McCarran International</td>
          <td>Los Angeles International</td>
          <td>Las Vegas</td>
          <td>Los Angeles</td>
          <td>NV</td>
          <td>CA</td>
          <td>12889</td>
          <td>12892</td>
          <td>380.413047</td>
        </tr>
        <tr>
          <th>6</th>
          <td>10245</td>
          <td>Seattle/Tacoma International</td>
          <td>Los Angeles International</td>
          <td>Seattle</td>
          <td>Los Angeles</td>
          <td>WA</td>
          <td>CA</td>
          <td>14747</td>
          <td>12892</td>
          <td>1535.379400</td>
        </tr>
        <tr>
          <th>7</th>
          <td>10224</td>
          <td>Los Angeles International</td>
          <td>Seattle/Tacoma International</td>
          <td>Los Angeles</td>
          <td>Seattle</td>
          <td>CA</td>
          <td>WA</td>
          <td>12892</td>
          <td>14747</td>
          <td>1535.379400</td>
        </tr>
        <tr>
          <th>8</th>
          <td>10057</td>
          <td>LaGuardia</td>
          <td>Chicago O'Hare International</td>
          <td>New York</td>
          <td>Chicago</td>
          <td>NY</td>
          <td>IL</td>
          <td>12953</td>
          <td>13930</td>
          <td>1180.129320</td>
        </tr>
        <tr>
          <th>9</th>
          <td>9954</td>
          <td>Chicago O'Hare International</td>
          <td>LaGuardia</td>
          <td>Chicago</td>
          <td>New York</td>
          <td>IL</td>
          <td>NY</td>
          <td>13930</td>
          <td>12953</td>
          <td>1180.129320</td>
        </tr>
      </tbody>
    </table>
    </div>



-  the top trips comes in pair....which makes sense, as most flights are
   "round-trips"

-  For instance, **SF to LA** (17757 flights) and **LA to SF** (17409
   flights) were the most frequent made trip.

-  As these values are very close, it's reasonable to believe most of
   the flights were **round trips**

-  (the small difference in flight-counts can be due to missed flight,
   permanent relocation, etc)

Let's next plot the top 500 ``trips``.

.. code:: python

    # create hover-text object for plotly
    def string_rank(ranking):
        headstr = 'Ranking: '
        if ranking == 1:
            return headstr + '1st'
        elif ranking == 2:
            return headstr + '2nd'
        elif ranking == 3:
            return headstr + '3rd'
        else:
            return headstr + str(ranking)+'th'
        
    trip_counts['text'] = (trip_counts['Airport1'] 
                  + ' to ' + trip_counts['Airport2']
                  + '<br>' + trip_counts['City1'] + ' (' + trip_counts['State1'] + ')'
                  + ' to ' + trip_counts['City2'] + ' (' + trip_counts['State2'] + ')'
                  + '<br>Number of flight: ' + trip_counts['counts'].astype(str))
    
    trip_counts['text'] = trip_counts['text'] + '<br>' + map(string_rank,trip_counts['text'].index + 1)

.. code:: python

    trip_counts['x'] = trip_counts.index+1
    # trip_counts.iplot(kind='bar',columns=['counts'],text='text',filename='test',x=trip_counts.index.bool())
    
    
    
    # # plot top_k
    top_k = 250
    
    title = 'Most frequent flights made in the US airports between {} (directions considered)'.format(top_k,period)
    title+= '<br>(hover over plots for the pairs of takeoff/landing airports; left-click to pan-zoom)'
    trip_counts[:top_k].iplot(kind='bar',columns=['counts'],x='x', # <- ranking info
                              text='text',xTitle='edge-ranking',
                              color='pink',title=title,
                              filename=outfile+'topk_trip')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1949.embed?link=false&logo=false&share_key=DGLvImGRtSipSJVEfFEkWN" height="525px" width="100%"></iframe>



Create undirected graph -- edges ignoring directionality
========================================================

-  In our next analysis, we'll drop **directionality** in our analysis

-  That is, for any given trip (edge), we'll ignoring which airport was
   used for **take-off** or **landing**

-  So the airport pair (SF,LA) will form an **undirected edge** with a
   value of 17757+17409 = 35166

-  To create an undirected graph, .we do the following:

-  For any airport pair ``A,B``, we identify the directed edges
   ``(A -> B)`` and ``(A <- B)``

-  The resulting undirected edge ``(A <-> B)`` will have the value
   ``(A -> B) + (A <- B)``

Data tidying
------------

.. code:: python

    trip_counts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
          <th>text</th>
          <th>x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>17757</td>
          <td>San Francisco International</td>
          <td>Los Angeles International</td>
          <td>San Francisco</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>CA</td>
          <td>14771</td>
          <td>12892</td>
          <td>543.531637</td>
          <td>San Francisco International to Los Angeles Int...</td>
          <td>1</td>
        </tr>
        <tr>
          <th>1</th>
          <td>17409</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
          <td>543.531637</td>
          <td>Los Angeles International to San Francisco Int...</td>
          <td>2</td>
        </tr>
        <tr>
          <th>2</th>
          <td>12463</td>
          <td>Los Angeles International</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles</td>
          <td>New York</td>
          <td>CA</td>
          <td>NY</td>
          <td>12892</td>
          <td>12478</td>
          <td>3983.079400</td>
          <td>Los Angeles International to John F. Kennedy I...</td>
          <td>3</td>
        </tr>
        <tr>
          <th>3</th>
          <td>12461</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
          <td>3983.079400</td>
          <td>John F. Kennedy International to Los Angeles I...</td>
          <td>4</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11317</td>
          <td>Los Angeles International</td>
          <td>McCarran International</td>
          <td>Los Angeles</td>
          <td>Las Vegas</td>
          <td>CA</td>
          <td>NV</td>
          <td>12892</td>
          <td>12889</td>
          <td>380.413047</td>
          <td>Los Angeles International to McCarran Internat...</td>
          <td>5</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    tmp = pd.Series(map(lambda pair: (min(pair), max(pair) ), 
                         zip(trip_counts['code1'],trip_counts['code2'])))
    
    print tmp[:6]
    
    # detect flights A->B and A<-B (flights sharing same pair of airport)
    mask_AB = tmp.duplicated(keep='first') # edges A -> B
    mask_BA = tmp.duplicated(keep='last')  # edges B -> A
    mask_    = ~(mask_AB|mask_BA)         # some trips only have one direction
    
    assert mask_AB.sum() == mask_BA.sum() 
    assert trip_counts.shape[0] == (mask_AB.sum() + mask_BA.sum() + mask_.sum())
    
    trips_AB = trip_counts[mask_AB]
    trips_BA = trip_counts[mask_BA]
    trip_neither = trip_counts[ ~(mask_AB|mask_BA)]
    
    display(trips_AB.head())
    display(trips_BA.head())
    display(trip_neither.head())


.. parsed-literal::
    :class: myliteral

    0    (12892, 14771)
    1    (12892, 14771)
    2    (12478, 12892)
    3    (12478, 12892)
    4    (12889, 12892)
    5    (12889, 12892)
    dtype: object
    


.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
          <th>text</th>
          <th>x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td>17409</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
          <td>543.531637</td>
          <td>Los Angeles International to San Francisco Int...</td>
          <td>2</td>
        </tr>
        <tr>
          <th>3</th>
          <td>12461</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
          <td>3983.079400</td>
          <td>John F. Kennedy International to Los Angeles I...</td>
          <td>4</td>
        </tr>
        <tr>
          <th>5</th>
          <td>11298</td>
          <td>McCarran International</td>
          <td>Los Angeles International</td>
          <td>Las Vegas</td>
          <td>Los Angeles</td>
          <td>NV</td>
          <td>CA</td>
          <td>12889</td>
          <td>12892</td>
          <td>380.413047</td>
          <td>McCarran International to Los Angeles Internat...</td>
          <td>6</td>
        </tr>
        <tr>
          <th>7</th>
          <td>10224</td>
          <td>Los Angeles International</td>
          <td>Seattle/Tacoma International</td>
          <td>Los Angeles</td>
          <td>Seattle</td>
          <td>CA</td>
          <td>WA</td>
          <td>12892</td>
          <td>14747</td>
          <td>1535.379400</td>
          <td>Los Angeles International to Seattle/Tacoma In...</td>
          <td>8</td>
        </tr>
        <tr>
          <th>9</th>
          <td>9954</td>
          <td>Chicago O'Hare International</td>
          <td>LaGuardia</td>
          <td>Chicago</td>
          <td>New York</td>
          <td>IL</td>
          <td>NY</td>
          <td>13930</td>
          <td>12953</td>
          <td>1180.129320</td>
          <td>Chicago O'Hare International to LaGuardia&lt;br&gt;C...</td>
          <td>10</td>
        </tr>
      </tbody>
    </table>
    </div>



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
          <th>text</th>
          <th>x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>17757</td>
          <td>San Francisco International</td>
          <td>Los Angeles International</td>
          <td>San Francisco</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>CA</td>
          <td>14771</td>
          <td>12892</td>
          <td>543.531637</td>
          <td>San Francisco International to Los Angeles Int...</td>
          <td>1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>12463</td>
          <td>Los Angeles International</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles</td>
          <td>New York</td>
          <td>CA</td>
          <td>NY</td>
          <td>12892</td>
          <td>12478</td>
          <td>3983.079400</td>
          <td>Los Angeles International to John F. Kennedy I...</td>
          <td>3</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11317</td>
          <td>Los Angeles International</td>
          <td>McCarran International</td>
          <td>Los Angeles</td>
          <td>Las Vegas</td>
          <td>CA</td>
          <td>NV</td>
          <td>12892</td>
          <td>12889</td>
          <td>380.413047</td>
          <td>Los Angeles International to McCarran Internat...</td>
          <td>5</td>
        </tr>
        <tr>
          <th>6</th>
          <td>10245</td>
          <td>Seattle/Tacoma International</td>
          <td>Los Angeles International</td>
          <td>Seattle</td>
          <td>Los Angeles</td>
          <td>WA</td>
          <td>CA</td>
          <td>14747</td>
          <td>12892</td>
          <td>1535.379400</td>
          <td>Seattle/Tacoma International to Los Angeles In...</td>
          <td>7</td>
        </tr>
        <tr>
          <th>8</th>
          <td>10057</td>
          <td>LaGuardia</td>
          <td>Chicago O'Hare International</td>
          <td>New York</td>
          <td>Chicago</td>
          <td>NY</td>
          <td>IL</td>
          <td>12953</td>
          <td>13930</td>
          <td>1180.129320</td>
          <td>LaGuardia to Chicago O'Hare International&lt;br&gt;N...</td>
          <td>9</td>
        </tr>
      </tbody>
    </table>
    </div>



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
          <th>text</th>
          <th>x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>3241</th>
          <td>366</td>
          <td>Wiley Post/Will Rogers Memorial</td>
          <td>Fairbanks International</td>
          <td>Barrow</td>
          <td>Fairbanks</td>
          <td>AK</td>
          <td>AK</td>
          <td>10754</td>
          <td>11630</td>
          <td>809.595183</td>
          <td>Wiley Post/Will Rogers Memorial to Fairbanks I...</td>
          <td>3242</td>
        </tr>
        <tr>
          <th>3598</th>
          <td>263</td>
          <td>Devils Lake Regional</td>
          <td>Denver International</td>
          <td>Devils Lake</td>
          <td>Denver</td>
          <td>ND</td>
          <td>CO</td>
          <td>11447</td>
          <td>11292</td>
          <td>1028.249825</td>
          <td>Devils Lake Regional to Denver International&lt;b...</td>
          <td>3599</td>
        </tr>
        <tr>
          <th>3607</th>
          <td>261</td>
          <td>Hattiesburg-Laurel Regional</td>
          <td>Dallas/Fort Worth International</td>
          <td>Hattiesburg/Laurel</td>
          <td>Dallas/Fort Worth</td>
          <td>MS</td>
          <td>TX</td>
          <td>14109</td>
          <td>11298</td>
          <td>751.719146</td>
          <td>Hattiesburg-Laurel Regional to Dallas/Fort Wor...</td>
          <td>3608</td>
        </tr>
        <tr>
          <th>4344</th>
          <td>23</td>
          <td>Washington Dulles International</td>
          <td>San Antonio International</td>
          <td>Washington</td>
          <td>San Antonio</td>
          <td>DC</td>
          <td>TX</td>
          <td>12264</td>
          <td>14683</td>
          <td>2192.125251</td>
          <td>Washington Dulles International to San Antonio...</td>
          <td>4345</td>
        </tr>
        <tr>
          <th>4365</th>
          <td>16</td>
          <td>Joslin Field - Magic Valley Regional</td>
          <td>San Francisco International</td>
          <td>Twin Falls</td>
          <td>San Francisco</td>
          <td>ID</td>
          <td>CA</td>
          <td>15389</td>
          <td>14771</td>
          <td>862.579453</td>
          <td>Joslin Field - Magic Valley Regional to San Fr...</td>
          <td>4366</td>
        </tr>
      </tbody>
    </table>
    </div>


.. code:: python

    trips_AB = trip_counts[mask_AB]
    trips_BA = trip_counts[mask_BA]
    trip_neither = trip_counts[ ~(mask_AB|mask_BA)]
    
    # this will serve as our final undirected graph
    trip_counts_und = trips_AB.copy()
    
    # to identify matching rows, swap code1,code2
    trips_BA = trips_BA.rename(columns={'code1':'code2','code2':'code1'})[['counts','code1','code2']]
    
    # now we can use the code pairs as merge-keys
    trip_counts_und = trips_AB.merge(trips_BA, on=['code1','code2'],suffixes=['','_'])
    
    trip_counts_und.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
          <th>text</th>
          <th>x</th>
          <th>counts_</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>17409</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
          <td>543.531637</td>
          <td>Los Angeles International to San Francisco Int...</td>
          <td>2</td>
          <td>17757</td>
        </tr>
        <tr>
          <th>1</th>
          <td>12461</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
          <td>3983.079400</td>
          <td>John F. Kennedy International to Los Angeles I...</td>
          <td>4</td>
          <td>12463</td>
        </tr>
        <tr>
          <th>2</th>
          <td>11298</td>
          <td>McCarran International</td>
          <td>Los Angeles International</td>
          <td>Las Vegas</td>
          <td>Los Angeles</td>
          <td>NV</td>
          <td>CA</td>
          <td>12889</td>
          <td>12892</td>
          <td>380.413047</td>
          <td>McCarran International to Los Angeles Internat...</td>
          <td>6</td>
          <td>11317</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10224</td>
          <td>Los Angeles International</td>
          <td>Seattle/Tacoma International</td>
          <td>Los Angeles</td>
          <td>Seattle</td>
          <td>CA</td>
          <td>WA</td>
          <td>12892</td>
          <td>14747</td>
          <td>1535.379400</td>
          <td>Los Angeles International to Seattle/Tacoma In...</td>
          <td>8</td>
          <td>10245</td>
        </tr>
        <tr>
          <th>4</th>
          <td>9954</td>
          <td>Chicago O'Hare International</td>
          <td>LaGuardia</td>
          <td>Chicago</td>
          <td>New York</td>
          <td>IL</td>
          <td>NY</td>
          <td>13930</td>
          <td>12953</td>
          <td>1180.129320</td>
          <td>Chicago O'Hare International to LaGuardia&lt;br&gt;C...</td>
          <td>10</td>
          <td>10057</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # now we can sum both directions of the edge to create our undirected graph :)
    trip_counts_und['counts'] = trip_counts_und['counts'] + trip_counts_und['counts_']
    del trip_counts_und['counts_']
    
    # to complete, append the trips that only had one-way direction, and re-sort!
    trip_counts_und = trip_counts_und.append(trip_neither).\
                          sort_values('counts',ascending=False).\
                          reset_index(drop=True)
    
    # finaly undirected graph!
    trip_counts_und.head(10)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
          <th>text</th>
          <th>x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>35166</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
          <td>543.531637</td>
          <td>Los Angeles International to San Francisco Int...</td>
          <td>2</td>
        </tr>
        <tr>
          <th>1</th>
          <td>24924</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
          <td>3983.079400</td>
          <td>John F. Kennedy International to Los Angeles I...</td>
          <td>4</td>
        </tr>
        <tr>
          <th>2</th>
          <td>22615</td>
          <td>McCarran International</td>
          <td>Los Angeles International</td>
          <td>Las Vegas</td>
          <td>Los Angeles</td>
          <td>NV</td>
          <td>CA</td>
          <td>12889</td>
          <td>12892</td>
          <td>380.413047</td>
          <td>McCarran International to Los Angeles Internat...</td>
          <td>6</td>
        </tr>
        <tr>
          <th>3</th>
          <td>20469</td>
          <td>Los Angeles International</td>
          <td>Seattle/Tacoma International</td>
          <td>Los Angeles</td>
          <td>Seattle</td>
          <td>CA</td>
          <td>WA</td>
          <td>12892</td>
          <td>14747</td>
          <td>1535.379400</td>
          <td>Los Angeles International to Seattle/Tacoma In...</td>
          <td>8</td>
        </tr>
        <tr>
          <th>4</th>
          <td>20011</td>
          <td>Chicago O'Hare International</td>
          <td>LaGuardia</td>
          <td>Chicago</td>
          <td>New York</td>
          <td>IL</td>
          <td>NY</td>
          <td>13930</td>
          <td>12953</td>
          <td>1180.129320</td>
          <td>Chicago O'Hare International to LaGuardia&lt;br&gt;C...</td>
          <td>10</td>
        </tr>
        <tr>
          <th>5</th>
          <td>18254</td>
          <td>Honolulu International</td>
          <td>Kahului Airport</td>
          <td>Honolulu</td>
          <td>Kahului</td>
          <td>HI</td>
          <td>HI</td>
          <td>12173</td>
          <td>13830</td>
          <td>162.094231</td>
          <td>Honolulu International to Kahului Airport&lt;br&gt;H...</td>
          <td>15</td>
        </tr>
        <tr>
          <th>6</th>
          <td>18244</td>
          <td>San Francisco International</td>
          <td>McCarran International</td>
          <td>San Francisco</td>
          <td>Las Vegas</td>
          <td>CA</td>
          <td>NV</td>
          <td>14771</td>
          <td>12889</td>
          <td>666.370587</td>
          <td>San Francisco International to McCarran Intern...</td>
          <td>14</td>
        </tr>
        <tr>
          <th>7</th>
          <td>18141</td>
          <td>Chicago O'Hare International</td>
          <td>Los Angeles International</td>
          <td>Chicago</td>
          <td>Los Angeles</td>
          <td>IL</td>
          <td>CA</td>
          <td>13930</td>
          <td>12892</td>
          <td>2807.429621</td>
          <td>Chicago O'Hare International to Los Angeles In...</td>
          <td>18</td>
        </tr>
        <tr>
          <th>8</th>
          <td>18093</td>
          <td>Hartsfield-Jackson Atlanta International</td>
          <td>Orlando International</td>
          <td>Atlanta</td>
          <td>Orlando</td>
          <td>GA</td>
          <td>FL</td>
          <td>10397</td>
          <td>13204</td>
          <td>649.748804</td>
          <td>Hartsfield-Jackson Atlanta International to Or...</td>
          <td>17</td>
        </tr>
        <tr>
          <th>9</th>
          <td>17042</td>
          <td>Ronald Reagan Washington National</td>
          <td>Logan International</td>
          <td>Washington</td>
          <td>Boston</td>
          <td>DC</td>
          <td>MA</td>
          <td>11278</td>
          <td>10721</td>
          <td>642.205372</td>
          <td>Ronald Reagan Washington National to Logan Int...</td>
          <td>20</td>
        </tr>
      </tbody>
    </table>
    </div>



Most frequent "routes" in US during the past year
-------------------------------------------------

-  To distinguish undirected edges from directed ones, I'll call the
   edges in the undirected graph **"routes"** , with the line of
   thinking that trips A->B and B->A shares the same *route*

-  (I'll continue to call the directed edges **trips**)

.. code:: python

    route_counts = trip_counts_und

Let's analyze the most frequent **routes** during the period Nov-1-2015
to Oct-31-2016

.. code:: python

    print "{} unique routes".format(route_counts.shape[0])
    print ' the top 10 flight-routes during {} '.format(period).center(80,'=')
    route_counts.head(n=10)


.. parsed-literal::
    :class: myliteral

    2365 unique routes
    =========== the top 10 flight-routes during 11/1/2015 to 10/31/2016 ============
    



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>Airport1</th>
          <th>Airport2</th>
          <th>City1</th>
          <th>City2</th>
          <th>State1</th>
          <th>State2</th>
          <th>code1</th>
          <th>code2</th>
          <th>distance</th>
          <th>text</th>
          <th>x</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>35166</td>
          <td>Los Angeles International</td>
          <td>San Francisco International</td>
          <td>Los Angeles</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>CA</td>
          <td>12892</td>
          <td>14771</td>
          <td>543.531637</td>
          <td>Los Angeles International to San Francisco Int...</td>
          <td>2</td>
        </tr>
        <tr>
          <th>1</th>
          <td>24924</td>
          <td>John F. Kennedy International</td>
          <td>Los Angeles International</td>
          <td>New York</td>
          <td>Los Angeles</td>
          <td>NY</td>
          <td>CA</td>
          <td>12478</td>
          <td>12892</td>
          <td>3983.079400</td>
          <td>John F. Kennedy International to Los Angeles I...</td>
          <td>4</td>
        </tr>
        <tr>
          <th>2</th>
          <td>22615</td>
          <td>McCarran International</td>
          <td>Los Angeles International</td>
          <td>Las Vegas</td>
          <td>Los Angeles</td>
          <td>NV</td>
          <td>CA</td>
          <td>12889</td>
          <td>12892</td>
          <td>380.413047</td>
          <td>McCarran International to Los Angeles Internat...</td>
          <td>6</td>
        </tr>
        <tr>
          <th>3</th>
          <td>20469</td>
          <td>Los Angeles International</td>
          <td>Seattle/Tacoma International</td>
          <td>Los Angeles</td>
          <td>Seattle</td>
          <td>CA</td>
          <td>WA</td>
          <td>12892</td>
          <td>14747</td>
          <td>1535.379400</td>
          <td>Los Angeles International to Seattle/Tacoma In...</td>
          <td>8</td>
        </tr>
        <tr>
          <th>4</th>
          <td>20011</td>
          <td>Chicago O'Hare International</td>
          <td>LaGuardia</td>
          <td>Chicago</td>
          <td>New York</td>
          <td>IL</td>
          <td>NY</td>
          <td>13930</td>
          <td>12953</td>
          <td>1180.129320</td>
          <td>Chicago O'Hare International to LaGuardia&lt;br&gt;C...</td>
          <td>10</td>
        </tr>
        <tr>
          <th>5</th>
          <td>18254</td>
          <td>Honolulu International</td>
          <td>Kahului Airport</td>
          <td>Honolulu</td>
          <td>Kahului</td>
          <td>HI</td>
          <td>HI</td>
          <td>12173</td>
          <td>13830</td>
          <td>162.094231</td>
          <td>Honolulu International to Kahului Airport&lt;br&gt;H...</td>
          <td>15</td>
        </tr>
        <tr>
          <th>6</th>
          <td>18244</td>
          <td>San Francisco International</td>
          <td>McCarran International</td>
          <td>San Francisco</td>
          <td>Las Vegas</td>
          <td>CA</td>
          <td>NV</td>
          <td>14771</td>
          <td>12889</td>
          <td>666.370587</td>
          <td>San Francisco International to McCarran Intern...</td>
          <td>14</td>
        </tr>
        <tr>
          <th>7</th>
          <td>18141</td>
          <td>Chicago O'Hare International</td>
          <td>Los Angeles International</td>
          <td>Chicago</td>
          <td>Los Angeles</td>
          <td>IL</td>
          <td>CA</td>
          <td>13930</td>
          <td>12892</td>
          <td>2807.429621</td>
          <td>Chicago O'Hare International to Los Angeles In...</td>
          <td>18</td>
        </tr>
        <tr>
          <th>8</th>
          <td>18093</td>
          <td>Hartsfield-Jackson Atlanta International</td>
          <td>Orlando International</td>
          <td>Atlanta</td>
          <td>Orlando</td>
          <td>GA</td>
          <td>FL</td>
          <td>10397</td>
          <td>13204</td>
          <td>649.748804</td>
          <td>Hartsfield-Jackson Atlanta International to Or...</td>
          <td>17</td>
        </tr>
        <tr>
          <th>9</th>
          <td>17042</td>
          <td>Ronald Reagan Washington National</td>
          <td>Logan International</td>
          <td>Washington</td>
          <td>Boston</td>
          <td>DC</td>
          <td>MA</td>
          <td>11278</td>
          <td>10721</td>
          <td>642.205372</td>
          <td>Ronald Reagan Washington National to Logan Int...</td>
          <td>20</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    route_counts['text'] = (  route_counts['Airport1'] 
                  + ' <-> ' + route_counts['Airport2']
                  + '<br>'  + route_counts['City1'] + ' (' + route_counts['State1'] + ')'
                  + ' <-> ' + route_counts['City2'] + ' (' + route_counts['State2'] + ')'
                  + '<br>Number of flights: ' + route_counts['counts'].astype(str))
    
    route_counts['text'] = route_counts['text'] + '<br>' + map(string_rank,route_counts['text'].index + 1)
    route_counts['text'][:5].tolist()




.. parsed-literal::
    :class: myliteral

    ['Los Angeles International <-> San Francisco International<br>Los Angeles (CA) <-> San Francisco (CA)<br>Number of flights: 35166<br>Ranking: 1st',
     'John F. Kennedy International <-> Los Angeles International<br>New York (NY) <-> Los Angeles (CA)<br>Number of flights: 24924<br>Ranking: 2nd',
     'McCarran International <-> Los Angeles International<br>Las Vegas (NV) <-> Los Angeles (CA)<br>Number of flights: 22615<br>Ranking: 3rd',
     'Los Angeles International <-> Seattle/Tacoma International<br>Los Angeles (CA) <-> Seattle (WA)<br>Number of flights: 20469<br>Ranking: 4th',
     "Chicago O'Hare International <-> LaGuardia<br>Chicago (IL) <-> New York (NY)<br>Number of flights: 20011<br>Ranking: 5th"]



.. code:: python

    route_counts['x'] = (route_counts.index+1).values # raking info to give plotly
    # route_counts.iplot(kind='bar',columns=['counts'],text='text',filename='test',color='cyan')
    
    
    # plot top_k
    top_k = 250
    title = 'Most frequent <b>flights</b> made in the US airports between {} (undirected network)'.format(top_k,period)
    title+= '<br>(hover over plots for the pairs of airports; left-click to pan-zoom)'
    route_counts[:top_k].iplot(kind='bar',columns=['counts'],text='text',color='cyan',title=title,x='x',
                              xTitle='Ranking',filename=outfile+'topk_routes')
    




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1951.embed?link=false&logo=false&share_key=mwagthg1Y2h7lqjZUTXlGu" height="525px" width="100%"></iframe>



Ok, the above is nice, but the charts above does not convey the
geographical information about the network architecture of the US
Airflight system.

We'll finally turn out attention to tools from network theory.

**The next setcion only contains helper codes that are rather specific
to ``networkx``, so can be skipped entirely**

(only codes, can be skipped) Define helper functions for complex network analysis
=================================================================================

-  this section defines a set of helper functions that I wrote for my
   own convenience.
-  please skip to next section for actual analysis

make\_nx\_graph: create networkx graph object
---------------------------------------------

.. code:: python

    def make_nx_graph(counts,df_lookup,digraph=False):
        """ Convert airflight-counts between airport pairs into networkx Graph object.
        
        Parameters
        ----------
        counts : pandas.DataFrame
            Table containing the trip_counts (digraph) or route_counts (undirected graph)
            Use for later network analysis scripts
        df_lookup : pandas.DataFrame
            Lookup table created in  http://takwatanabe.me/airtraffic/create_lookup_table.html
            (used to map airport-id key quantities of interest)
        digraph : bool
            Is the graph directed? (default = False, so undirected)
        """
        if digraph:
            G = nx.DiGraph() # directed graph
        else: 
            G = nx.Graph()   # undirected graph
    
        # === provide node information === #
        # get unique set of nodes in the graph
        nodes = set(counts['code1'].unique().tolist() +
                    counts['code2'].unique().tolist())
                    
        G.add_nodes_from(nodes)
        
        # --- add airport name as node attribute (handy for later analysis in Gephi) ---
        # --- to do this, need to pass a dictionary to networkx 
        hash_airport   = df_lookup.set_index('Code')['Airport'].to_dict()
    
        # filter away airports in the lookup-table absent in the graph
        nodes_airport = {key:val for key,val in hash_airport.iteritems() if key in nodes}
        nx.set_node_attributes(G, 'airport', nodes_airport)
        
        # --- add airport latitude/longitude information --- 
        hash_lat       = df_lookup.set_index('Code')['lat'].to_dict()
        hash_lon       = df_lookup.set_index('Code')['lon'].to_dict()
        
        """ Warning (why the typecasting below is important)
        Pandas returns data type in numpy.float64 for floats, which is not 
        supported in ``networkx.write_gexf`` (learned this the hard way...)
        
        http://stackoverflow.com/questions/22037360/keyerror-when-writing-numpy-values-to-gexf-with-networkx
        """
        # apply filering with typecasting from numpy.float64 to float
        nodes_lat = {key:float(val) for key,val in hash_lat.iteritems() if key in nodes}
        nodes_lon = {key:float(val) for key,val in hash_lon.iteritems() if key in nodes}
        nx.set_node_attributes(G, 'lat', nodes_lat)
        nx.set_node_attributes(G, 'lon', nodes_lon)
        
        # === add weighted edge information (flight counts in our context) === #
        # to define edge, supply a 3-tuple of ``(node1,node2,dict(weight=edge))``
        edges = map(lambda x:(x[0],x[1], dict(weight=x[2])), 
                    zip(counts['code1'], counts['code2'], counts['counts']))
        G.add_edges_from(edges)
        
        # === done! ready to return, except one more step! === 
        # instead of using the Airport_ID as the node-labels, let's instead use the
        # City+State information, which is unique so can be used as lookup-keys
        hash_citystate = df_lookup.set_index('Code')['City_State'].to_dict()
        nodes_citystate = {key:val for key,val in hash_citystate.iteritems() if key in nodes}
        G = nx.relabel_nodes(G,nodes_citystate)
        return G

compute\_network\_measures: network measures characterizing nodes (airport)
---------------------------------------------------------------------------

.. code:: python

    def compute_network_measures(G,add_module_attr = True):
        """ Compute a set of well studied complex network measures
        
        The measures characterizes individual nodes in the network
        (in  our context, characterizes the airport)
        
        - pagerank: Google page-rank centrality
        - eig_cent: Eigen-value centrality
        - bet_cent: Betweenness centrality
        - clust_coef: Clustering coefficient (only implemented for undirected graph)
        
        Parameters
        ----------
        G : networkx graph object
            networkx graph object returned from ``make_nx_graph``. 
            Can be directed or undirected.
        add_module_attr : bool
            Add module information to the input G inplace. 
            Helpful when wanting to export object as ``*.gexf`` file for 
            analysis in Gephi.
        """
        A = np.array(nx.to_numpy_matrix(G))
        
        degree_wei = A.sum(axis=0,dtype=int) # weighted degree 
        degree_bin = (A!=0).sum(axis=0)      # binary degree
        
        # appply modularity algorithm to detect communities of airports
        module = bct.modularity_louvain_und(bct.normalize(A),seed=0)[0]
        
        # convert numpy array into dictionary with node-label
        degree_wei = {node:deg for node,deg in zip(G.nodes(), degree_wei)}
        degree_bin = {node:deg for node,deg in zip(G.nodes(), degree_bin)}
        module = {node:int(modu) for node,modu in zip(G.nodes(), module)}
        
        if add_module_attr:
            # add community label as node attributes 
            # (handy when exporting .gexf file)
            nx.set_node_attributes(G, 'modu', module)
        
        # nodal centrality measures
        pagerank = nx.pagerank(G)               # google page-rank
        eig_cent = nx.eigenvector_centrality(G) # eigenvalue centrality
        bet_cent = nx.betweenness_centrality(G) # betweennes centrality
        
        # create dictionary of each of the measures computed above
        # (to be convertd to dataframe at end)
        df_network = dict(pagerank=pagerank,
                          eig_cent=eig_cent,
                          bet_cent=bet_cent,
                          degree_wei=degree_wei,
                          degree_bin=degree_bin,
                          module=module)
                          
        if not isinstance(G, nx.classes.digraph.DiGraph):
            # clustering coefficient (tendency of a node to cluster together)
            # (not implemented for digraphs)
            clust_coef = nx.clustering(G,weight=G)
            df_network.update(dict(clust_coef=clust_coef))
        
        # all set! convert dict to dataframe and return :)
        return pd.DataFrame(df_network)

Other helper functions
----------------------

.. code:: python

    def string_rank(ranking):
        headstr = 'Ranking: '
        if ranking == 1:
            return headstr + '1st'
        elif ranking == 2:
            return headstr + '2nd'
        elif ranking == 3:
            return headstr + '3rd'
        else:
            return headstr + str(ranking)+'th'
    
    def add_ranking_hover_text(df,column,description):
        hover_text = df['Airport'] + '<br>' \
                   + df['City'] + ', ' + df['State'] + '<br>' \
                   + description + ': ' + df[column].astype(str)
    
        df['text'] = (hover_text + '<br>' + map(string_rank,df.index+1)).tolist()
        
    def get_base_plotly_layout():
        """ This layout will be used repeatedly """
        layout = dict(
                showlegend = True,
                legend = dict(
                    font = dict(size=11),
                    #bordercolor='rgb(0,0,0)',
                    #borderwidth=1,
                    orientation='h',
                    x=0.5, y = 1.08, 
                    xanchor='center', yanchor='top',
                ),
                geo = dict(
                    scope='usa',
                    projection=dict( type='albers usa' ),
                    showland = True,
                    landcolor = 'rgb(217, 217, 217)',
                    subunitwidth=1,
                    countrywidth=1,
                    subunitcolor="rgb(255, 255, 255)",
                    countrycolor="rgb(255, 255, 255)"
                ),
                margin = dict(b=0,l=0,r=0,t=125),
            )
        return layout

Complex network theory in action!
=================================

-  below, we will focus on **undirected graph**, but a very similar
   result can be obtained using directed graph
-  (which makes sense, since most of the flights consist of round-trips)

.. code:: python

    measure_abbrev = {
        'bet_cent': 'Betweenness Centrality',
        'clust_coef': 'Clustering Coefficient',
        'degree_bin' : 'Binary Degree',
        'degree_wei' : 'Weighted Degree',
        'eig_cent': 'Eigenvalue Centrality',
        'pagerank': 'Google PageRank Cenrality',
        'module': 'Community membership'
    }

.. code:: python

    G = make_nx_graph(route_counts,df_lookup,digraph=False)
    df_network = compute_network_measures(G,add_module_attr=True)
    
    df_network['module'] = df_network['module'].map(lambda num: 'Module '+str(num))
    df_network.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>bet_cent</th>
          <th>clust_coef</th>
          <th>degree_bin</th>
          <th>degree_wei</th>
          <th>eig_cent</th>
          <th>module</th>
          <th>pagerank</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Aberdeen (SD)</th>
          <td>0.000000e+00</td>
          <td>0.000000</td>
          <td>1</td>
          <td>1484</td>
          <td>0.001100</td>
          <td>Module 4</td>
          <td>0.000590</td>
        </tr>
        <tr>
          <th>Abilene (TX)</th>
          <td>0.000000e+00</td>
          <td>0.000000</td>
          <td>1</td>
          <td>1019</td>
          <td>0.001120</td>
          <td>Module 1</td>
          <td>0.000548</td>
        </tr>
        <tr>
          <th>Adak Island (AK)</th>
          <td>0.000000e+00</td>
          <td>0.000000</td>
          <td>1</td>
          <td>210</td>
          <td>0.000021</td>
          <td>Module 2</td>
          <td>0.000512</td>
        </tr>
        <tr>
          <th>Aguadilla (PR)</th>
          <td>7.630803e-07</td>
          <td>0.833333</td>
          <td>4</td>
          <td>3642</td>
          <td>0.002570</td>
          <td>Module 3</td>
          <td>0.000696</td>
        </tr>
        <tr>
          <th>Akron (OH)</th>
          <td>1.396953e-05</td>
          <td>0.777778</td>
          <td>9</td>
          <td>11059</td>
          <td>0.012991</td>
          <td>Module 1</td>
          <td>0.001239</td>
        </tr>
      </tbody>
    </table>
    </div>



Let's quickly peruse the distribution of these network measures

.. code:: python

    FF = plotly.tools.FigureFactory
    fig = FF.create_scatterplotmatrix(df_network,diag='histogram',index='module',width=800,height=650)
    fig.layout['title'] = 'Scatterplot Matrix of Complex Network Measures'
    
    py.iplot(fig,filename=outfile+'_scattermat')


.. parsed-literal::
    :class: myliteral

    This is the format of your plot grid:
    [ (1,1) x1,y1 ]    [ (1,2) x2,y2 ]    [ (1,3) x3,y3 ]    [ (1,4) x4,y4 ]    [ (1,5) x5,y5 ]    [ (1,6) x6,y6 ]  
    [ (2,1) x7,y7 ]    [ (2,2) x8,y8 ]    [ (2,3) x9,y9 ]    [ (2,4) x10,y10 ]  [ (2,5) x11,y11 ]  [ (2,6) x12,y12 ]
    [ (3,1) x13,y13 ]  [ (3,2) x14,y14 ]  [ (3,3) x15,y15 ]  [ (3,4) x16,y16 ]  [ (3,5) x17,y17 ]  [ (3,6) x18,y18 ]
    [ (4,1) x19,y19 ]  [ (4,2) x20,y20 ]  [ (4,3) x21,y21 ]  [ (4,4) x22,y22 ]  [ (4,5) x23,y23 ]  [ (4,6) x24,y24 ]
    [ (5,1) x25,y25 ]  [ (5,2) x26,y26 ]  [ (5,3) x27,y27 ]  [ (5,4) x28,y28 ]  [ (5,5) x29,y29 ]  [ (5,6) x30,y30 ]
    [ (6,1) x31,y31 ]  [ (6,2) x32,y32 ]  [ (6,3) x33,y33 ]  [ (6,4) x34,y34 ]  [ (6,5) x35,y35 ]  [ (6,6) x36,y36 ]
    
    



.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1953.embed?link=false&logo=false&share_key=gGIBKQOHB5hkU1UgIIoq2z" height="650px" width="800px"></iframe>



-  High **`centrality <https://en.wikipedia.org/wiki/Centrality>`__**
   indicates the airports of high importance, such as number of
   connections an airport provides (eg, hub structure from nodes with
   high degree).
-  The centrality measures, appear to indicate a
   **`power-law <https://en.wikipedia.org/wiki/Power_law>`__**
   disttribution, hinting that the US airtraffic system forms what is
   known as a `scale-free
   structure <en.wikipedia.org/wiki/Scale-free_network>`__

Power law analysis of centrality measures
-----------------------------------------

-  we'll visually examine how well the distribution of the cenrality
   measures fit the power-law distribution.

**CREDIT**: code inspired from Philip Singer's blog post.

http://www.philippsinger.info/?p=247

.. code:: python

    import powerlaw 
    
    _,axes=util.sns_subplots(nrows=2,ncols=3,figsize=(14,11))
    
    i=0
    for measure in measure_abbrev:
        if measure == 'module': continue
        ax = axes[i]
        i+=1
        fit = powerlaw.Fit(df_network[measure])
    
        fit.plot_ccdf(linewidth=3, label=measure_abbrev[measure],ax=ax)
        fit.power_law.plot_ccdf(ax=ax, color='r', linestyle='--', label='Power law fit')
    
        ax.set_ylabel(r"$p(X\geq x)$")
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc=3,fontsize=11)
        ax.set_title(measure_abbrev[measure])


.. parsed-literal::
    :class: myliteral

    Calculating best minimal value for power law fit
    Values less than or equal to 0 in data. Throwing out 0 or negative values
    Calculating best minimal value for power law fit
    Values less than or equal to 0 in data. Throwing out 0 or negative values
    Calculating best minimal value for power law fit
    Calculating best minimal value for power law fit
    Calculating best minimal value for power law fit
    Calculating best minimal value for power law fit
    


.. image:: /_static/img/network_analysis_48_1.png
    :scale: 100%

-  Outside of clustering coefficient (which is not a centrality
   measure), measures seem to exhibit the property of the Power-law
   distribution to an extent.
-  The `Google PageRank
   centrality <https://en.wikipedia.org/wiki/PageRank>`__ seems to
   exhibit the best fit.

PageRank Centrality among US Airports
-------------------------------------

-  let's identify the most important nodes according to the Google
   PageRank algorithm, one of the best known algorithms from Google that
   measures the importance of a node (site) in the world-wide-web graph.

.. code:: python

    measure = 'pagerank'
    
    # join data-table with pagerank with the lookup table (City_State is unique, so is a valid merge keu)
    df = df_network[measure].reset_index().rename(columns={'index':'City_State'})
    df = df.merge(df_lookup,on='City_State').sort_values(by=measure,ascending=False).reset_index(drop=True)
    df.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>City_State</th>
          <th>pagerank</th>
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
          <th>0</th>
          <td>Atlanta (GA)</td>
          <td>0.064983</td>
          <td>10397</td>
          <td>Atlanta, GA: Hartsfield-Jackson Atlanta Intern...</td>
          <td>Hartsfield-Jackson Atlanta International</td>
          <td>Atlanta</td>
          <td>GA</td>
          <td>South</td>
          <td>33.640728</td>
          <td>-84.427700</td>
        </tr>
        <tr>
          <th>1</th>
          <td>Chicago (IL) [O'Hare]</td>
          <td>0.044911</td>
          <td>13930</td>
          <td>Chicago, IL: Chicago O'Hare International</td>
          <td>Chicago O'Hare International</td>
          <td>Chicago</td>
          <td>IL</td>
          <td>Midwest</td>
          <td>41.974162</td>
          <td>-87.907321</td>
        </tr>
        <tr>
          <th>2</th>
          <td>Dallas/Fort Worth (TX)</td>
          <td>0.037017</td>
          <td>11298</td>
          <td>Dallas/Fort Worth, TX: Dallas/Fort Worth Inter...</td>
          <td>Dallas/Fort Worth International</td>
          <td>Dallas/Fort Worth</td>
          <td>TX</td>
          <td>South</td>
          <td>32.899809</td>
          <td>-97.040335</td>
        </tr>
        <tr>
          <th>3</th>
          <td>Denver (CO)</td>
          <td>0.036630</td>
          <td>11292</td>
          <td>Denver, CO: Denver International</td>
          <td>Denver International</td>
          <td>Denver</td>
          <td>CO</td>
          <td>West</td>
          <td>39.856096</td>
          <td>-104.673738</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Los Angeles (CA)</td>
          <td>0.029119</td>
          <td>12892</td>
          <td>Los Angeles, CA: Los Angeles International</td>
          <td>Los Angeles International</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>West</td>
          <td>33.941589</td>
          <td>-118.408530</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # remove illegal latitude locations from plotly
    # (everything outside 50states+DC...so drops Virgin Island, Guam,Puerto rico, etc)
    mask = df['lat']>=19
    df_filtered = df[mask].reset_index(drop=True)
    
    df_filtered = df_filtered.sort_values(by=[measure],ascending=False).reset_index(drop=True)
    add_ranking_hover_text(df_filtered,measure,'PageRank Score')

.. code:: python

    ranking_group = [(0,10),(10,25),(25,50),(50,100),(100,300)]
    scale = 0.00005 # scaling factor for the bubble plots
    
    # colors for each ranking group
    colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
    
    data = []
    for i in range(len(ranking_group)):
        lim = ranking_group[i]
        df_sub = df_filtered[lim[0]:lim[1]]
        airport = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub['lon'],lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(size = df_sub[measure]/scale,sizemode = 'area',
                color = colors[i],line = dict(width=0.5, color='rgb(40,40,40)'),),
            name = 'Top {0} - {1}'.format(lim[0]+1,lim[1]) )
        data.append(airport)
    
    layout = get_base_plotly_layout()
    layout['title'] = 'Top 300 airports based on Google PageRank Centrality ({})'.format(period)
    layout['title']+= '<br>(hover for airport info; click legend below to toggle on/off ranking-groups)'
    
    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename=outfile+'page_rank' )




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1955.embed?link=false&logo=false&share_key=b2DdhlljEH0JZMTRVPlUjf" height="525px" width="100%"></iframe>



Above plot is quite insightful!

As a Michigan native, proud to see Detroit Airport score in the top 10.

Communities Detected via Modularity Score
-----------------------------------------

We next analyze the **communities** of airports that were identified by
the `Girvan-Newman modularity
algorithm <https://en.wikipedia.org/wiki/Girvan%E2%80%93Newman_algorithm>`__.

A **community** describes a set of airports that tend to connect with
each other.

To gain geographical insight, we'll again display the results on the US
map.

.. code:: python

    measure = 'degree_bin' # make bubble size proportional to binary degree
    df = df_network[[measure,'module']].reset_index().rename(columns={'index':'City_State'})
    df = df.merge(df_lookup,on='City_State').sort_values(by=measure,ascending=False).reset_index(drop=True)
    display(df.head())
    
    # remove illegal latitude locations from plotly
    # (everything outside 50states+DC...so drops Virgin Island, Guam,Puerto rico, etc)
    mask = df['lat']>=19
    df_filtered = df[mask].reset_index(drop=True)
    
    df_filtered = df_filtered.sort_values(by=[measure],ascending=False).reset_index(drop=True)
    add_ranking_hover_text(df_filtered,measure,'Binary Degree')



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>City_State</th>
          <th>degree_bin</th>
          <th>module</th>
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
          <th>0</th>
          <td>Atlanta (GA)</td>
          <td>166</td>
          <td>Module 1</td>
          <td>10397</td>
          <td>Atlanta, GA: Hartsfield-Jackson Atlanta Intern...</td>
          <td>Hartsfield-Jackson Atlanta International</td>
          <td>Atlanta</td>
          <td>GA</td>
          <td>South</td>
          <td>33.640728</td>
          <td>-84.427700</td>
        </tr>
        <tr>
          <th>1</th>
          <td>Chicago (IL) [O'Hare]</td>
          <td>163</td>
          <td>Module 4</td>
          <td>13930</td>
          <td>Chicago, IL: Chicago O'Hare International</td>
          <td>Chicago O'Hare International</td>
          <td>Chicago</td>
          <td>IL</td>
          <td>Midwest</td>
          <td>41.974162</td>
          <td>-87.907321</td>
        </tr>
        <tr>
          <th>2</th>
          <td>Dallas/Fort Worth (TX)</td>
          <td>145</td>
          <td>Module 1</td>
          <td>11298</td>
          <td>Dallas/Fort Worth, TX: Dallas/Fort Worth Inter...</td>
          <td>Dallas/Fort Worth International</td>
          <td>Dallas/Fort Worth</td>
          <td>TX</td>
          <td>South</td>
          <td>32.899809</td>
          <td>-97.040335</td>
        </tr>
        <tr>
          <th>3</th>
          <td>Denver (CO)</td>
          <td>135</td>
          <td>Module 2</td>
          <td>11292</td>
          <td>Denver, CO: Denver International</td>
          <td>Denver International</td>
          <td>Denver</td>
          <td>CO</td>
          <td>West</td>
          <td>39.856096</td>
          <td>-104.673738</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Houston (TX) [G.Bush]</td>
          <td>122</td>
          <td>Module 1</td>
          <td>12266</td>
          <td>Houston, TX: George Bush Intercontinental/Houston</td>
          <td>George Bush Intercontinental/Houston</td>
          <td>Houston</td>
          <td>TX</td>
          <td>South</td>
          <td>29.990220</td>
          <td>-95.336783</td>
        </tr>
      </tbody>
    </table>
    </div>


.. code:: python

    community_group = sorted(df_filtered['module'].unique().tolist())
    scale = .2 # scaling factor for the bubble plots
    
    # colors for each community group
    colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)"]
    
    data = []
    for i,community in enumerate(community_group):
        df_sub = df_filtered.query('module == @community')
        airport = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub['lon'],lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(size = df_sub[measure]/scale,sizemode = 'area',
                color = colors[i],line = dict(width=0.5, color='rgb(40,40,40)'),),
            name = community
        )
        data.append(airport)
        
        layout = get_base_plotly_layout()
    layout['title'] = 'Communities detected among the US Airports using Louvain Modularity Algorithm'
    layout['title']+= '<br>(nodes scaled by binary degree; click legend below to toggle on/off community display)'
    
    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename=outfile+'communities' )




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1957.embed?link=false&logo=false&share_key=KybShvlrzWuZ5pwbUUwQOq" height="525px" width="100%"></iframe>



From the above chart, we can quickly see that the US airport community
is mostly based on geographical distance.

In fact, I was quite surprised to see how closely the communities
resemble the `four regions of the United
Stats <https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States>`__
assigned by the Census Bureau (Northeast, South, Midwest, and West
regions), which was fascinating since the Girvan-Newman modularity
algorithm was purely driven by the Airline traffic data. It could be
possible that policy-makers assign flight schedule based o these four
regions, but it was still cool to see the data pick this up.

Finally, it was interesting to see Washingto DC be part of the Western
region dominant red community.

Visualizing the airtraffics in Gephi
------------------------------------

We conclude our analysis by producing the overall graph structure in the
US airline by rendering the edges on the US map using
`Gephi <https://gephi.org/>`__.

To do this, we exported the Graph object in networkx as a GEXF (Graph
Exchange XML Format) file.

.. code:: python

    # export graph object with the module information for visualizing in Gephi
    nx.write_gexf(G, 'airtraffic_network.gexf')

Below are the result of the figures rendered in Gephi in SVG format.

.. code:: python

    from IPython.display import SVG, display
    display(SVG('./gephi/traffic_mainland.svg'))



.. image:: /_static/img/network_analysis_65_0.svg
    :scale: 100%

Finally, below we display only the *intra*-community edges to avoid
cluttering the figure with edges.

.. code:: python

    display(SVG('./gephi/traffic_mainland_intra_only.svg'))



.. image:: /_static/img/network_analysis_67_0.svg
    :scale: 100%

We can also obtain a hierarchical module/community by running another
recursion of community detection algorithm, as illustrated below.

.. code:: python

    display(SVG('./gephi/south.svg'))



.. image:: /_static/img/network_analysis_69_0.svg
    :scale: 100%

.. code:: python

    display(SVG('./gephi/midwest.svg'))



.. image:: /_static/img/network_analysis_70_0.svg
    :scale: 100%

.. code:: python

    display(SVG('./gephi/west.svg'))



.. image:: /_static/img/network_analysis_71_0.svg
    :scale: 100%

Other visualization charts that we created in Gephi is available at
https://github.com/wtak23/airtraffic/tree/master/final\_scripts/gephi

Conclusion
==========

As an overall concluding remark, I am glad I undertook this data science
project. 
I learned a lot about the seasonal and geographical trends present in  the US air-traffic system, and also became familiar about the network architecture of the sytem in terms of centrality and modularity. ,

I was also able to get my hands wet on utilizing variety of practical tools, such as included web-scraping, API querying, geocoding, visualization of network graphs, dataframe manipulation and data tidying, and creating
intuitive visualization charts that helps data to deliver the message to us analysts.
