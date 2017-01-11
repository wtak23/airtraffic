Air-traffic Count Analysis
""""""""""""""""""""""""""

The original ipython notebook can be downloaded from `here <http://nbviewer.jupyter.org/github/wtak23/airtraffic/blob/master/final_scripts/flight-count-analysis1.ipynb>`__ .

.. contents:: `Contents`
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
    outfile = 'flight_count_analysis1_'

Load data
=========

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
          <th>lat</th>
          <th>lon</th>
          <th>latlon</th>
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
          <td>40.651650</td>
          <td>-75.434746</td>
          <td>(40.651650399999994, -75.434746099999984)</td>
          <td>Allentown/Bethlehem/Easton (PA)</td>
        </tr>
        <tr>
          <th>1</th>
          <td>10136</td>
          <td>Abilene, TX: Abilene Regional</td>
          <td>Abilene Regional</td>
          <td>Abilene</td>
          <td>TX</td>
          <td>32.448736</td>
          <td>-99.733144</td>
          <td>(32.448736400000001, -99.733143900000002)</td>
          <td>Abilene (TX)</td>
        </tr>
        <tr>
          <th>2</th>
          <td>10140</td>
          <td>Albuquerque, NM: Albuquerque International Sun...</td>
          <td>Albuquerque International Sunport</td>
          <td>Albuquerque</td>
          <td>NM</td>
          <td>35.043333</td>
          <td>-106.612909</td>
          <td>(35.0433333, -106.6129085)</td>
          <td>Albuquerque (NM)</td>
        </tr>
        <tr>
          <th>3</th>
          <td>10141</td>
          <td>Aberdeen, SD: Aberdeen Regional</td>
          <td>Aberdeen Regional</td>
          <td>Aberdeen</td>
          <td>SD</td>
          <td>45.453458</td>
          <td>-98.417726</td>
          <td>(45.453458300000001, -98.417726099999996)</td>
          <td>Aberdeen (SD)</td>
        </tr>
        <tr>
          <th>4</th>
          <td>10146</td>
          <td>Albany, GA: Southwest Georgia Regional</td>
          <td>Southwest Georgia Regional</td>
          <td>Albany</td>
          <td>GA</td>
          <td>31.535671</td>
          <td>-84.193905</td>
          <td>(31.535671100000002, -84.193904900000007)</td>
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
    ts_flightcounts = pd.DataFrame(df_data['time'].value_counts()).rename(columns={'time':'counts'})
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

    # see https://plot.ly/pandas/line-charts/
    plt_options = dict(text=hover_text,color='pink')
    title = 'Daily Airflight Counts in the US between ' + period
    title+= '<br>(hover over plot for dates; left-click to zoom)'
    
    ts_flightcounts.iplot(y='counts',
                          filename=outfile+'plot_flightcounts',
                          title=title,
                          **plt_options)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1555.embed?link=false&logo=false" height="525px" width="100%"></iframe>



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

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1695.embed?link=false&logo=false" height="525px" width="100%"></iframe>



-  from the above plot, the summertime and end-of-the-year looks to have
   more flights (makes sense...vacation time)

Flight counts study by "day\_of\_week" and "month"
==================================================

-  to gain further insights in the patterns among the flight-counts
   across ``day_of_week`` and ``month``, let's create some
   **count-charts** via bar-graphs

Over entire year
----------------

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

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1683.embed?link=false&logo=false" height="525px" width="100%"></iframe>



-  from the above plot, we see that Saturday definitely takes a huge dip
   in flight-counts.

.. code:: python

    title = 'Total US Flight-counts over "day_of_week" ({})'.format(period)
    flight_counts_month.iplot(kind='bar',title=title,filename=outfile+'bar_by_month')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1685.embed?link=false&logo=false" height="525px" width="100%"></iframe>



-  as we saw in the rolling-averaged timeseries plot, the above plot
   tells us that the summertime and end-of-the-year looks to have more
   flights (makes sense...vacation time)

Apply pivoting to groupby month and day\_of\_week
-------------------------------------------------

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

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1599.embed?link=false&logo=false" height="525px" width="100%"></iframe>



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

