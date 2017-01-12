Part 1. Air-traffic Count Analysis
""""""""""""""""""""""""""""""""""

The original ipython notebook can be downloaded from `here <http://nbviewer.jupyter.org/github/wtak23/airtraffic/blob/master/final_scripts/flight-count-analysis.ipynb>`__ .

.. contents:: `Page Contents`
   :depth: 2
   :local:

.. code:: python

    %matplotlib inline

.. code:: python

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn.apionly as sns
    import plotly
    import plotly.plotly as py
    import calendar
    
    from datetime import datetime
    from pprint import pprint
    from IPython.display import display
    
    import cufflinks as cf
    cf.set_config_file(theme='ggplot')
    
    import util
    
    # limit output to avoid cluttering screen
    pd.options.display.max_rows = 20

.. code:: python

    # name of output files to prepend with
    outfile = 'flight_count_analysis_'

Load and explore dataset
========================

Load the **airport data**, as well as the **lookup-table** I created
`here <http://takwatanabe.me/airtraffic/create_lookup_table.html>`__.

.. code:: python

    df_data = util.load_airport_data()
    period = '11/1/2015 to 10/31/2016'


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

    # make the "day_of_week" explicit
    hash_dayofweek = {1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'}
    df_data['DAY_OF_WEEK'] = df_data['DAY_OF_WEEK'].map(lambda key: hash_dayofweek[key])
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
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>4</td>
          <td>Wed</td>
          <td>14570</td>
          <td>13930</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>5</td>
          <td>Thu</td>
          <td>13930</td>
          <td>14057</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>6</td>
          <td>Fri</td>
          <td>13930</td>
          <td>14057</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>7</td>
          <td>Sat</td>
          <td>13930</td>
          <td>14057</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>8</td>
          <td>Sun</td>
          <td>13930</td>
          <td>14057</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_lookup = pd.read_csv('df_lookup.csv') # lookup table for the AIRPORT_ID above
    df_lookup.head()




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



.. code:: python

    # create hash-table to convert Airport "Code" to "City_State" 
    # (combination of city/state is verified to be unique with the scope of this dataset)
    hash_lookup = df_lookup.set_index('Code')['City_State'].to_dict()
    pprint({k: hash_lookup[k] for k in hash_lookup.keys()[:10]})
    
    # also create hash-table for airport names
    hash_airport = df_lookup.set_index('Code')['Airport'].to_dict()
    pprint({k: hash_airport[k] for k in hash_airport.keys()[:10]})


.. parsed-literal::
    :class: myliteral

    {10245: 'King Salmon (AK)',
     10754: 'Barrow (AK)',
     11267: 'Dayton (OH)',
     11274: 'Dubuque (IA)',
     11278: 'Washington (DC) [R.Reagan]',
     11778: 'Fort Smith (AR)',
     13230: 'Harrisburg (PA)',
     13830: 'Kahului (HI)',
     14696: 'South Bend (IN)',
     15412: 'Knoxville (TN)'}
    {10245: 'King Salmon Airport',
     10754: 'Wiley Post/Will Rogers Memorial',
     11267: 'James M Cox/Dayton International',
     11274: 'Dubuque Regional',
     11278: 'Ronald Reagan Washington National',
     11778: 'Fort Smith Regional',
     13230: 'Harrisburg International',
     13830: 'Kahului Airport',
     14696: 'South Bend International',
     15412: 'McGhee Tyson'}
    

Create Timeseries of Daily Flight Counts
========================================

-  Here, I would like to analyze the trend in the **total daily
   flights** in the United States.

-  To this end, we'll first construct a `Pandas
   TimeSeries <http://pandas.pydata.org/pandas-docs/stable/timeseries.html>`__
   DataFrame containing the daily Flight-count information.

.. code:: python

    # create a column containing "YEAR-MONTH-DAY"
    df_data['time'] = ( df_data['YEAR'].astype(str) + '-' 
                      + df_data['MONTH'].astype(str) + '-' 
                      + df_data['DAY_OF_MONTH'].astype(str))
    
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
          <th>time</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>4</td>
          <td>Wed</td>
          <td>14570</td>
          <td>13930</td>
          <td>2015-11-4</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>5</td>
          <td>Thu</td>
          <td>13930</td>
          <td>14057</td>
          <td>2015-11-5</td>
        </tr>
        <tr>
          <th>2</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>6</td>
          <td>Fri</td>
          <td>13930</td>
          <td>14057</td>
          <td>2015-11-6</td>
        </tr>
        <tr>
          <th>3</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>7</td>
          <td>Sat</td>
          <td>13930</td>
          <td>14057</td>
          <td>2015-11-7</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>8</td>
          <td>Sun</td>
          <td>13930</td>
          <td>14057</td>
          <td>2015-11-8</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # create time-series of airtraffic counts
    ts_flightcounts = df_data['time'].value_counts().to_frame(name='counts')
    ts_flightcounts.index = ts_flightcounts.index.to_datetime()
    ts_flightcounts.sort_index(inplace=True) # need to sort by date
    ts_flightcounts.head(8)




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
          <th>2015-11-01</th>
          <td>15652</td>
        </tr>
        <tr>
          <th>2015-11-02</th>
          <td>16596</td>
        </tr>
        <tr>
          <th>2015-11-03</th>
          <td>15918</td>
        </tr>
        <tr>
          <th>2015-11-04</th>
          <td>16363</td>
        </tr>
        <tr>
          <th>2015-11-05</th>
          <td>16619</td>
        </tr>
        <tr>
          <th>2015-11-06</th>
          <td>16600</td>
        </tr>
        <tr>
          <th>2015-11-07</th>
          <td>12793</td>
        </tr>
        <tr>
          <th>2015-11-08</th>
          <td>15679</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # explicitly add extra date-info as dataframe columns (to apply `groupby` later)
    ts_flightcounts['day']= ts_flightcounts.index.day
    ts_flightcounts['month']= ts_flightcounts.index.month
    ts_flightcounts['day_of_week'] = ts_flightcounts.index.dayofweek
    
    ts_flightcounts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>day</th>
          <th>month</th>
          <th>day_of_week</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2015-11-01</th>
          <td>15652</td>
          <td>1</td>
          <td>11</td>
          <td>6</td>
        </tr>
        <tr>
          <th>2015-11-02</th>
          <td>16596</td>
          <td>2</td>
          <td>11</td>
          <td>0</td>
        </tr>
        <tr>
          <th>2015-11-03</th>
          <td>15918</td>
          <td>3</td>
          <td>11</td>
          <td>1</td>
        </tr>
        <tr>
          <th>2015-11-04</th>
          <td>16363</td>
          <td>4</td>
          <td>11</td>
          <td>2</td>
        </tr>
        <tr>
          <th>2015-11-05</th>
          <td>16619</td>
          <td>5</td>
          <td>11</td>
          <td>3</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # `dayofweek` uses encoding Monday=0 ... Sunday=6...make this explicit
    ts_flightcounts['day_of_week'] = ts_flightcounts['day_of_week'].map({0:'Mon',
                                                                         1:'Tue',
                                                                         2:'Wed',
                                                                         3:'Thu',
                                                                         4:'Fri',
                                                                         5:'Sat',
                                                                         6:'Sun'}).astype(str)
    
    ts_flightcounts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>counts</th>
          <th>day</th>
          <th>month</th>
          <th>day_of_week</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2015-11-01</th>
          <td>15652</td>
          <td>1</td>
          <td>11</td>
          <td>Sun</td>
        </tr>
        <tr>
          <th>2015-11-02</th>
          <td>16596</td>
          <td>2</td>
          <td>11</td>
          <td>Mon</td>
        </tr>
        <tr>
          <th>2015-11-03</th>
          <td>15918</td>
          <td>3</td>
          <td>11</td>
          <td>Tue</td>
        </tr>
        <tr>
          <th>2015-11-04</th>
          <td>16363</td>
          <td>4</td>
          <td>11</td>
          <td>Wed</td>
        </tr>
        <tr>
          <th>2015-11-05</th>
          <td>16619</td>
          <td>5</td>
          <td>11</td>
          <td>Thu</td>
        </tr>
      </tbody>
    </table>
    </div>



Create interactive plot with plotly/cufflinks
---------------------------------------------

-  I am a huge fan of `plotly <http://plot.ly/python/>`__...brings the
   distance between the data and user closer together :)

.. code:: python

    # create hover_text object for plotly
    hover_text= (
        ts_flightcounts['month'].astype(str) 
        +  '/' + ts_flightcounts['day'].astype(str)
        + ' (' + ts_flightcounts['day_of_week'] + ')'
    ).tolist()
    print hover_text[:5]
    
    


.. parsed-literal::
    :class: myliteral

    ['11/1 (Sun)', '11/2 (Mon)', '11/3 (Tue)', '11/4 (Wed)', '11/5 (Thu)']
    

.. code:: python

    plt_options = dict(text=hover_text,color='pink')
    title = 'Daily Airflight Counts in the US between ' + period
    title+= '<br>(hover over plot for dates; left-click to zoom)'
    
    ts_flightcounts.iplot(y='counts',
                          filename=outfile+'plot_flightcounts',
                          title=title,
                          **plt_options)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1367.embed?link=false&logo=false&share_key=qgyP6TszCcdzevwP8jgO7E" height="525px" width="100%"></iframe>



-  From the above time-series plot, we can see that the trend in the
   Flight-counts looks to be obscured by the effect from the
   ``day_of_week``

-  (a clear cyclical trend appears in the time-series above)

-  By hovering over the above plot, we can observe that Saturday takes a
   *dip* downwards in flight-counts

-  (while this was somewhat expected, it's always nice to have the data
   reaffirm your intuition)

Study seasonal trend with rolling-averaged timeseries
-----------------------------------------------------

.. code:: python

    title = 'Daily Airflight Counts in the US between ' + period + ' with rolling-mean applied over 7day window'
    ts_flightcounts['counts'].rolling(window=7).mean().iplot(filename=outfile+'rolling_mean',title=title)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1837.embed?link=false&logo=false&share_key=uglr1NeXnqOQpWP8C23UW7" height="525px" width="100%"></iframe>



-  from the above plot, the summertime and end-of-the-year looks to have
   more flights (makes sense...vacation time)

Narrow focus on Honolulu Airport
--------------------------------

-  I'm curious to see the trensd in the flights to Honolulu airport

-  I would guess there would be more flight during the cold, winter
   period

.. code:: python

    honolulu = df_lookup.query('City == "Honolulu"')
    display(honolulu)
    code = honolulu['Code'].values[0]
    hawaii_flights = df_data.query('ORIGIN_AIRPORT_ID == @code or DEST_AIRPORT_ID == @code')
    hawaii_flights.sample(6).sort_index()



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
          <th>147</th>
          <td>12173</td>
          <td>Honolulu, HI: Honolulu International</td>
          <td>Honolulu International</td>
          <td>Honolulu</td>
          <td>HI</td>
          <td>West</td>
          <td>21.324513</td>
          <td>-157.925074</td>
          <td>Honolulu (HI)</td>
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
          <th>YEAR</th>
          <th>QUARTER</th>
          <th>MONTH</th>
          <th>DAY_OF_MONTH</th>
          <th>DAY_OF_WEEK</th>
          <th>ORIGIN_AIRPORT_ID</th>
          <th>DEST_AIRPORT_ID</th>
          <th>time</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>145291</th>
          <td>2015</td>
          <td>4</td>
          <td>12</td>
          <td>15</td>
          <td>Tue</td>
          <td>12173</td>
          <td>12892</td>
          <td>2015-12-15</td>
        </tr>
        <tr>
          <th>236668</th>
          <td>2015</td>
          <td>4</td>
          <td>12</td>
          <td>5</td>
          <td>Sat</td>
          <td>12173</td>
          <td>12982</td>
          <td>2015-12-5</td>
        </tr>
        <tr>
          <th>256048</th>
          <td>2016</td>
          <td>3</td>
          <td>8</td>
          <td>31</td>
          <td>Wed</td>
          <td>12173</td>
          <td>12758</td>
          <td>2016-8-31</td>
        </tr>
        <tr>
          <th>260987</th>
          <td>2016</td>
          <td>3</td>
          <td>7</td>
          <td>9</td>
          <td>Sat</td>
          <td>12173</td>
          <td>12402</td>
          <td>2016-7-9</td>
        </tr>
        <tr>
          <th>317478</th>
          <td>2016</td>
          <td>3</td>
          <td>9</td>
          <td>13</td>
          <td>Tue</td>
          <td>12173</td>
          <td>11618</td>
          <td>2016-9-13</td>
        </tr>
        <tr>
          <th>323943</th>
          <td>2016</td>
          <td>2</td>
          <td>5</td>
          <td>23</td>
          <td>Mon</td>
          <td>14771</td>
          <td>12173</td>
          <td>2016-5-23</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    hawaii_flights = hawaii_flights['time'].value_counts().to_frame(name='counts')
    hawaii_flights.index = hawaii_flights.index.to_datetime()
    hawaii_flights.sort_index(inplace=True) # need to sort by date
    
    plt_options = dict(text=hover_text,color='pink')
    title = 'Daily Airflight Counts at Honolulu Airport between ' + period
    title+= '<br>(hover over plot for dates; left-click to zoom)'
    
    hawaii_flights.iplot(y='counts',
                          filename=outfile+'plot_flightcounts_honolulu',
                          title=title,
                          **plt_options)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1959.embed?link=false&logo=false&share_key=NIoblG1lHUId8n8eMV81uW" height="525px" width="100%"></iframe>



-  contrary to my initial hypothesis, the peak flight counts at Honolulu
   Airport takes place more during the summer

-  the rolling-mean plot below shows that vacation period around new
   years and summer attracts the most flight (makes sense)

.. code:: python

    title = 'Daily Airflight Counts at Honolulu Airport between ' 
    title+= period + '<br>(rolling-mean applied over 7day window; left click to select zoom region)'
    hawaii_flights['counts'].rolling(window=7).mean().iplot(filename=outfile+'rolling_mean_honolulu',title=title)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1961.embed?link=false&logo=false&share_key=QekV0ZwAg0rPIdoQOsMy9n" height="525px" width="100%"></iframe>



Flight counts study by "day\_of\_week" and "month"
==================================================

-  to gain further insights in the patterns among the flight-counts
   across ``day_of_week`` and ``month``, let's create some
   **count-charts** via bar-graphs

Over entire year period
-----------------------

.. code:: python

    # dow = dayofweek
    flight_counts_dow = df_data['DAY_OF_WEEK'].value_counts().to_frame(name='flight-counts')
    flight_counts_dow = flight_counts_dow.reindex(['Sun','Mon','Tue','Wed','Thu','Fri','Sat']) # reorder rows by day-of-week
    
    flight_counts_month = df_data['MONTH'].value_counts().to_frame(name='flight-counts')
    flight_counts_month = flight_counts_month.reindex(range(1,13))  # reorder by month
    flight_counts_month.index = flight_counts_month.index.map(lambda num: calendar.month_abbr[num]) # replace number with string-of-month
    
    display(flight_counts_dow.T)
    display(flight_counts_month.T)



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Sun</th>
          <th>Mon</th>
          <th>Tue</th>
          <th>Wed</th>
          <th>Thu</th>
          <th>Fri</th>
          <th>Sat</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>flight-counts</th>
          <td>804731</td>
          <td>850170</td>
          <td>820609</td>
          <td>829558</td>
          <td>831454</td>
          <td>834372</td>
          <td>682079</td>
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
          <th>Jan</th>
          <th>Feb</th>
          <th>Mar</th>
          <th>Apr</th>
          <th>May</th>
          <th>Jun</th>
          <th>Jul</th>
          <th>Aug</th>
          <th>Sep</th>
          <th>Oct</th>
          <th>Nov</th>
          <th>Dec</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>flight-counts</th>
          <td>445827</td>
          <td>423889</td>
          <td>479122</td>
          <td>461630</td>
          <td>479358</td>
          <td>487637</td>
          <td>502457</td>
          <td>498347</td>
          <td>454878</td>
          <td>472626</td>
          <td>467972</td>
          <td>479230</td>
        </tr>
      </tbody>
    </table>
    </div>


.. code:: python

    title = 'Total US Flight-counts over "day_of_week" ({})'.format(period)
    flight_counts_dow.iplot(kind='bar',title=title,filename=outfile+'bar_by_dow')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1839.embed?link=false&logo=false&share_key=asTK6yNQPfpKSufetq0hUv" height="525px" width="100%"></iframe>



-  from the above plot, we see that Saturday definitely takes a huge dip
   in flight-counts.

.. code:: python

    title = 'Total US Flight-counts over "day_of_week" ({})'.format(period)
    flight_counts_month.iplot(kind='bar',title=title,filename=outfile+'bar_by_month')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1841.embed?link=false&logo=false&share_key=24ppDqw5nftiWmjIncDcd3" height="525px" width="100%"></iframe>



-  as we saw in the rolling-averaged timeseries plot, the above plot
   tells us that the summertime and end-of-the-year looks to have more
   flights (makes sense...vacation time)

Pivoting: analysis grouped by month and day\_of\_week
-----------------------------------------------------

.. code:: python

    df_counts_month = df_data.groupby(['MONTH','DAY_OF_WEEK',])['YEAR'].count().unstack()
    df_counts_month = df_counts_month[['Sun','Mon','Tue','Wed','Thu','Fri','Sat']] # reorder columns
    df_counts_month.index = df_counts_month.index.map(lambda num: calendar.month_abbr[num])
    df_counts_month




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th>DAY_OF_WEEK</th>
          <th>Sun</th>
          <th>Mon</th>
          <th>Tue</th>
          <th>Wed</th>
          <th>Thu</th>
          <th>Fri</th>
          <th>Sat</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Jan</th>
          <td>70654</td>
          <td>61028</td>
          <td>58273</td>
          <td>59036</td>
          <td>61044</td>
          <td>74138</td>
          <td>61654</td>
        </tr>
        <tr>
          <th>Feb</th>
          <td>54748</td>
          <td>76987</td>
          <td>59617</td>
          <td>60326</td>
          <td>61945</td>
          <td>62097</td>
          <td>48169</td>
        </tr>
        <tr>
          <th>Mar</th>
          <td>61115</td>
          <td>64094</td>
          <td>77364</td>
          <td>78285</td>
          <td>80333</td>
          <td>64145</td>
          <td>53786</td>
        </tr>
        <tr>
          <th>Apr</th>
          <td>61020</td>
          <td>64426</td>
          <td>62860</td>
          <td>63275</td>
          <td>64454</td>
          <td>80605</td>
          <td>64990</td>
        </tr>
        <tr>
          <th>May</th>
          <td>73918</td>
          <td>80141</td>
          <td>79913</td>
          <td>64065</td>
          <td>65144</td>
          <td>65187</td>
          <td>50990</td>
        </tr>
        <tr>
          <th>Jun</th>
          <td>64372</td>
          <td>67055</td>
          <td>66239</td>
          <td>82752</td>
          <td>83913</td>
          <td>67070</td>
          <td>56236</td>
        </tr>
        <tr>
          <th>Jul</th>
          <td>78665</td>
          <td>64712</td>
          <td>67158</td>
          <td>67429</td>
          <td>67717</td>
          <td>84935</td>
          <td>71841</td>
        </tr>
        <tr>
          <th>Aug</th>
          <td>63469</td>
          <td>83136</td>
          <td>81291</td>
          <td>82178</td>
          <td>66676</td>
          <td>66872</td>
          <td>54725</td>
        </tr>
        <tr>
          <th>Sep</th>
          <td>58264</td>
          <td>63402</td>
          <td>61955</td>
          <td>62463</td>
          <td>80059</td>
          <td>80204</td>
          <td>48531</td>
        </tr>
        <tr>
          <th>Oct</th>
          <td>76328</td>
          <td>79157</td>
          <td>62309</td>
          <td>63424</td>
          <td>64635</td>
          <td>64674</td>
          <td>62099</td>
        </tr>
        <tr>
          <th>Nov</th>
          <td>79587</td>
          <td>81315</td>
          <td>64102</td>
          <td>65775</td>
          <td>59947</td>
          <td>62624</td>
          <td>54622</td>
        </tr>
        <tr>
          <th>Dec</th>
          <td>62591</td>
          <td>64717</td>
          <td>79528</td>
          <td>80550</td>
          <td>75587</td>
          <td>61821</td>
          <td>54436</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    title = 'Total US Flight-counts over "day_of_week" over each month ({})'.format(period)
    df_counts_month.iplot(kind='bar',title=title,xTitle='Month',yTitle='Counts',filename=outfile+'bar2')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1843.embed?link=false&logo=false&share_key=wDgZZeXGfFeuDXteuK1L1C" height="525px" width="100%"></iframe>



-  the trend of Saturday having the smallest airflights holds generally
   true for each month
-  intereting exceptions at **January** and **July**...perhaps this is a
   common vacation period (so businessday trend is eliminated)?
-  for example, maybe there tends to be more family trips since children
   is on school vacation

Repeat analysis for NY, LA, and Vegas.
======================================

-  Now I'm curious to see what the trend looks like in major cities.

-  Let's repeat the above analysis for NY, LA, and Las Vegas

Data tidying
------------

-  We begin by "tidying" up our data so we have a data-structure that
   are amenable for plotting

-  First extract list of airports in these three cities

.. code:: python

    cities = ['New York','Los Angeles','Las Vegas']
    
    # get AIRPORT_ID codes corresponding to the above three cities
    df_lookup[ df_lookup['City'].isin(cities) ]




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
          <th>173</th>
          <td>12478</td>
          <td>New York, NY: John F. Kennedy International</td>
          <td>John F. Kennedy International</td>
          <td>New York</td>
          <td>NY</td>
          <td>Northeast</td>
          <td>40.641311</td>
          <td>-73.778139</td>
          <td>New York (NY) [JFK]</td>
        </tr>
        <tr>
          <th>181</th>
          <td>12889</td>
          <td>Las Vegas, NV: McCarran International</td>
          <td>McCarran International</td>
          <td>Las Vegas</td>
          <td>NV</td>
          <td>West</td>
          <td>36.084000</td>
          <td>-115.153739</td>
          <td>Las Vegas (NV)</td>
        </tr>
        <tr>
          <th>183</th>
          <td>12892</td>
          <td>Los Angeles, CA: Los Angeles International</td>
          <td>Los Angeles International</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>West</td>
          <td>33.941589</td>
          <td>-118.408530</td>
          <td>Los Angeles (CA)</td>
        </tr>
        <tr>
          <th>189</th>
          <td>12953</td>
          <td>New York, NY: LaGuardia</td>
          <td>LaGuardia</td>
          <td>New York</td>
          <td>NY</td>
          <td>Northeast</td>
          <td>40.776927</td>
          <td>-73.873966</td>
          <td>New York (NY) [Lag]</td>
        </tr>
      </tbody>
    </table>
    </div>



-  Well, both Houston and NY have multiple major airport.

-  For the sake of simplicity of our analysis, we'll combine the flight
   counts from these airports.

Below we create a dictionary that keeps track of the lsit of airports in
each city

.. code:: python

    # dictionary keeping track of list of Airport code for each city
    # (list-array used since there could be multiple airports in a city)
    # city_codes = {'New York':[12478, 12953],
    #               'Los Angeles' : [12892],
    #               'Las Vegas' : [12889]}
    city_codes = {}
    for city in cities:
        city_codes[city] = df_lookup[ df_lookup['City']== city ]['Code'].tolist()
    city_codes




.. parsed-literal::
    :class: myliteral

    {'Las Vegas': [12889], 'Los Angeles': [12892], 'New York': [12478, 12953]}



-  From the main dataframe, extract the flights that involve these three
   cities

.. code:: python

    def filter_by_codelist(df_data,code_list):
        mask1 = df_data['ORIGIN_AIRPORT_ID'].isin(code_list)
        mask2 = df_data['DEST_AIRPORT_ID'].isin(code_list)
        return df_data[mask1 | mask2]
    
    df_data_city = {city:[] for city in cities}
    
    for city in cities:
        print city
        city_code = city_codes[city]
        df_data_city[city] = filter_by_codelist(df_data, city_code)
        
        # sanity check
        display(df_data_city[city].sample(3))
        


.. parsed-literal::
    :class: myliteral

    New York
    


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
          <th>time</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>88104</th>
          <td>2016</td>
          <td>1</td>
          <td>2</td>
          <td>14</td>
          <td>Sun</td>
          <td>12478</td>
          <td>14986</td>
          <td>2016-2-14</td>
        </tr>
        <tr>
          <th>306364</th>
          <td>2016</td>
          <td>2</td>
          <td>4</td>
          <td>28</td>
          <td>Thu</td>
          <td>12953</td>
          <td>13930</td>
          <td>2016-4-28</td>
        </tr>
        <tr>
          <th>335411</th>
          <td>2016</td>
          <td>3</td>
          <td>9</td>
          <td>1</td>
          <td>Thu</td>
          <td>12953</td>
          <td>11292</td>
          <td>2016-9-1</td>
        </tr>
      </tbody>
    </table>
    </div>


.. parsed-literal::
    :class: myliteral

    Los Angeles
    


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
          <th>time</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>97887</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>19</td>
          <td>Thu</td>
          <td>10721</td>
          <td>12892</td>
          <td>2015-11-19</td>
        </tr>
        <tr>
          <th>369000</th>
          <td>2016</td>
          <td>4</td>
          <td>10</td>
          <td>30</td>
          <td>Sun</td>
          <td>12892</td>
          <td>14747</td>
          <td>2016-10-30</td>
        </tr>
        <tr>
          <th>182393</th>
          <td>2015</td>
          <td>4</td>
          <td>12</td>
          <td>28</td>
          <td>Mon</td>
          <td>12892</td>
          <td>10397</td>
          <td>2015-12-28</td>
        </tr>
      </tbody>
    </table>
    </div>


.. parsed-literal::
    :class: myliteral

    Las Vegas
    


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
          <th>time</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>429670</th>
          <td>2015</td>
          <td>4</td>
          <td>11</td>
          <td>21</td>
          <td>Sat</td>
          <td>12889</td>
          <td>14869</td>
          <td>2015-11-21</td>
        </tr>
        <tr>
          <th>181923</th>
          <td>2015</td>
          <td>4</td>
          <td>12</td>
          <td>27</td>
          <td>Sun</td>
          <td>12889</td>
          <td>14747</td>
          <td>2015-12-27</td>
        </tr>
        <tr>
          <th>337794</th>
          <td>2016</td>
          <td>1</td>
          <td>3</td>
          <td>14</td>
          <td>Mon</td>
          <td>12266</td>
          <td>12889</td>
          <td>2016-3-14</td>
        </tr>
      </tbody>
    </table>
    </div>


-  Finally, we can compute the total flight-counts in each of these
   cities by ``DAY_OF_WEEK`` and ``MONTH``

.. code:: python

    # dow = 'day of week'
    flight_counts_by_dow = []
    flight_counts_by_month = []
    for city in cities:
        flight_counts_by_dow.append( df_data_city[city]['DAY_OF_WEEK'].value_counts())
        flight_counts_by_month.append(df_data_city[city]['MONTH'].value_counts())
        
    flight_counts_by_dow   = pd.DataFrame(flight_counts_by_dow, index=cities)[['Sun','Mon','Tue','Wed','Thu','Fri','Sat']] # reorder columns
    flight_counts_by_month = pd.DataFrame(flight_counts_by_month,index=cities).rename(columns = lambda num: calendar.month_abbr[num])
    display(flight_counts_by_dow)
    display(flight_counts_by_month)



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Sun</th>
          <th>Mon</th>
          <th>Tue</th>
          <th>Wed</th>
          <th>Thu</th>
          <th>Fri</th>
          <th>Sat</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>New York</th>
          <td>54774</td>
          <td>59836</td>
          <td>57450</td>
          <td>58018</td>
          <td>58680</td>
          <td>58437</td>
          <td>43946</td>
        </tr>
        <tr>
          <th>Los Angeles</th>
          <td>60730</td>
          <td>63463</td>
          <td>60909</td>
          <td>61503</td>
          <td>62119</td>
          <td>62430</td>
          <td>51961</td>
        </tr>
        <tr>
          <th>Las Vegas</th>
          <td>43824</td>
          <td>44222</td>
          <td>42803</td>
          <td>43217</td>
          <td>43708</td>
          <td>44043</td>
          <td>39132</td>
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
          <th>Jan</th>
          <th>Feb</th>
          <th>Mar</th>
          <th>Apr</th>
          <th>May</th>
          <th>Jun</th>
          <th>Jul</th>
          <th>Aug</th>
          <th>Sep</th>
          <th>Oct</th>
          <th>Nov</th>
          <th>Dec</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>New York</th>
          <td>32104</td>
          <td>31092</td>
          <td>33700</td>
          <td>31911</td>
          <td>32788</td>
          <td>33710</td>
          <td>34540</td>
          <td>34666</td>
          <td>31638</td>
          <td>31519</td>
          <td>31387</td>
          <td>32086</td>
        </tr>
        <tr>
          <th>Los Angeles</th>
          <td>32833</td>
          <td>30814</td>
          <td>34609</td>
          <td>33986</td>
          <td>35385</td>
          <td>38150</td>
          <td>39835</td>
          <td>39447</td>
          <td>35055</td>
          <td>35979</td>
          <td>32922</td>
          <td>34100</td>
        </tr>
        <tr>
          <th>Las Vegas</th>
          <td>24491</td>
          <td>22844</td>
          <td>25465</td>
          <td>25045</td>
          <td>25883</td>
          <td>25586</td>
          <td>26112</td>
          <td>26075</td>
          <td>25156</td>
          <td>26312</td>
          <td>23809</td>
          <td>24171</td>
        </tr>
      </tbody>
    </table>
    </div>


-  good, we now have the apppropriate data-structure to construct
   desired plots :)

Plot results
------------

.. code:: python

    title = 'Flight-counts across "day_of_week" during {}'.format(period)
    flight_counts_by_dow.iplot(kind='bar',title=title,xTitle='City',yTitle='Counts',filename=outfile+'bar_dow_3cities')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1845.embed?link=false&logo=false&share_key=N480wj0Kp1fNvPZMpNBz4U" height="525px" width="100%"></iframe>



-  interesting to see flight-traffic in Las Vegas seems to be unaffected
   by ``day_of_week``...

-  now I'm curious to see what the monthly trend looks like...

.. code:: python

    title = 'Flight-counts across "month" during {}'.format(period)
    flight_counts_by_month.iplot(kind='bar',title=title,xTitle='City',yTitle='Counts',filename=outfile+'bar_month_3cities')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1847.embed?link=false&logo=false&share_key=SZpObOWiSOY56QLvixs3Rg" height="525px" width="100%"></iframe>



Create sublots of monthly flight-count trends for each city
-----------------------------------------------------------

.. code:: python

    df_monthly_counts_by_city = {city:[] for city in cities}
    for city in cities:
        df_monthly_counts_by_city[city] = df_data_city[city].groupby(['MONTH','DAY_OF_WEEK',])['YEAR'].count().unstack()[['Sun','Mon','Tue','Wed','Thu','Fri','Sat']]
        df_monthly_counts_by_city[city].index = df_monthly_counts_by_city[city].index.map(lambda num: calendar.month_abbr[num])
    
    df_monthly_counts_by_city = pd.concat(df_monthly_counts_by_city)
    print df_monthly_counts_by_city
    # df_monthly_counts_by_city.loc['New York'] # access city by multi-indexing by "levels"


.. parsed-literal::
    :class: myliteral

    DAY_OF_WEEK     Sun   Mon   Tue   Wed   Thu   Fri   Sat
    Las Vegas Jan  3940  3235  3169  3164  3283  4051  3649
              Feb  3062  4045  3115  3173  3273  3308  2868
              Mar  3313  3347  4029  4113  4245  3406  3012
              Apr  3374  3419  3335  3389  3452  4327  3749
              May  4097  4238  4225  3413  3470  3482  2958
              Jun  3468  3451  3420  4291  4342  3494  3120
              Jul  4220  3315  3408  3422  3472  4365  3910
              Aug  3422  4265  4200  4219  3441  3464  3064
              Sep  3309  3421  3382  3409  4338  4345  2952
              Oct  4342  4272  3403  3440  3505  3516  3834
    ...             ...   ...   ...   ...   ...   ...   ...
    New York  Mar  4158  4591  5547  5625  5777  4572  3430
              Apr  4120  4536  4379  4445  4545  5643  4243
              May  4978  5559  5519  4406  4520  4478  3328
              Jun  4373  4698  4650  5776  5918  4707  3588
              Jul  5350  4556  4701  4740  4747  5911  4535
              Aug  4351  5862  5708  5795  4708  4712  3530
              Sep  4050  4486  4319  4338  5653  5667  3125
              Oct  5068  5407  4108  4198  4414  4419  3905
              Nov  5278  5569  4410  4483  4103  4144  3400
              Dec  4103  4367  5394  5424  5116  4172  3510
    
    [36 rows x 7 columns]
    

-  Good, we're ready to make subplots

-  Some references

-  http://takwatanabe.me/data\_science/plotly\_pandas/Cufflinks%20-%20Pandas%20Like%20Visualization.html#id21

-  http://takwatanabe.me/data\_science/plotly\_layout/plotly-layout-options-subplots.html

-  http://stackoverflow.com/questions/26939121/how-to-avoid-duplicate-legend-labels-in-plotly-or-pass-custom-legend-labels

-  http://takwatanabe.me/data\_science/plotly\_layout/plotly-layout-options-legend.html

-  (self-remark) Maybe next time, **do not** try to make subplots with
   cufflinks...was a huge pain...

-  see
   http://takwatanabe.me/data\_science/plotly\_pandas/plotly-pandas-basic-charts.html#id2

.. code:: python

    figs = []
    skip_legend = False
    for city in cities:
        #print city
        #titles.append('Flight-counts over "day_of_week" over each month in {} <br>(during {})'.format(city,period))
        tmp_fig = df_monthly_counts_by_city.loc['New York'].iplot(kind='bar',asFigure=True)
        
        if skip_legend:
            for i in range(tmp_fig.data.__len__()):
                # have to access individual trace element to access this parameter...
                # (figuring this out took an atrocious amount of time....)
                tmp_fig.data[i]['showlegend'] = False
                
        figs.append(tmp_fig)
        skip_legend = True # <- to avoid duplicate legend (show legend for the first subplot only)
        
    # convert list of figures to subplot object
    subplots = cf.subplots(figs,shared_xaxes=True,subplot_titles=cities,shape=(3,1),vertical_spacing=0.05)
    subplots.layout['height'] = 1000
    subplots.layout['title']  = 'Monthly Flight-counts grouped over NY/LA/Vegas, "day_of_week" ({})'.format(period)
    cf.iplot(subplots,filename=outfile+'bar_3cities_by_month')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1849.embed?link=false&logo=false&share_key=Fz2ganoLsyJfWYderZDFKQ" height="1000px" width="100%"></iframe>



Which state had the most air traffics?
======================================

-  Now let's conduct a similar analysis by grouping over states

-  the code used below is nearly a carbon copy of the above (next-time,
   perhaps create a function to avoid repeating the same code)

Data tidying
------------

-  Again, we start by "tidying" our data so we have a data-structure
   that are amenable for plotting

-  We start by creating a dictionary that keeps a list of airports in
   each state

.. code:: python

    states = sorted(list(df_lookup['State'].unique()))
    
    state_codes = {}
    for state in states:
        # get list of AIRPORT_ID corresponding to this state
        state_codes[state] = df_lookup[ df_lookup['State'] == state]['Code'].tolist()
    
    # check if the last state in the above loop extracted the correct list of airports
    print state
    df_lookup[ df_lookup['Code'].isin(state_codes[state])] 


.. parsed-literal::
    :class: myliteral

    WY
    



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
          <th>75</th>
          <td>11097</td>
          <td>Cody, WY: Yellowstone Regional</td>
          <td>Yellowstone Regional</td>
          <td>Cody</td>
          <td>WY</td>
          <td>West</td>
          <td>44.520442</td>
          <td>-109.022579</td>
          <td>Cody (WY)</td>
        </tr>
        <tr>
          <th>78</th>
          <td>11122</td>
          <td>Casper, WY: Casper/Natrona County International</td>
          <td>Casper/Natrona County International</td>
          <td>Casper</td>
          <td>WY</td>
          <td>West</td>
          <td>42.897274</td>
          <td>-106.464850</td>
          <td>Casper (WY)</td>
        </tr>
        <tr>
          <th>125</th>
          <td>11865</td>
          <td>Gillette, WY: Gillette Campbell County</td>
          <td>Gillette Campbell County</td>
          <td>Gillette</td>
          <td>WY</td>
          <td>West</td>
          <td>44.291092</td>
          <td>-105.502221</td>
          <td>Gillette (WY)</td>
        </tr>
        <tr>
          <th>170</th>
          <td>12441</td>
          <td>Jackson, WY: Jackson Hole</td>
          <td>Jackson Hole</td>
          <td>Jackson</td>
          <td>WY</td>
          <td>West</td>
          <td>43.479929</td>
          <td>-110.762428</td>
          <td>Jackson (WY)</td>
        </tr>
        <tr>
          <th>180</th>
          <td>12888</td>
          <td>Laramie, WY: Laramie Regional</td>
          <td>Laramie Regional</td>
          <td>Laramie</td>
          <td>WY</td>
          <td>West</td>
          <td>41.320194</td>
          <td>-105.670345</td>
          <td>Laramie (WY)</td>
        </tr>
        <tr>
          <th>271</th>
          <td>14543</td>
          <td>Rock Springs, WY: Rock Springs Sweetwater County</td>
          <td>Rock Springs Sweetwater County</td>
          <td>Rock Springs</td>
          <td>WY</td>
          <td>West</td>
          <td>41.587464</td>
          <td>-109.202904</td>
          <td>Rock Springs (WY)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df_data_states = {state:[] for state in states}
    for state in states:
        df_data_states[state] = filter_by_codelist(df_data, state_codes[state])
        
    # dow = 'day of week'
    flight_counts_by_dow = []
    flight_counts_by_month = []
    for state in states:
        flight_counts_by_dow.append( df_data_states[state]['DAY_OF_WEEK'].value_counts())
        flight_counts_by_month.append(df_data_states[state]['MONTH'].value_counts())
        
    flight_counts_by_dow   = pd.DataFrame(flight_counts_by_dow, index=states)\
                                         [['Sun','Mon','Tue','Wed','Thu','Fri','Sat']] # reorder columns
    flight_counts_by_month = pd.DataFrame(flight_counts_by_month,index=states).\
                                          rename(columns = lambda num: calendar.month_abbr[num])
    display(flight_counts_by_dow.head())
    display(flight_counts_by_month.head())



.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Sun</th>
          <th>Mon</th>
          <th>Tue</th>
          <th>Wed</th>
          <th>Thu</th>
          <th>Fri</th>
          <th>Sat</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>AK</th>
          <td>7578.0</td>
          <td>7775.0</td>
          <td>7415.0</td>
          <td>7350.0</td>
          <td>7630.0</td>
          <td>7677.0</td>
          <td>7393.0</td>
        </tr>
        <tr>
          <th>AL</th>
          <td>7154.0</td>
          <td>7917.0</td>
          <td>7565.0</td>
          <td>7674.0</td>
          <td>7734.0</td>
          <td>7766.0</td>
          <td>5315.0</td>
        </tr>
        <tr>
          <th>AR</th>
          <td>4746.0</td>
          <td>5465.0</td>
          <td>5309.0</td>
          <td>5369.0</td>
          <td>5350.0</td>
          <td>5337.0</td>
          <td>3560.0</td>
        </tr>
        <tr>
          <th>AZ</th>
          <td>50097.0</td>
          <td>51292.0</td>
          <td>48255.0</td>
          <td>50236.0</td>
          <td>50543.0</td>
          <td>50824.0</td>
          <td>45005.0</td>
        </tr>
        <tr>
          <th>CA</th>
          <td>174652.0</td>
          <td>183544.0</td>
          <td>175707.0</td>
          <td>177915.0</td>
          <td>179338.0</td>
          <td>180126.0</td>
          <td>147463.0</td>
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
          <th>Jan</th>
          <th>Feb</th>
          <th>Mar</th>
          <th>Apr</th>
          <th>May</th>
          <th>Jun</th>
          <th>Jul</th>
          <th>Aug</th>
          <th>Sep</th>
          <th>Oct</th>
          <th>Nov</th>
          <th>Dec</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>AK</th>
          <td>3757.0</td>
          <td>3473.0</td>
          <td>3769.0</td>
          <td>3614.0</td>
          <td>4532.0</td>
          <td>5979.0</td>
          <td>6403.0</td>
          <td>6143.0</td>
          <td>4127.0</td>
          <td>3626.0</td>
          <td>3600.0</td>
          <td>3795.0</td>
        </tr>
        <tr>
          <th>AL</th>
          <td>3733.0</td>
          <td>3665.0</td>
          <td>4218.0</td>
          <td>4160.0</td>
          <td>4301.0</td>
          <td>4217.0</td>
          <td>4361.0</td>
          <td>4401.0</td>
          <td>4308.0</td>
          <td>4478.0</td>
          <td>4666.0</td>
          <td>4617.0</td>
        </tr>
        <tr>
          <th>AR</th>
          <td>2426.0</td>
          <td>2430.0</td>
          <td>2707.0</td>
          <td>2659.0</td>
          <td>2920.0</td>
          <td>2820.0</td>
          <td>2834.0</td>
          <td>2927.0</td>
          <td>2740.0</td>
          <td>2904.0</td>
          <td>3898.0</td>
          <td>3871.0</td>
        </tr>
        <tr>
          <th>AZ</th>
          <td>28703.0</td>
          <td>27053.0</td>
          <td>31670.0</td>
          <td>29159.0</td>
          <td>29590.0</td>
          <td>29642.0</td>
          <td>30367.0</td>
          <td>28903.0</td>
          <td>26002.0</td>
          <td>28383.0</td>
          <td>27579.0</td>
          <td>29201.0</td>
        </tr>
        <tr>
          <th>CA</th>
          <td>94693.0</td>
          <td>89079.0</td>
          <td>100383.0</td>
          <td>98335.0</td>
          <td>103366.0</td>
          <td>107574.0</td>
          <td>111746.0</td>
          <td>112351.0</td>
          <td>101604.0</td>
          <td>105013.0</td>
          <td>95710.0</td>
          <td>98891.0</td>
        </tr>
      </tbody>
    </table>
    </div>


.. code:: python

    # sanity check
    assert np.all(flight_counts_by_month.sum(axis=1) == flight_counts_by_dow.sum(axis=1))
     
    flight_counts = flight_counts_by_month.sum(axis=1).astype(int).to_frame(name='flight-counts')
    flight_counts.T




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>AK</th>
          <th>AL</th>
          <th>AR</th>
          <th>AZ</th>
          <th>CA</th>
          <th>CO</th>
          <th>CT</th>
          <th>DC</th>
          <th>DE</th>
          <th>FL</th>
          <th>...</th>
          <th>TT</th>
          <th>TX</th>
          <th>UT</th>
          <th>VA</th>
          <th>VI</th>
          <th>VT</th>
          <th>WA</th>
          <th>WI</th>
          <th>WV</th>
          <th>WY</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>flight-counts</th>
          <td>52818</td>
          <td>51125</td>
          <td>35136</td>
          <td>346252</td>
          <td>1218745</td>
          <td>479372</td>
          <td>40194</td>
          <td>226131</td>
          <td>0</td>
          <td>876232</td>
          <td>...</td>
          <td>976</td>
          <td>1041128</td>
          <td>218147</td>
          <td>66199</td>
          <td>12035</td>
          <td>8150</td>
          <td>283837</td>
          <td>103489</td>
          <td>5194</td>
          <td>17507</td>
        </tr>
      </tbody>
    </table>
    <p>1 rows × 54 columns</p>
    </div>



-  Cool, we're ready to plot

.. code:: python

    title = 'US airflight-counts across states " (during {})'.format(period)
    flight_counts.sort_values('flight-counts',ascending=False).iplot(kind='bar',title=title,filename=outfile+'bar_by_state')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1851.embed?link=false&logo=false&share_key=PNATJ4yJPiuILM772Cxu9L" height="525px" width="100%"></iframe>



Choropleth figure (display result on US map)
--------------------------------------------

-  Let's display the flight-count values we organized above into the US
   map

-  This form of visualization is nice as it also provide geographical
   information

-  To see how this can be done in Plotly, visit
   https://plot.ly/python/choropleth-maps/

.. code:: python

    states = flight_counts.index
    counts = flight_counts.values

.. code:: python

    # prepare Plotly "Data" and "Layout" object
    
    # took this colorscale from: https://plot.ly/python/choropleth-maps/
    colorscale = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
                  [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
    
    # define data object
    data = dict(
            type='choropleth',
            autocolorscale = False,
            #Greys, YlGnBu, Greens, YlOrRd, Bluered, RdBu, Reds, Blues, Picnic, Rainbow, Portland, Jet, Hot, Blackbody, Earth, Electric, Viridis
            colorscale = colorscale,
            locations = states,
            z = counts,
            locationmode = 'USA-states',
            marker = dict(line = dict (color = 'rgb(0,0,0)',width = 2) ),
            colorbar = dict(title = "flight-counts")
    )
    
    # define layout object
    geo = dict(scope='usa',
               projection=dict( type='albers usa' ),
               showlakes = True,
               lakecolor = 'rgb(255, 255, 255)'
              )
    
    title = 'US airflight-counts across states (during {})'.format(period)
    title+= '<br>(hover over to get count values)'
    layout = dict(geo=geo,
                  margin = dict(b=0,l=0,r=0,t=40),
                  title = title)
    
    fig = dict( data=[data], layout=layout )
    
    # alright, ready for plotting!
    py.iplot( fig , filename=outfile+'_choropleth')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1853.embed?link=false&logo=false&share_key=xcDy8dp7T93r2qLV5WLTCI" height="525px" width="100%"></iframe>



.. code:: python

    # what about during January? 
    data['z'] = flight_counts_by_month['Jan'].values
    layout['title'] = 'US airflight-counts across states during Jan,2016'
    py.iplot( fig , filename=outfile+'_choropleth_jan')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1855.embed?link=false&logo=false&share_key=wNO9k0tspaCCCR4aUjllda" height="525px" width="100%"></iframe>



Choropleth after normalizing over state population
--------------------------------------------------

-  I'm curious to see how the above plot will look after we scale by
   state population

-  Let's created a normalized chart using the US population data that I
   extracted from
   `Wikipedia <https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population>`__
   using
   `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`__

-  script:
   https://github.com/wtak23/airtraffic/blob/master/final\_scripts/get\_us\_state\_populations.py

.. code:: python

    # 2015 estimate of state population saved va script ``get_us_state_populations.py``
    df_state_popu = pd.read_csv('df_state_populations.csv')
    df_state_popu.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>state</th>
          <th>population</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>CA</td>
          <td>39250017</td>
        </tr>
        <tr>
          <th>1</th>
          <td>TX</td>
          <td>27862596</td>
        </tr>
        <tr>
          <th>2</th>
          <td>FL</td>
          <td>20612439</td>
        </tr>
        <tr>
          <th>3</th>
          <td>NY</td>
          <td>19745289</td>
        </tr>
        <tr>
          <th>4</th>
          <td>IL</td>
          <td>12801539</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # create a dataframe by applying inner-join with our flight-count dataframe
    flight_counts_popu = flight_counts.reset_index().rename(columns=dict(index='state')).merge(df_state_popu,on='state',how='inner')
    flight_counts_popu.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>state</th>
          <th>flight-counts</th>
          <th>population</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>AK</td>
          <td>52818</td>
          <td>741894</td>
        </tr>
        <tr>
          <th>1</th>
          <td>AL</td>
          <td>51125</td>
          <td>4863300</td>
        </tr>
        <tr>
          <th>2</th>
          <td>AR</td>
          <td>35136</td>
          <td>2988248</td>
        </tr>
        <tr>
          <th>3</th>
          <td>AZ</td>
          <td>346252</td>
          <td>6931071</td>
        </tr>
        <tr>
          <th>4</th>
          <td>CA</td>
          <td>1218745</td>
          <td>39250017</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # normalize by state population
    flight_counts_popu['normalized_flight_counts'] = flight_counts_popu['flight-counts'].astype(float)/flight_counts_popu['population']
    flight_counts_popu.sort_values('normalized_flight_counts',ascending=False).head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>state</th>
          <th>flight-counts</th>
          <th>population</th>
          <th>normalized_flight_counts</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>7</th>
          <td>DC</td>
          <td>226131</td>
          <td>681170</td>
          <td>0.331974</td>
        </tr>
        <tr>
          <th>33</th>
          <td>NV</td>
          <td>323313</td>
          <td>2940058</td>
          <td>0.109968</td>
        </tr>
        <tr>
          <th>11</th>
          <td>HI</td>
          <td>139771</td>
          <td>1428557</td>
          <td>0.097841</td>
        </tr>
        <tr>
          <th>5</th>
          <td>CO</td>
          <td>479372</td>
          <td>5540545</td>
          <td>0.086521</td>
        </tr>
        <tr>
          <th>10</th>
          <td>GA</td>
          <td>776731</td>
          <td>10310371</td>
          <td>0.075335</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    # took this colorscale from: https://plot.ly/python/choropleth-maps/
    colorscale = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
                  [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
    
    # define data object
    data = dict(
            type='choropleth',
            autocolorscale = False,
            colorscale = colorscale,
            locations = flight_counts_popu['state'].tolist(),
            z = flight_counts_popu['normalized_flight_counts'].values,
            locationmode = 'USA-states',
            marker = dict(line = dict (color = 'rgb(0,0,0)',width = 2), zmax=0.1 ),
            colorbar = dict(title = "flight-counts"),
            # --- customize heatmap scale --- #
            zauto=False, # <- took me forever to figure this out....argh...plotly api definitely has room for improvements...
            zmax=0.1
    )
    
    layout['title'] = 'US Airflight-counts normalized over state population ({})'.format(period)
    
    fig = dict( data=[data], layout=layout )
    py.iplot( fig , validate=False)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1963.embed?link=false&logo=false&share_key=rX1PkRx764wtdkfkuVyoJQ" height="525px" width="100%"></iframe>



(ignore, nothing interesting) Normalized flight-counts at different month?
--------------------------------------------------------------------------

.. code:: python

    # flight_counts_by_month2 = flight_counts_by_month.reset_index().rename(columns=dict(index='state')).merge(df_state_popu,on='state',how='inner')
    # flight_counts_by_month2.head()

.. code:: python

    # month = 'Aug'
    # data['z'] = (flight_counts_by_month2[month]/flight_counts_by_month2['population']).values
    # data['zmax'] = np.nanmax(data['z'])/3
    # layout['title'] = '(Month={}) US Airflight-counts normalized over state population ({})'.format(month,period)
    
    # py.iplot( fig , validate=False)

Most frequently used airports
=============================

-  To conclude this notebook, let's investigate which airports were used
   the most during the last one year period

Data tidying
------------

-  the traffic-counts for each airport is computed by adding the number
   of times it was used as an **origin** or **destination**

.. code:: python

    # number of times an airport was used as an origin
    flight_counts_orig = df_data['ORIGIN_AIRPORT_ID'].value_counts().to_frame(name='origin')
    
    # number of times an airport was used as a destination
    flight_counts_dest = df_data['DEST_AIRPORT_ID'].value_counts().to_frame(name='destination')
    
    # join the table, and get total flight counts by adding
    flight_counts = flight_counts_orig.join(flight_counts_dest,how='inner')
    flight_counts['flight_counts'] = flight_counts['origin'] + flight_counts['destination']
    flight_counts.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>origin</th>
          <th>destination</th>
          <th>flight_counts</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>10397</th>
          <td>384666</td>
          <td>384588</td>
          <td>769254</td>
        </tr>
        <tr>
          <th>13930</th>
          <td>257425</td>
          <td>257275</td>
          <td>514700</td>
        </tr>
        <tr>
          <th>11292</th>
          <td>225515</td>
          <td>225578</td>
          <td>451093</td>
        </tr>
        <tr>
          <th>12892</th>
          <td>211563</td>
          <td>211552</td>
          <td>423115</td>
        </tr>
        <tr>
          <th>11298</th>
          <td>205545</td>
          <td>205565</td>
          <td>411110</td>
        </tr>
      </tbody>
    </table>
    </div>



-  Ok, so we now have a dataframe with the airports ranked by
   flight-counts.

-  To gain more insights, let's join this dataframe with our lookup
   table.

.. code:: python

    df = flight_counts.join(df_lookup.set_index('Code'),how='inner').\
            sort_values('flight_counts',ascending=False).reset_index(drop=True)
    
    # print top 10 airports
    df.head(10)




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>origin</th>
          <th>destination</th>
          <th>flight_counts</th>
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
          <td>384666</td>
          <td>384588</td>
          <td>769254</td>
          <td>Atlanta, GA: Hartsfield-Jackson Atlanta Intern...</td>
          <td>Hartsfield-Jackson Atlanta International</td>
          <td>Atlanta</td>
          <td>GA</td>
          <td>South</td>
          <td>33.640728</td>
          <td>-84.427700</td>
          <td>Atlanta (GA)</td>
        </tr>
        <tr>
          <th>1</th>
          <td>257425</td>
          <td>257275</td>
          <td>514700</td>
          <td>Chicago, IL: Chicago O'Hare International</td>
          <td>Chicago O'Hare International</td>
          <td>Chicago</td>
          <td>IL</td>
          <td>Midwest</td>
          <td>41.974162</td>
          <td>-87.907321</td>
          <td>Chicago (IL) [O'Hare]</td>
        </tr>
        <tr>
          <th>2</th>
          <td>225515</td>
          <td>225578</td>
          <td>451093</td>
          <td>Denver, CO: Denver International</td>
          <td>Denver International</td>
          <td>Denver</td>
          <td>CO</td>
          <td>West</td>
          <td>39.856096</td>
          <td>-104.673738</td>
          <td>Denver (CO)</td>
        </tr>
        <tr>
          <th>3</th>
          <td>211563</td>
          <td>211552</td>
          <td>423115</td>
          <td>Los Angeles, CA: Los Angeles International</td>
          <td>Los Angeles International</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>West</td>
          <td>33.941589</td>
          <td>-118.408530</td>
          <td>Los Angeles (CA)</td>
        </tr>
        <tr>
          <th>4</th>
          <td>205545</td>
          <td>205565</td>
          <td>411110</td>
          <td>Dallas/Fort Worth, TX: Dallas/Fort Worth Inter...</td>
          <td>Dallas/Fort Worth International</td>
          <td>Dallas/Fort Worth</td>
          <td>TX</td>
          <td>South</td>
          <td>32.899809</td>
          <td>-97.040335</td>
          <td>Dallas/Fort Worth (TX)</td>
        </tr>
        <tr>
          <th>5</th>
          <td>171704</td>
          <td>171746</td>
          <td>343450</td>
          <td>San Francisco, CA: San Francisco International</td>
          <td>San Francisco International</td>
          <td>San Francisco</td>
          <td>CA</td>
          <td>West</td>
          <td>37.621313</td>
          <td>-122.378955</td>
          <td>San Francisco (CA)</td>
        </tr>
        <tr>
          <th>6</th>
          <td>158589</td>
          <td>158636</td>
          <td>317225</td>
          <td>Phoenix, AZ: Phoenix Sky Harbor International</td>
          <td>Phoenix Sky Harbor International</td>
          <td>Phoenix</td>
          <td>AZ</td>
          <td>West</td>
          <td>33.437269</td>
          <td>-112.007788</td>
          <td>Phoenix (AZ)</td>
        </tr>
        <tr>
          <th>7</th>
          <td>150470</td>
          <td>150479</td>
          <td>300949</td>
          <td>Las Vegas, NV: McCarran International</td>
          <td>McCarran International</td>
          <td>Las Vegas</td>
          <td>NV</td>
          <td>West</td>
          <td>36.084000</td>
          <td>-115.153739</td>
          <td>Las Vegas (NV)</td>
        </tr>
        <tr>
          <th>8</th>
          <td>140240</td>
          <td>140230</td>
          <td>280470</td>
          <td>Houston, TX: George Bush Intercontinental/Houston</td>
          <td>George Bush Intercontinental/Houston</td>
          <td>Houston</td>
          <td>TX</td>
          <td>South</td>
          <td>29.990220</td>
          <td>-95.336783</td>
          <td>Houston (TX) [G.Bush]</td>
        </tr>
        <tr>
          <th>9</th>
          <td>131934</td>
          <td>131941</td>
          <td>263875</td>
          <td>Seattle, WA: Seattle/Tacoma International</td>
          <td>Seattle/Tacoma International</td>
          <td>Seattle</td>
          <td>WA</td>
          <td>West</td>
          <td>47.450250</td>
          <td>-122.308817</td>
          <td>Seattle (WA)</td>
        </tr>
      </tbody>
    </table>
    </div>



-  Interesting. I never knew that Atlanta had the airport with the
   highest traffic counts!

Plot results
------------

Begin by creating "hovertext" object for plotly

.. code:: python

    # create hovertext with ranking information
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
    
    hover_text = df['Airport'] + '<br>' \
               + df['City'] + ', ' + df['State'] + '<br>' \
               + 'Number of flight: ' + df['flight_counts'].astype(str)
            
    df['text'] = (hover_text + '<br>' + map(string_rank,df.index+1)).tolist()
    pprint(df['text'].head().tolist())


.. parsed-literal::
    :class: myliteral

    ['Hartsfield-Jackson Atlanta International<br>Atlanta, GA<br>Number of flight: 769254<br>Ranking: 1st',
     "Chicago O'Hare International<br>Chicago, IL<br>Number of flight: 514700<br>Ranking: 2nd",
     'Denver International<br>Denver, CO<br>Number of flight: 451093<br>Ranking: 3rd',
     'Los Angeles International<br>Los Angeles, CA<br>Number of flight: 423115<br>Ranking: 4th',
     'Dallas/Fort Worth International<br>Dallas/Fort Worth, TX<br>Number of flight: 411110<br>Ranking: 5th']
    

.. code:: python

    title = 'Airports ranked by number of traffics between ' + period
    title+= '<br>(hover over plots for airport names; left-click to pan-zoom)'
    
    df[['flight_counts','City_State']].set_index('City_State').\
        sort_values('flight_counts',ascending=False).\
        iplot(kind='bar',text=df['text'].tolist(),color='pink',
              title=title,filename=outfile+'_traffic-rank')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1863.embed?link=false&logo=false&share_key=k0JiLH4nSRE9l2Rq60IOqZ" height="525px" width="100%"></iframe>



Display results on US Map
-------------------------

.. code:: python

    # welp, i faced the worst kind of bug...bug that doesn't throw any exception!
    # i learned the hard way that there apparently are some lat/lon values that
    # breaks plotly's hover functionality...took forever to figure this out through
    # trial and error....but it did produce pretty figure so i'm happy :)
    
    # drop entries with latitude lower than 18
    # (these are outside of the main US land area, such as Guam and the Virgin islands...
    #  which is probaby why breaks the hover functionality)
    mask = df['lat']>=19
    df_filtered = df[mask].reset_index(drop=True)
    print df_filtered.shape
    
    # the dropped airports
    display(df[~mask])


.. parsed-literal::
    :class: myliteral

    (309, 12)
    


.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>origin</th>
          <th>destination</th>
          <th>flight_counts</th>
          <th>Description</th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
          <th>Region</th>
          <th>lat</th>
          <th>lon</th>
          <th>City_State</th>
          <th>text</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>47</th>
          <td>27033</td>
          <td>27027</td>
          <td>54060</td>
          <td>San Juan, PR: Luis Munoz Marin International</td>
          <td>Luis Munoz Marin International</td>
          <td>San Juan</td>
          <td>PR</td>
          <td>NaN</td>
          <td>18.437355</td>
          <td>-66.004473</td>
          <td>San Juan (PR)</td>
          <td>Luis Munoz Marin International&lt;br&gt;San Juan, PR...</td>
        </tr>
        <tr>
          <th>110</th>
          <td>4940</td>
          <td>4940</td>
          <td>9880</td>
          <td>Charlotte Amalie, VI: Cyril E King</td>
          <td>Cyril E King</td>
          <td>Charlotte Amalie</td>
          <td>VI</td>
          <td>NaN</td>
          <td>18.336061</td>
          <td>-64.972273</td>
          <td>Charlotte Amalie (VI)</td>
          <td>Cyril E King&lt;br&gt;Charlotte Amalie, VI&lt;br&gt;Number...</td>
        </tr>
        <tr>
          <th>192</th>
          <td>1820</td>
          <td>1822</td>
          <td>3642</td>
          <td>Aguadilla, PR: Rafael Hernandez</td>
          <td>Rafael Hernandez</td>
          <td>Aguadilla</td>
          <td>PR</td>
          <td>NaN</td>
          <td>-34.549958</td>
          <td>-58.450550</td>
          <td>Aguadilla (PR)</td>
          <td>Rafael Hernandez&lt;br&gt;Aguadilla, PR&lt;br&gt;Number of...</td>
        </tr>
        <tr>
          <th>218</th>
          <td>1078</td>
          <td>1077</td>
          <td>2155</td>
          <td>Christiansted, VI: Henry E. Rohlsen</td>
          <td>Henry E. Rohlsen</td>
          <td>Christiansted</td>
          <td>VI</td>
          <td>NaN</td>
          <td>17.701287</td>
          <td>-64.805797</td>
          <td>Christiansted (VI)</td>
          <td>Henry E. Rohlsen&lt;br&gt;Christiansted, VI&lt;br&gt;Numbe...</td>
        </tr>
        <tr>
          <th>243</th>
          <td>853</td>
          <td>853</td>
          <td>1706</td>
          <td>Ponce, PR: Mercedita</td>
          <td>Mercedita</td>
          <td>Ponce</td>
          <td>PR</td>
          <td>NaN</td>
          <td>18.013893</td>
          <td>-66.549230</td>
          <td>Ponce (PR)</td>
          <td>Mercedita&lt;br&gt;Ponce, PR&lt;br&gt;Number of flight: 17...</td>
        </tr>
        <tr>
          <th>292</th>
          <td>367</td>
          <td>367</td>
          <td>734</td>
          <td>Guam, TT: Guam International</td>
          <td>Guam International</td>
          <td>Guam</td>
          <td>TT</td>
          <td>NaN</td>
          <td>13.485645</td>
          <td>144.800147</td>
          <td>Guam (TT)</td>
          <td>Guam International&lt;br&gt;Guam, TT&lt;br&gt;Number of fl...</td>
        </tr>
        <tr>
          <th>306</th>
          <td>121</td>
          <td>121</td>
          <td>242</td>
          <td>Pago Pago, TT: Pago Pago International</td>
          <td>Pago Pago International</td>
          <td>Pago Pago</td>
          <td>TT</td>
          <td>NaN</td>
          <td>-14.331389</td>
          <td>-170.711389</td>
          <td>Pago Pago (TT)</td>
          <td>Pago Pago International&lt;br&gt;Pago Pago, TT&lt;br&gt;Nu...</td>
        </tr>
        <tr>
          <th>316</th>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>Saipan, TT: Francisco C. Ada Saipan International</td>
          <td>Francisco C. Ada Saipan International</td>
          <td>Saipan</td>
          <td>TT</td>
          <td>NaN</td>
          <td>15.119743</td>
          <td>145.728279</td>
          <td>Saipan (TT)</td>
          <td>Francisco C. Ada Saipan International&lt;br&gt;Saipa...</td>
        </tr>
      </tbody>
    </table>
    </div>


.. code:: python

    # group each airport by ranking-group
    ranking_group = [(0,10),(10,25),(25,50),(50,100),(100,300)]
    
    # colors for each ranking group
    colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
    data = []
    scale = 1000 # scaling factor for the bubbles
    
    for i in range(len(ranking_group)):
        lim = ranking_group[i]
        df_sub = df_filtered[lim[0]:lim[1]]
        airport = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub['lon'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(
                size = df_sub['flight_counts']/scale,
                color = colors[i],
                line = dict(width=0.5, color='rgb(40,40,40)'),
                sizemode = 'area'
            ),
            name = 'Top {0} - {1}'.format(lim[0]+1,lim[1]) )
    #     if i == 0:
    # #         airport.update(dict(mode='markers+text'))
    #         airport['mode'] = 'markers+text'
    #         airport['textfont'] = dict(size=18),
    #         airport['textposition'] = "middle center",
        data.append(airport)
    
    title = 'Top 300 airports based on air-traffics during {}'.format(period)
    title+= '<br>(hover for airport info; click legend below to toggle airports by ranking-class)'
    
    layout = dict(
            title=title,
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
    
    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename=outfile+'_traffic_by_airport' )




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1865.embed?link=false&logo=false&share_key=7RDIKA9PJVI5HB2jeiKPGb" height="525px" width="100%"></iframe>


