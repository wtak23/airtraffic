Part2: Holiday Detction via Regression and Residual Analysis
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The original ipython notebook can be downloaded from `here <http://nbviewer.jupyter.org/github/wtak23/airtraffic/blob/master/final_scripts/regressing_out_weekday_effect.ipynb>`__ .

.. contents:: `Page Contents`
   :depth: 2
   :local:

Aim of this notebook
====================

-  In our `air-traffic count
   analysis <http://takwatanabe.me/airtraffic/flight-count-analysis1.html>`__,
   we found from the following plot that when the time-series signal of
   the airtraffic-counts is heavily influenced by "*what day of the week
   it is*.", indicating that people tend to fly out less especially on
   Saturdays.

-  This ``day_of_week`` effect seems to obscure away interesting trend
   in our data.

.. code:: python

    from IPython.core.display import display, HTML
    display(HTML('<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1555.embed?link=false&logo=false" height="525px" width="100%"></iframe>'))



.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1555.embed?link=false&logo=false" height="525px" width="100%"></iframe>


-  So in this notebook, we'll aim to **linearly regress out** the effect
   of ``day_of_week`` by using a linear regression model

-  The regressors will be the ``day_of_week``, encoded by a categorical
   `dummy
   variables <https://en.wikipedia.org/wiki/Dummy_variable_(statistics)>`__
   (called ``factor`` in R)

.. code:: python

    %matplotlib inline
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn.apionly as sns
    import plotly.plotly as py
    import calendar
    
    from datetime import datetime
    from pprint import pprint
    from IPython.display import display
    
    import cufflinks as cf
    cf.set_config_file(theme='ggplot',sharing='secret')
    
    import util
    
    # limit output to avoid cluttering screen
    pd.options.display.max_rows = 20

.. code:: python

    # name of output files to prepend with
    outfile = 'regressing_out_weekday_effect'
    period = '11/1/2015 to 10/31/2016' #range of our analysis

Load data, and prepare Timeseries
=================================

-  Here I'll quickly repeat the procedure I took in my previous notebook
   (`link <http://takwatanabe.me/airtraffic/flight-count-analysis1.html#create-timeseries-of-daily-flight-counts>`__)

.. code:: python

    df_data = util.load_airport_data()
    
    hash_dayofweek = {1:'Mon', 2:'Tue', 3:'Wed', 4:'Thu', 5:'Fri', 6:'Sat', 7:'Sun'}
    df_data['DAY_OF_WEEK'] = df_data['DAY_OF_WEEK'].map(lambda key: hash_dayofweek[key])


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

    # lookup table for the AIRPORT_ID
    df_lookup = pd.read_csv('df_lookup.csv') 
    
    # create hash-table to convert Airport "Code" to "City_State" and "Airport-name" 
    hash_lookup = df_lookup.set_index('Code')['City_State'].to_dict()
    hash_airport = df_lookup.set_index('Code')['Airport'].to_dict()

.. code:: python

    # create a column containing "YEAR-MONTH-DAY" info
    df_data['time'] = ( df_data['YEAR'].astype(str) + '-' 
                      + df_data['MONTH'].astype(str) + '-' 
                      + df_data['DAY_OF_MONTH'].astype(str))
    