-  First we'll "tidy" up our data so we have a data-structure that are
   amenable for plotting

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
          <th>lat</th>
          <th>lon</th>
          <th>latlon</th>
          <th>City_State</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>164</th>
          <td>12478</td>
          <td>New York, NY: John F. Kennedy International</td>
          <td>John F. Kennedy International</td>
          <td>New York</td>
          <td>NY</td>
          <td>40.641311</td>
          <td>-73.778139</td>
          <td>(40.641311100000003, -73.77813909999999)</td>
          <td>New York (NY) [JFK]</td>
        </tr>
        <tr>
          <th>172</th>
          <td>12889</td>
          <td>Las Vegas, NV: McCarran International</td>
          <td>McCarran International</td>
          <td>Las Vegas</td>
          <td>NV</td>
          <td>36.084000</td>
          <td>-115.153739</td>
          <td>(36.083999799999994, -115.15373889999999)</td>
          <td>Las Vegas (NV)</td>
        </tr>
        <tr>
          <th>174</th>
          <td>12892</td>
          <td>Los Angeles, CA: Los Angeles International</td>
          <td>Los Angeles International</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>33.941589</td>
          <td>-118.408530</td>
          <td>(33.941588899999999, -118.40853)</td>
          <td>Los Angeles (CA)</td>
        </tr>
        <tr>
          <th>180</th>
          <td>12953</td>
          <td>New York, NY: LaGuardia</td>
          <td>LaGuardia</td>
          <td>New York</td>
          <td>NY</td>
          <td>40.776927</td>
          <td>-73.873966</td>
          <td>(40.776927100000002, -73.873965900000016)</td>
          <td>New York (NY) [Lag]</td>
        </tr>
      </tbody>
    </table>
    </div>



-  Well, both Houston and NY have multiple major airport.

-  For the sake of simplicity of our analysis, we'll pool the flight
   counts from these airports.

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
          <th>141327</th>
          <td>2016</td>
          <td>1</td>
          <td>1</td>
          <td>15</td>
          <td>Fri</td>
          <td>12478</td>
          <td>10721</td>
          <td>2016-1-15</td>
        </tr>
        <tr>
          <th>51544</th>
          <td>2016</td>
          <td>3</td>
          <td>8</td>
          <td>8</td>
          <td>Mon</td>
          <td>12953</td>
          <td>10721</td>
          <td>2016-8-8</td>
        </tr>
        <tr>
          <th>47106</th>
          <td>2016</td>
          <td>2</td>
          <td>4</td>
          <td>8</td>
          <td>Fri</td>
          <td>11278</td>
          <td>12953</td>
          <td>2016-4-8</td>
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
          <th>317195</th>
          <td>2016</td>
          <td>3</td>
          <td>9</td>
          <td>15</td>
          <td>Thu</td>
          <td>12892</td>
          <td>13830</td>
          <td>2016-9-15</td>
        </tr>
        <tr>
          <th>176974</th>
          <td>2016</td>
          <td>2</td>
          <td>5</td>
          <td>23</td>
          <td>Mon</td>
          <td>12892</td>
          <td>13830</td>
          <td>2016-5-23</td>
        </tr>
        <tr>
          <th>383603</th>
          <td>2016</td>
          <td>1</td>
          <td>2</td>
          <td>19</td>
          <td>Fri</td>
          <td>12892</td>
          <td>11292</td>
          <td>2016-2-19</td>
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
          <th>370999</th>
          <td>2016</td>
          <td>2</td>
          <td>5</td>
          <td>2</td>
          <td>Mon</td>
          <td>14893</td>
          <td>12889</td>
          <td>2016-5-2</td>
        </tr>
        <tr>
          <th>399702</th>
          <td>2016</td>
          <td>1</td>
          <td>3</td>
          <td>10</td>
          <td>Thu</td>
          <td>12889</td>
          <td>14831</td>
          <td>2016-3-10</td>
        </tr>
        <tr>
          <th>389667</th>
          <td>2016</td>
          <td>2</td>
          <td>4</td>
          <td>11</td>
          <td>Mon</td>
          <td>15016</td>
          <td>12889</td>
          <td>2016-4-11</td>
        </tr>
      </tbody>
    </table>
    </div>


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
   desired plots

Plot results
------------

.. code:: python

    title = 'Flight-counts across "day_of_week" during {}'.format(period)
    flight_counts_by_dow.iplot(kind='bar',title=title,xTitle='City',yTitle='Counts',filename=outfile+'bar_dow_3cities')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1697.embed?link=false&logo=false" height="525px" width="100%"></iframe>



-  interesting to see flight-traffic in Las Vegas seems to be unaffected
   by ``day_of_week``...

-  now I'm curious to see what the monthly trend looks like...

.. code:: python

    title = 'Flight-counts across "month" during {}'.format(period)
    flight_counts_by_month.iplot(kind='bar',title=title,xTitle='City',yTitle='Counts',filename=outfile+'bar_month_3cities')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1699.embed?link=false&logo=false" height="525px" width="100%"></iframe>



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

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1681.embed?link=false&logo=false" height="1000px" width="100%"></iframe>



Which state had the most air traffics?
======================================

-  Now let's conduct a similar analysis by grouping over states

-  the code used below is nearly a carbon copy of the above (next-time,
   perhaps create a function to avoid repeating the same code)

Data tidying
------------

-  Again, we start by "tidying" our data so we have a data-structure
   that are amenable for plotting

.. code:: python

    states = sorted(list(df_lookup['State'].unique()))
    print states[:8]
    
    state_codes = {}
    for state in states:
        # get AIRPORT_ID codes corresponding to this state
        state_codes[state] = df_lookup[ df_lookup['State'] == state]['Code'].tolist()
    
    # below for sanity check
    print state
    df_lookup[ df_lookup['Code'].isin(state_codes[state])] 