.. code:: python

    # now we can create time-series of airtraffic counts
    ts_flightcounts = pd.DataFrame(df_data['time'].value_counts()).\
        rename(columns={'time':'counts'})
    ts_flightcounts.index = ts_flightcounts.index.to_datetime()
    ts_flightcounts.sort_index(inplace=True) # need to sort by date
    
    # explicitly add extra date-info as dataframe columns (to apply `groupby` later)
    ts_flightcounts['day']= ts_flightcounts.index.day
    ts_flightcounts['month']= ts_flightcounts.index.month
    ts_flightcounts['day_of_week'] = ts_flightcounts.index.dayofweek
    
    # `dayofweek` uses encoding Monday=0 ... Sunday=6...make this explicit
    ts_flightcounts['day_of_week'] = ts_flightcounts['day_of_week'].map({0:'Mon',
                                                                         1:'Tue',
                                                                         2:'Wed',
                                                                         3:'Thu',
                                                                         4:'Fri',
                                                                         5:'Sat',
                                                                         6:'Sun'}).astype(str)
    
    # create hover_text object for plotly
    hover_text= (
        ts_flightcounts['month'].astype(str) 
        + '/'  + ts_flightcounts['day'].astype(str)
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


-  Ok, we are in business. Let's next run our regression analysis.

Regression analysis: eliminate effect from "day\_of\_week"
==========================================================

-  Here we will apply linear regression using ``day_of_week`` encoded by
   dummy-variables as the regressors.

-  By studying the residual-timeseries from this regression, we hope to
   identify interesting trends that are buried under the dominant effect
   of ``day_of_week``

Fit OLS model
-------------

.. code:: python

    # i love statsmodels, as it allows me to apply R like syntax
    import statsmodels.formula.api as smf
    
    # fit OLS model using categorical variables without intercept 
    # (so all dummy-variables receive a binary encoder in the design matrix)
    mod = smf.ols(formula = 'counts ~ C(day_of_week) - 1',data=ts_flightcounts).fit()
    
    mod.summary()




.. raw:: html

    <table class="simpletable">
    <caption>OLS Regression Results</caption>
    <tr>
      <th>Dep. Variable:</th>         <td>counts</td>      <th>  R-squared:         </th> <td>   0.553</td>
    </tr>
    <tr>
      <th>Model:</th>                   <td>OLS</td>       <th>  Adj. R-squared:    </th> <td>   0.545</td>
    </tr>
    <tr>
      <th>Method:</th>             <td>Least Squares</td>  <th>  F-statistic:       </th> <td>   73.96</td>
    </tr>
    <tr>
      <th>Date:</th>             <td>Wed, 11 Jan 2017</td> <th>  Prob (F-statistic):</th> <td>9.34e-60</td>
    </tr>
    <tr>
      <th>Time:</th>                 <td>12:24:22</td>     <th>  Log-Likelihood:    </th> <td> -3004.6</td>
    </tr>
    <tr>
      <th>No. Observations:</th>      <td>   366</td>      <th>  AIC:               </th> <td>   6023.</td>
    </tr>
    <tr>
      <th>Df Residuals:</th>          <td>   359</td>      <th>  BIC:               </th> <td>   6051.</td>
    </tr>
    <tr>
      <th>Df Model:</th>              <td>     6</td>      <th>                     </th>     <td> </td>   
    </tr>
    <tr>
      <th>Covariance Type:</th>      <td>nonrobust</td>    <th>                     </th>     <td> </td>   
    </tr>
    </table>
    <table class="simpletable">
    <tr>
               <td></td>              <th>coef</th>     <th>std err</th>      <th>t</th>      <th>P>|t|</th> <th>[95.0% Conf. Int.]</th> 
    </tr>
    <tr>
      <th>C(day_of_week)[Fri]</th> <td> 1.605e+04</td> <td>  124.514</td> <td>  128.866</td> <td> 0.000</td> <td> 1.58e+04  1.63e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Mon]</th> <td> 1.604e+04</td> <td>  123.334</td> <td>  130.061</td> <td> 0.000</td> <td> 1.58e+04  1.63e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Sat]</th> <td> 1.312e+04</td> <td>  124.514</td> <td>  105.345</td> <td> 0.000</td> <td> 1.29e+04  1.34e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Sun]</th> <td> 1.518e+04</td> <td>  123.334</td> <td>  123.110</td> <td> 0.000</td> <td> 1.49e+04  1.54e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Thu]</th> <td> 1.599e+04</td> <td>  124.514</td> <td>  128.415</td> <td> 0.000</td> <td> 1.57e+04  1.62e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Tue]</th> <td> 1.578e+04</td> <td>  124.514</td> <td>  126.740</td> <td> 0.000</td> <td> 1.55e+04   1.6e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Wed]</th> <td> 1.595e+04</td> <td>  124.514</td> <td>  128.122</td> <td> 0.000</td> <td> 1.57e+04  1.62e+04</td>
    </tr>
    </table>
    <table class="simpletable">
    <tr>
      <th>Omnibus:</th>       <td>138.226</td> <th>  Durbin-Watson:     </th> <td>   0.904</td> 
    </tr>
    <tr>
      <th>Prob(Omnibus):</th> <td> 0.000</td>  <th>  Jarque-Bera (JB):  </th> <td> 802.535</td> 
    </tr>
    <tr>
      <th>Skew:</th>          <td>-1.478</td>  <th>  Prob(JB):          </th> <td>5.39e-175</td>
    </tr>
    <tr>
      <th>Kurtosis:</th>      <td> 9.625</td>  <th>  Cond. No.          </th> <td>    1.01</td> 
    </tr>
    </table>