.. parsed-literal::
    :class: myliteral

    ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC']
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
          <th>lat</th>
          <th>lon</th>
          <th>latlon</th>
          <th>City_State</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>69</th>
          <td>11097</td>
          <td>Cody, WY: Yellowstone Regional</td>
          <td>Yellowstone Regional</td>
          <td>Cody</td>
          <td>WY</td>
          <td>44.526342</td>
          <td>-109.056531</td>
          <td>(44.526342200000002, -109.05653079999999)</td>
          <td>Cody (WY)</td>
        </tr>
        <tr>
          <th>72</th>
          <td>11122</td>
          <td>Casper, WY: Casper/Natrona County International</td>
          <td>Casper/Natrona County International</td>
          <td>Casper</td>
          <td>WY</td>
          <td>42.866632</td>
          <td>-106.313081</td>
          <td>(42.866632000000003, -106.31308100000001)</td>
          <td>Casper (WY)</td>
        </tr>
        <tr>
          <th>118</th>
          <td>11865</td>
          <td>Gillette, WY: Gillette Campbell County</td>
          <td>Gillette Campbell County</td>
          <td>Gillette</td>
          <td>WY</td>
          <td>44.291092</td>
          <td>-105.502221</td>
          <td>(44.2910915, -105.50222050000001)</td>
          <td>Gillette (WY)</td>
        </tr>
        <tr>
          <th>161</th>
          <td>12441</td>
          <td>Jackson, WY: Jackson Hole</td>
          <td>Jackson Hole</td>
          <td>Jackson</td>
          <td>WY</td>
          <td>43.479929</td>
          <td>-110.762428</td>
          <td>(43.4799291, -110.76242820000002)</td>
          <td>Jackson (WY)</td>
        </tr>
        <tr>
          <th>171</th>
          <td>12888</td>
          <td>Laramie, WY: Laramie Regional</td>
          <td>Laramie Regional</td>
          <td>Laramie</td>
          <td>WY</td>
          <td>41.320194</td>
          <td>-105.670345</td>
          <td>(41.320193700000004, -105.67034469999999)</td>
          <td>Laramie (WY)</td>
        </tr>
        <tr>
          <th>258</th>
          <td>14543</td>
          <td>Rock Springs, WY: Rock Springs Sweetwater County</td>
          <td>Rock Springs Sweetwater County</td>
          <td>Rock Springs</td>
          <td>WY</td>
          <td>41.587464</td>
          <td>-109.202904</td>
          <td>(41.587464399999995, -109.2029043)</td>
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
        
    flight_counts_by_dow   = pd.DataFrame(flight_counts_by_dow, index=states)[['Sun','Mon','Tue','Wed','Thu','Fri','Sat']] # reorder columns
    flight_counts_by_month = pd.DataFrame(flight_counts_by_month,index=states).rename(columns = lambda num: calendar.month_abbr[num])
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
          <td>7578</td>
          <td>7775</td>
          <td>7415</td>
          <td>7350</td>
          <td>7630</td>
          <td>7677</td>
          <td>7393</td>
        </tr>
        <tr>
          <th>AL</th>
          <td>7154</td>
          <td>7917</td>
          <td>7565</td>
          <td>7674</td>
          <td>7734</td>
          <td>7766</td>
          <td>5315</td>
        </tr>
        <tr>
          <th>AR</th>
          <td>4746</td>
          <td>5465</td>
          <td>5309</td>
          <td>5369</td>
          <td>5350</td>
          <td>5337</td>
          <td>3560</td>
        </tr>
        <tr>
          <th>AZ</th>
          <td>50097</td>
          <td>51292</td>
          <td>48255</td>
          <td>50236</td>
          <td>50543</td>
          <td>50824</td>
          <td>45005</td>
        </tr>
        <tr>
          <th>CA</th>
          <td>174652</td>
          <td>183544</td>
          <td>175707</td>
          <td>177915</td>
          <td>179338</td>
          <td>180126</td>
          <td>147463</td>
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
          <td>3757</td>
          <td>3473</td>
          <td>3769</td>
          <td>3614</td>
          <td>4532</td>
          <td>5979</td>
          <td>6403</td>
          <td>6143</td>
          <td>4127</td>
          <td>3626</td>
          <td>3600</td>
          <td>3795</td>
        </tr>
        <tr>
          <th>AL</th>
          <td>3733</td>
          <td>3665</td>
          <td>4218</td>
          <td>4160</td>
          <td>4301</td>
          <td>4217</td>
          <td>4361</td>
          <td>4401</td>
          <td>4308</td>
          <td>4478</td>
          <td>4666</td>
          <td>4617</td>
        </tr>
        <tr>
          <th>AR</th>
          <td>2426</td>
          <td>2430</td>
          <td>2707</td>
          <td>2659</td>
          <td>2920</td>
          <td>2820</td>
          <td>2834</td>
          <td>2927</td>
          <td>2740</td>
          <td>2904</td>
          <td>3898</td>
          <td>3871</td>
        </tr>
        <tr>
          <th>AZ</th>
          <td>28703</td>
          <td>27053</td>
          <td>31670</td>
          <td>29159</td>
          <td>29590</td>
          <td>29642</td>
          <td>30367</td>
          <td>28903</td>
          <td>26002</td>
          <td>28383</td>
          <td>27579</td>
          <td>29201</td>
        </tr>
        <tr>
          <th>CA</th>
          <td>94693</td>
          <td>89079</td>
          <td>100383</td>
          <td>98335</td>
          <td>103366</td>
          <td>107574</td>
          <td>111746</td>
          <td>112351</td>
          <td>101604</td>
          <td>105013</td>
          <td>95710</td>
          <td>98891</td>
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
          <th>FL</th>
          <th>GA</th>
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
          <td>876232</td>
          <td>776731</td>
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
    <p>1 rows × 53 columns</p>
    </div>



-  Cool, we're ready to plot

.. code:: python

    title = 'US airflight-counts across states " (during {})'.format(period)
    flight_counts.sort_values('flight-counts',ascending=False).iplot(kind='bar',title=title,filename=outfile+'bar_by_state')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1705.embed?link=false&logo=false" height="525px" width="100%"></iframe>



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

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1707.embed?share_key=IFdLfrSEUYGHVEAJ8CZu9V&link=false&logo=false" height="525px" width="100%"></iframe>



.. code:: python

    # what about during January? 
    data['z'] = flight_counts_by_month['Jan'].values
    layout['title'] = 'US airflight-counts across states during Jan,2016'
    py.iplot( fig , filename=outfile+'_choropleth_jan')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1711.embed?share_key=j4uABK8kQlGgUd29yZGkCj&link=false&logo=false" height="525px" width="100%"></iframe>




Choropleth after normalizing over state population
--------------------------------------------------

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
          <th>32</th>
          <td>NV</td>
          <td>323313</td>
          <td>2940058</td>
          <td>0.109968</td>
        </tr>
        <tr>
          <th>10</th>
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
          <th>9</th>
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

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1781.embed?share_key=qIQQ6Y94YA9V3gGhcjukom&link=false&logo=false" height="525px" width="100%"></iframe>



Normalized flight-counts at different month?
--------------------------------------------

.. code:: python

    flight_counts_by_month2 = flight_counts_by_month.reset_index().rename(columns=dict(index='state')).merge(df_state_popu,on='state',how='inner')
    flight_counts_by_month2.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>state</th>
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
          <th>population</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>AK</td>
          <td>3757</td>
          <td>3473</td>
          <td>3769</td>
          <td>3614</td>
          <td>4532</td>
          <td>5979</td>
          <td>6403</td>
          <td>6143</td>
          <td>4127</td>
          <td>3626</td>
          <td>3600</td>
          <td>3795</td>
          <td>741894</td>
        </tr>
        <tr>
          <th>1</th>
          <td>AL</td>
          <td>3733</td>
          <td>3665</td>
          <td>4218</td>
          <td>4160</td>
          <td>4301</td>
          <td>4217</td>
          <td>4361</td>
          <td>4401</td>
          <td>4308</td>
          <td>4478</td>
          <td>4666</td>
          <td>4617</td>
          <td>4863300</td>
        </tr>
        <tr>
          <th>2</th>
          <td>AR</td>
          <td>2426</td>
          <td>2430</td>
          <td>2707</td>
          <td>2659</td>
          <td>2920</td>
          <td>2820</td>
          <td>2834</td>
          <td>2927</td>
          <td>2740</td>
          <td>2904</td>
          <td>3898</td>
          <td>3871</td>
          <td>2988248</td>
        </tr>
        <tr>
          <th>3</th>
          <td>AZ</td>
          <td>28703</td>
          <td>27053</td>
          <td>31670</td>
          <td>29159</td>
          <td>29590</td>
          <td>29642</td>
          <td>30367</td>
          <td>28903</td>
          <td>26002</td>
          <td>28383</td>
          <td>27579</td>
          <td>29201</td>
          <td>6931071</td>
        </tr>
        <tr>
          <th>4</th>
          <td>CA</td>
          <td>94693</td>
          <td>89079</td>
          <td>100383</td>
          <td>98335</td>
          <td>103366</td>
          <td>107574</td>
          <td>111746</td>
          <td>112351</td>
          <td>101604</td>
          <td>105013</td>
          <td>95710</td>
          <td>98891</td>
          <td>39250017</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    month = 'Dec'
    data['z'] = (flight_counts_by_month2[month]/flight_counts_by_month2['population']).values
    data['zmax'] = np.nanmax(data['z'])/3
    layout['title'] = '(Month={}) US Airflight-counts normalized over state population ({})'.format(month,period)
    
    py.iplot( fig , validate=False)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1783.embed?share_key=QRYw7NDGr2G5PMGm9MSajW&link=false&logo=false" height="525px" width="100%"></iframe>



.. code:: python

    month = 'Aug'
    data['z'] = (flight_counts_by_month2[month]/flight_counts_by_month2['population']).values
    data['zmax'] = np.nanmax(data['z'])/3
    layout['title'] = '(Month={}) US Airflight-counts normalized over state population ({})'.format(month,period)
    
    py.iplot( fig , validate=False)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1785.embed?share_key=Uiy7WdUz3xUOwqu6w8hyBS&link=false&logo=false" height="525px" width="100%"></iframe>



Flight-counts by airport
========================

.. code:: python

    flight_counts_orig = df_data['ORIGIN_AIRPORT_ID'].value_counts().to_frame(name='origin')
    flight_counts_dest = df_data['DEST_AIRPORT_ID'].value_counts().to_frame(name='destination')
    
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



.. code:: python

    df = flight_counts.join(df_lookup.set_index('Code'),how='inner').sort_values('flight_counts',ascending=False).reset_index()
    df.head()