-  There are some interesting remarks I can make about the above
   summary, but let's just focus on the residual timeseries signal from
   this regression model.

Analyze residual signal
-----------------------

.. code:: python

    # add residual signal to our timeseries dataframe
    ts_flightcounts['residual'] = mod.resid
    
    
    title = 'Residual Signal in the Daily Airflight Counts ({})'.format(period)
    title+= '<br>(`day_of_week` used as regressors)'
    ts_flightcounts.iplot(y=['residual'],
                          filename=outfile+'plot_resid',
                          text=hover_text,
                          color='green',
                          title=title)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1799.embed?link=false&logo=false&share_key=BF0DMZva3xxQFcxM1MYjnb" height="525px" width="100%"></iframe>



.. code:: python

    title = 'Residual Signal in the Daily Airflight Counts ({})'.format(period)
    title+= '<br>(original signal overlaid in secondary y-axes)'
    
    fig1 = ts_flightcounts.iplot(columns=['counts'],   text=hover_text, color='pink',asFigure=True)
    fig2 = ts_flightcounts.iplot(columns=['residual'], text=hover_text, color='green',
                                 secondary_y=['residual'], asFigure=True,title=title)
    fig2['data'].extend(fig1['data'])
    py.iplot(fig2,filename=outfile+'residual-overlaid')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1805.embed?link=false&logo=false&share_key=miNWMfcO2toDdFhYS4UWJf" height="525px" width="100%"></iframe>



-  The cyclical effect from ``day_of_week`` has been fairly suppressed.

-  There are dominant *spikes* present around National holidays (eg,
   Thanksgiving, Independence day), which makes sesne --- many people,
   myself included, tend to fly out during these vacation time :)

Get "Lagged" residual
---------------------

-  Let's take this a step further, and compute and plot the "lagged"
   residual plot by computing the "first-order-difference" in the
   residual signal

-  this is given by: ``resid_lag[t] = resid[t] - resid[t-1]``

-  (coming from an electrical engineering background, I interpret this
   as a high-pass filtering operation)

.. code:: python

    # also add "lagged" residual information
    ts_flightcounts['resid_lag'] = \
        ts_flightcounts['residual'].shift(1) - ts_flightcounts['residual']
        
    title = 'Lagged Residual Signal of Airflight Counts in the US between {}'.format(period)
    title+= '<br>(left click to zoom on figure; shaded region = +/-1.5 std-dev)'
    
    annotations = {
        datetime(2015,11,26):'Thanksgiving',
        datetime(2015,12,24):'Christmas Eve',
        datetime(2015,12,31):'New Years',
        datetime(2016, 2, 7):'??? Something happen ???',
        datetime(2016, 5,29):'Memorials Day',
        datetime(2016, 7, 3):'Independence Day',
        datetime(2016, 9, 4):'Labor Day',
    }
    
    std_ = ts_flightcounts['resid_lag'].std() # std-deviation
    
    ts_flightcounts['resid_lag'].iplot(
        filename=outfile+'plot_resid_lag',
        annotations=annotations,
        color = 'orange',
        #hspan=[(-1.5*std_,1.5*std_)],
        hspan = dict(y0=-1.5*std_,y1=1.5*std_,opacity=0.2,color='teal',fill=True),
        text=hover_text,
        title=title)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1807.embed?link=false&logo=false&share_key=gZgt67hPMDug68ug3PsKwf" height="525px" width="100%"></iframe>



-  Pretty neat! The national holidays appear as huge "*spikes*" in the
   signal!

-  There are some other mild "spikes" occuring at days I am not familiar
   with (e.g., was February 7th last year a special day?)

.. code:: python

    title = 'Lagged Residual Signal in the Daily Airflight Counts ({})'.format(period)
    title+= '<br>(original signal overlaid in secondary y-axes; left click to select zooming region)'
    
    fig1 = ts_flightcounts.iplot(columns=['counts'],   text=hover_text, color='pink',asFigure=True)
    fig2 = ts_flightcounts.iplot(columns=['resid_lag'], text=hover_text, color='orange',
                                 secondary_y=['resid_lag'], asFigure=True,title=title)
    fig2['data'].extend(fig1['data'])
    py.iplot(fig2,filename=outfile+'resid-lag-overlaid')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1809.embed?link=false&logo=false&share_key=OZtWbp85ihAeQoPk7bnbGm" height="525px" width="100%"></iframe>



.. code:: python

    #| below create stacked subplot...not that interesting, so comment out
    # title = 'Flight counts'
    # ts_flightcounts.iplot(y=['counts','residual','resid_lag'],
    #                       subplots=True, shape=(3,1),
    #                       text=hover_text,
    #                       shared_xaxes=True, 
    #                       title=title,
    #                       filename=outfile+'flightcounts_subplot')

Histograms of the signals
-------------------------

-  The *spike* detection approach above seems like an "anomaly
   detection" or "outlier detection problem.

-  Since there are several (heuristic) outlier detection method that
   relies on normality assumptions, let's quickly study the distribution
   of the time series signal

.. code:: python

    from plotly.tools import FigureFactory as FF
    
    columns = ['counts','residual','resid_lag']
    colors  = ['red','green','orange']
    group_data = map(lambda col: ts_flightcounts[col].dropna().values,columns)
    fig = FF.create_distplot(group_data,
                             group_labels=columns,
                             bin_size= 300,
                             colors=colors,
                             curve_type='kde',#'kde' or 'normal'
    )
    
    title = 'Distributions among the three quantities of interest ({})'.format(period)
    title+= '<br>(KDE of the lagged residual looks sufficiently bell curvy?)'
    
    fig['layout'].update(title=title)
    py.iplot(fig, filename=outfile+'histogram2')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1811.embed?link=false&logo=false&share_key=Id7ybFN2fZfkCXnhxvsiYT" height="525px" width="100%"></iframe>



-  test of normality is quite a heavily debated topic, so I will refrain
   myself on discussing about it too much

-  (for exmple, with large sample size, your chance of rejecting the
   null based on pvalues gets very high, regardless of the
   distributional assumption you make on the test statistics)

-  but based on the above plot, the ``lagged_residual_plot`` looks
   sufficiently normal to my eyes (perhaps an `subexponential
   distribution <https://en.wikipedia.org/wiki/Heavy-tailed_distribution>`__,
   based on its heavy tail...can be an interesting reserch topic)

Repeat analysis for 3 years period
==================================

-  Just for kicks, I further downloaded data over 2 additional years
   (from Nov2013-Oct2015), to see if similar pattern appeared in
   previous years.

-  The code below is merely a carbon copy of the above.

.. code:: python

    df_data = util.load_airport_data_3years()
    period = '11/1/2013 to 10/31/2016' #range of our analysis


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

    # create a column containing "YEAR-MONTH-DAY"
    df_data['time'] = ( df_data['YEAR'].astype(str) + '-' 
                      + df_data['MONTH'].astype(str) + '-' 
                      + df_data['DAY_OF_MONTH'].astype(str))

.. code:: python

    # create time-series of airtraffic counts
    ts_flightcounts = pd.DataFrame(df_data['time'].value_counts()).rename(columns={'time':'counts'})
    ts_flightcounts.index = ts_flightcounts.index.to_datetime()
    ts_flightcounts.sort_index(inplace=True) # need to sort by date
    
    # explicitly add extra date-info as dataframe columns (to apply `groupby` later)
    ts_flightcounts['day']= ts_flightcounts.index.day
    ts_flightcounts['month']= ts_flightcounts.index.month
    ts_flightcounts['day_of_week'] = ts_flightcounts.index.dayofweek
    
    # `dayofweek` uses encoding Monday=0 ... Sunday=6...make this explicit
    ts_flightcounts['day_of_week'] = ts_flightcounts['day_of_week'].map({0:'Mon',
                                                                         1:'Tue',
                                                                         2:'Wed',
                                                                         3:'Thu',
                                                                         4:'Fri',
                                                                         5:'Sat',
                                                                         6:'Sun'}).astype(str)
    
    # create hover_text object for plotly
    hover_text= (
        ts_flightcounts['month'].astype(str) 
        + '/'  + ts_flightcounts['day'].astype(str)
        + ' (' + ts_flightcounts['day_of_week'] + ')'
    ).tolist()