.. raw:: html

    <div>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>index</th>
          <th>origin</th>
          <th>destination</th>
          <th>flight_counts</th>
          <th>Description</th>
          <th>Airport</th>
          <th>City</th>
          <th>State</th>
          <th>lat</th>
          <th>lon</th>
          <th>latlon</th>
          <th>City_State</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>10397</td>
          <td>384666</td>
          <td>384588</td>
          <td>769254</td>
          <td>Atlanta, GA: Hartsfield-Jackson Atlanta Intern...</td>
          <td>Hartsfield-Jackson Atlanta International</td>
          <td>Atlanta</td>
          <td>GA</td>
          <td>33.748995</td>
          <td>-84.387982</td>
          <td>(33.748995399999998, -84.387982399999999)</td>
          <td>Atlanta (GA)</td>
        </tr>
        <tr>
          <th>1</th>
          <td>13930</td>
          <td>257425</td>
          <td>257275</td>
          <td>514700</td>
          <td>Chicago, IL: Chicago O'Hare International</td>
          <td>Chicago O'Hare International</td>
          <td>Chicago</td>
          <td>IL</td>
          <td>41.974162</td>
          <td>-87.907321</td>
          <td>(41.974162499999998, -87.907321400000001)</td>
          <td>Chicago (IL) [O'Hare]</td>
        </tr>
        <tr>
          <th>2</th>
          <td>11292</td>
          <td>225515</td>
          <td>225578</td>
          <td>451093</td>
          <td>Denver, CO: Denver International</td>
          <td>Denver International</td>
          <td>Denver</td>
          <td>CO</td>
          <td>39.856096</td>
          <td>-104.673738</td>
          <td>(39.856096299999997, -104.6737376)</td>
          <td>Denver (CO)</td>
        </tr>
        <tr>
          <th>3</th>
          <td>12892</td>
          <td>211563</td>
          <td>211552</td>
          <td>423115</td>
          <td>Los Angeles, CA: Los Angeles International</td>
          <td>Los Angeles International</td>
          <td>Los Angeles</td>
          <td>CA</td>
          <td>33.941589</td>
          <td>-118.408530</td>
          <td>(33.941588899999999, -118.40853)</td>
          <td>Los Angeles (CA)</td>
        </tr>
        <tr>
          <th>4</th>
          <td>11298</td>
          <td>205545</td>
          <td>205565</td>
          <td>411110</td>
          <td>Dallas/Fort Worth, TX: Dallas/Fort Worth Inter...</td>
          <td>Dallas/Fort Worth International</td>
          <td>Dallas/Fort Worth</td>
          <td>TX</td>
          <td>32.899809</td>
          <td>-97.040335</td>
          <td>(32.899809099999999, -97.040335200000001)</td>
          <td>Dallas/Fort Worth (TX)</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: python

    df[['flight_counts','City_State']].set_index('City_State').sort_values('flight_counts',ascending=False).iplot(kind='bar',text=hover_text,color='pink')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" width="100%" height="500" frameborder="0" scrolling="no" src="https://plot.ly/~takanori/1795.embed?link=false&logo=false"></iframe>



.. code:: python

    # welp, i faced the worth kind of bug...bug that doesn't throw any exception!
    # i learned the hard way that there apparently are some lat/lon values that
    # breaks plotly's hover functionality...took forever to figure this out through
    # trial and error....but it did produce pretty figure so i'm happy :)
    df = df[df['lat']>=20].reset_index(drop=True)
    df.shape




.. parsed-literal::
    :class: myliteral

    (307, 12)



.. code:: python

    df['text'] = df['Airport'] + '<br>' \
               + df['City'] + ', ' + df['State'] + '<br>' \
               + df['flight_counts'].astype(str) + 'flights'
    limits = [(0,10),(10,25),(25,50),(50,100),(100,300)]
    colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
    data = []
    scale = 1000
    
    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
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
    title+= '<br>(click legend below to toggle airports by ranking-class)'
    
    layout = dict(
            title=title,
            showlegend = True,
            legend = dict(
                font = dict(size=11),
                #bordercolor='rgb(0,0,0)',
                #borderwidth=1,
                orientation='h',
                x=0.5, y = 1, 
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
            margin = dict(b=0,l=0,r=0,t=60),
        )
    
    fig = dict( data=data, layout=layout )
    py.iplot( fig, validate=False, filename=outfile+'_traffic_by_airport' )




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1779.embed?share_key=xkV9WAnsiywgPQQgk2lE0h&link=false&logo=false" height="525px" width="100%"></iframe>