.. code:: python

    plt_options = dict(text=hover_text,color='pink')
    title = 'Daily Airflight Counts in the US between ' + period
    title+= '<br>(hover over plot for dates; left-click to zoom)'
    
    ts_flightcounts.iplot(y='counts',
                          filename=outfile+'plot_flightcounts3yrs',
                          title=title,
                          **plt_options)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1813.embed?link=false&logo=false&share_key=ki26T9goZ2Vdx43NnU8qZb" height="525px" width="100%"></iframe>



.. code:: python

    mod = smf.ols(formula = 'counts ~ C(day_of_week) - 1',data=ts_flightcounts).fit()
    
    mod.summary()




.. raw:: html

    <table class="simpletable">
    <caption>OLS Regression Results</caption>
    <tr>
      <th>Dep. Variable:</th>         <td>counts</td>      <th>  R-squared:         </th> <td>   0.540</td> 
    </tr>
    <tr>
      <th>Model:</th>                   <td>OLS</td>       <th>  Adj. R-squared:    </th> <td>   0.537</td> 
    </tr>
    <tr>
      <th>Method:</th>             <td>Least Squares</td>  <th>  F-statistic:       </th> <td>   212.7</td> 
    </tr>
    <tr>
      <th>Date:</th>             <td>Wed, 11 Jan 2017</td> <th>  Prob (F-statistic):</th> <td>1.59e-179</td>
    </tr>
    <tr>
      <th>Time:</th>                 <td>12:27:02</td>     <th>  Log-Likelihood:    </th> <td> -9081.9</td> 
    </tr>
    <tr>
      <th>No. Observations:</th>      <td>  1096</td>      <th>  AIC:               </th> <td>1.818e+04</td>
    </tr>
    <tr>
      <th>Df Residuals:</th>          <td>  1089</td>      <th>  BIC:               </th> <td>1.821e+04</td>
    </tr>
    <tr>
      <th>Df Model:</th>              <td>     6</td>      <th>                     </th>     <td> </td>    
    </tr>
    <tr>
      <th>Covariance Type:</th>      <td>nonrobust</td>    <th>                     </th>     <td> </td>    
    </tr>
    </table>
    <table class="simpletable">
    <tr>
               <td></td>              <th>coef</th>     <th>std err</th>      <th>t</th>      <th>P>|t|</th> <th>[95.0% Conf. Int.]</th> 
    </tr>
    <tr>
      <th>C(day_of_week)[Fri]</th> <td> 1.652e+04</td> <td>   76.905</td> <td>  214.751</td> <td> 0.000</td> <td> 1.64e+04  1.67e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Mon]</th> <td> 1.653e+04</td> <td>   76.905</td> <td>  214.941</td> <td> 0.000</td> <td> 1.64e+04  1.67e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Sat]</th> <td> 1.341e+04</td> <td>   76.905</td> <td>  174.351</td> <td> 0.000</td> <td> 1.33e+04  1.36e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Sun]</th> <td>  1.56e+04</td> <td>   76.905</td> <td>  202.900</td> <td> 0.000</td> <td> 1.55e+04  1.58e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Thu]</th> <td> 1.646e+04</td> <td>   77.151</td> <td>  213.367</td> <td> 0.000</td> <td> 1.63e+04  1.66e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Tue]</th> <td> 1.612e+04</td> <td>   77.151</td> <td>  208.939</td> <td> 0.000</td> <td>  1.6e+04  1.63e+04</td>
    </tr>
    <tr>
      <th>C(day_of_week)[Wed]</th> <td> 1.627e+04</td> <td>   77.151</td> <td>  210.946</td> <td> 0.000</td> <td> 1.61e+04  1.64e+04</td>
    </tr>
    </table>
    <table class="simpletable">
    <tr>
      <th>Omnibus:</th>       <td>334.890</td> <th>  Durbin-Watson:     </th> <td>   0.796</td>
    </tr>
    <tr>
      <th>Prob(Omnibus):</th> <td> 0.000</td>  <th>  Jarque-Bera (JB):  </th> <td>1830.024</td>
    </tr>
    <tr>
      <th>Skew:</th>          <td>-1.299</td>  <th>  Prob(JB):          </th> <td>    0.00</td>
    </tr>
    <tr>
      <th>Kurtosis:</th>      <td> 8.772</td>  <th>  Cond. No.          </th> <td>    1.00</td>
    </tr>
    </table>



.. code:: python

    # add residual signal to our timeseries dataframe
    ts_flightcounts['residual'] = mod.resid
    
    title = 'Residual Signal in the Daily Airflight Counts ({})'.format(period)
    title+= '<br>(`day_of_week` used as regressors)'
    ts_flightcounts.iplot(y=['residual'],
                          filename=outfile+'plot_resid_3years',
                          text=hover_text,
                          color='green',
                          title=title)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1819.embed?link=false&logo=false&share_key=vlfcxJfo1KSoFHHsIQsNn0" height="525px" width="100%"></iframe>



.. code:: python

    title = 'Residual Signal in the Daily Airflight Counts ({})'.format(period)
    title+= '<br>(original signal overlaid in secondary y-axes)'
    
    fig1 = ts_flightcounts.iplot(columns=['counts'],   text=hover_text, color='pink',asFigure=True)
    fig2 = ts_flightcounts.iplot(columns=['residual'], text=hover_text, color='green',
                                 secondary_y=['residual'], asFigure=True,title=title)
    fig2['data'].extend(fig1['data'])
    py.iplot(fig2,filename=outfile+'residual-overlaid_3years')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1821.embed?link=false&logo=false&share_key=pCiPLG6CDNgpQf2zpWx6LO" height="525px" width="100%"></iframe>



.. code:: python

    # also add "lagged" residual information
    ts_flightcounts['resid_lag'] = \
        ts_flightcounts['residual'].shift(1) - ts_flightcounts['residual']
        
    title = 'Lagged Residual Plot of Airflight Counts in the US ({})(left click to zoom)'.format(period)
    title+= '<br>("day-of-week" used as regressors; shaded region = +/-1.5 std-dev)'
    
    std_ = ts_flightcounts['resid_lag'].std()
    
    ts_flightcounts['resid_lag'].iplot(
        filename=outfile+'plot_resid_lag_3years',
        hspan = dict(y0=-1.5*std_,y1=1.5*std_,opacity=0.2,color='teal',fill=True),
        text=hover_text,
        title=title)




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1817.embed?link=false&logo=false&share_key=lgPen2YeoNXEvEBbXRWvOj" height="525px" width="100%"></iframe>



.. code:: python

    title = 'Lagged Residual Signal in the Daily Airflight Counts ({})'.format(period)
    title+= '<br>(original signal overlaid in secondary y-axes; left click to select zooming region)'
    
    fig1 = ts_flightcounts.iplot(columns=['counts'],   text=hover_text, color='pink',asFigure=True)
    fig2 = ts_flightcounts.iplot(columns=['resid_lag'], text=hover_text, color='orange',
                                 secondary_y=['resid_lag'], asFigure=True,title=title)
    fig2['data'].extend(fig1['data'])
    py.iplot(fig2,filename=outfile+'resid-lag-overlaid_3years')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1825.embed?link=false&logo=false&share_key=u82qeAgOF2RqhNxIADGimh" height="525px" width="100%"></iframe>



.. code:: python

    columns = ['counts','residual','resid_lag']
    colors  = ['red','green','orange']
    group_data = map(lambda col: ts_flightcounts[col].dropna().values,columns)
    fig = FF.create_distplot(group_data,
                             group_labels=columns,
                             bin_size= 300,
                             colors=colors,
                             curve_type='kde',#'kde' or 'normal'
    )
    
    title = 'Distributions among the three quantities of interest ({})'.format(period)
    
    fig['layout'].update(title=title)
    py.iplot(fig, filename=outfile+'histogram3years')




.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1823.embed?link=false&logo=false&share_key=NC65bD2dR9ZTSbfCPCUtts" height="525px" width="100%"></iframe>



Try overlaying the annual plot
------------------------------

-  Turned out plotly's data structure requires the full "year-month-day"
   information to create a timeseries plot...

-  So I'll resort to a static figure creating using Seaborn

.. code:: python

    # --- add period info ---
    display(ts_flightcounts.head())
    ts_flightcounts['period'] = np.nan
    #ts_flightcounts.isnull().sum()
    ts_flightcounts.loc[datetime(2013,11,1):datetime(2014,10,31), 'period'] = 'period1'
    ts_flightcounts.loc[datetime(2014,11,1):datetime(2015,10,31), 'period'] = 'period2'
    ts_flightcounts.loc[datetime(2015,11,1):datetime(2016,10,31), 'period'] = 'period3'
    
    display(ts_flightcounts.head())
    assert ts_flightcounts['period'].isnull().sum() == 0



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
          <th>residual</th>
          <th>resid_lag</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2013-11-01</th>
          <td>18215</td>
          <td>1</td>
          <td>11</td>
          <td>Fri</td>
          <td>1699.554140</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2013-11-02</th>
          <td>13813</td>
          <td>2</td>
          <td>11</td>
          <td>Sat</td>
          <td>404.471338</td>
          <td>1295.082803</td>
        </tr>
        <tr>
          <th>2013-11-03</th>
          <td>17031</td>
          <td>3</td>
          <td>11</td>
          <td>Sun</td>
          <td>1426.910828</td>
          <td>-1022.439490</td>
        </tr>
        <tr>
          <th>2013-11-04</th>
          <td>18039</td>
          <td>4</td>
          <td>11</td>
          <td>Mon</td>
          <td>1508.917197</td>
          <td>-82.006369</td>
        </tr>
        <tr>
          <th>2013-11-05</th>
          <td>17259</td>
          <td>5</td>
          <td>11</td>
          <td>Tue</td>
          <td>1139.108974</td>
          <td>369.808223</td>
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
          <th>day</th>
          <th>month</th>
          <th>day_of_week</th>
          <th>residual</th>
          <th>resid_lag</th>
          <th>period</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2013-11-01</th>
          <td>18215</td>
          <td>1</td>
          <td>11</td>
          <td>Fri</td>
          <td>1699.554140</td>
          <td>NaN</td>
          <td>period1</td>
        </tr>
        <tr>
          <th>2013-11-02</th>
          <td>13813</td>
          <td>2</td>
          <td>11</td>
          <td>Sat</td>
          <td>404.471338</td>
          <td>1295.082803</td>
          <td>period1</td>
        </tr>
        <tr>
          <th>2013-11-03</th>
          <td>17031</td>
          <td>3</td>
          <td>11</td>
          <td>Sun</td>
          <td>1426.910828</td>
          <td>-1022.439490</td>
          <td>period1</td>
        </tr>
        <tr>
          <th>2013-11-04</th>
          <td>18039</td>
          <td>4</td>
          <td>11</td>
          <td>Mon</td>
          <td>1508.917197</td>
          <td>-82.006369</td>
          <td>period1</td>
        </tr>
        <tr>
          <th>2013-11-05</th>
          <td>17259</td>
          <td>5</td>
          <td>11</td>
          <td>Tue</td>
          <td>1139.108974</td>
          <td>369.808223</td>
          <td>period1</td>
        </tr>
      </tbody>
    </table>
    </div>


.. code:: python

    #http://stackoverflow.com/questions/37596714/compare-multiple-year-data-on-a-single-plot-python
    #http://man7.org/linux/man-pages/man3/strftime.3.html
    ts_flightcounts['month'] = ts_flightcounts.index.to_series().dt.strftime('%b')
    util.sns_figure(figsize=(16,5))
    ts_flightcounts.query('period == "period1"').plot(x='month',y='counts',label='(2013/11 to 2014/10)',ax=plt.gca(),color='red')
    ts_flightcounts.query('period == "period2"').plot(x='month',y='counts',label='(2014/11 to 2015/10)',ax=plt.gca(),color='green')
    ts_flightcounts.query('period == "period3"').plot(x='month',y='counts',label='(2015/11 to 2016/10)',ax=plt.gca(),color='orange')
    plt.title('Daily Airflight Counts in the US over 3 different annual periods')




.. parsed-literal::
    :class: myliteral

    <matplotlib.text.Text at 0xc1824828>




.. figure:: /_static/img/regressing_out_weekday_effect_42_1.png


.. code:: python

    util.sns_figure(figsize=(16,5))
    ts_flightcounts.query('period == "period1"').plot(x='month',y='resid_lag',label='(2013/11 to 2014/10)',ax=plt.gca(),color='red')
    ts_flightcounts.query('period == "period2"').plot(x='month',y='resid_lag',label='(2014/11 to 2015/10)',ax=plt.gca(),color='green')
    ts_flightcounts.query('period == "period3"').plot(x='month',y='resid_lag',label='(2015/11 to 2016/10)',ax=plt.gca(),color='orange')
    plt.title('Lagged residual plots in the Airflight Counts in the US over 3 different annual periods')




.. parsed-literal::
    :class: myliteral

    <matplotlib.text.Text at 0xf37d45c0>




.. figure:: /_static/img/regressing_out_weekday_effect_43_1.png

