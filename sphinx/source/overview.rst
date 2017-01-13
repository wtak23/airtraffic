Project Overview
""""""""""""""""
To narrow the scope of my analysis, I decided to focus on the air-traffic data from Nov-1-2015 to Oct-31-2016. This is the latest available data provided by the Bureau of Transportation Statistic, and completes a full year cycle.

The project is broken down into three-parts, each having its own separate `Jupyter notebook <http://jupyter.org/>`__ page that allows me to present the result along with the analysis code.

.. rubric:: A quick remark

About 65-75% of the content in my Jupyter notebooks are occupied with codes (most of the effort towards "`tidying <https://en.wikipedia.org/wiki/Tidy_data>`__" the data-table). I put my best effort in making the visualization charts self-explanatory as possible, so if you are only interested in the "punchline" of the analysis, please scroll thorough the code and pause whenever you see a figure/chart (or visit the gallery pages linked below).

#########
Galleries
#########

.. toctree::
    :maxdepth: 2

    flight-count-analysis-gallery
    regression-gallery
    network-analysis-gallery.rst



.. rubric:: Part 1. Air-traffic trend analysis (`main notebook <http://takwatanabe.me/airtraffic/flight-count-analysis.html>`__)

- Here I analyzed the general trend in the daily flight-counts in the US airline as a time-series signal. 
- The goal was to identify any interesting trend in the flight-counts at different time period (eg, day-of-week, month, national holidayss) and location (eg, densely populated area, location of **hub** airports).
- Example types of questions asked: 

  - Is there any day/time of the year when the US flight-counts takes a dip/spike? 

    (**answer**: ``Saturday`` takes a huge dip)
  - does Honolulu airport attract more visitors during the winter-time when its cold at most other part of the country? 

    (**answer**: turned out to be the opposite - summer turned out to be the busiest in terms  of air-traffic movements)
  - Is there any trend in fight-counts that is specific to airports at major cities like NY/LA? 

    (**answer**: nothing I can detect)
  - which airport in the US is the busiest i terms of flight-counts? 

    (**answer**: Atlanta turned out to be the biggest **hub** spot. Nevada also stood out after normalizing over state population)

- Example chart from analysis:

.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1853.embed?link=false&logo=false&share_key=xcDy8dp7T93r2qLV5WLTCI" height="400px" width="75%"></iframe>

.. ==========================================================================..

.. rubric:: Part2: Regressing away the effect of ``day_of_the_week`` in the Air-traffic Time Series Signal (`main notebook <http://takwatanabe.me/airtraffic/regressing_out_weekday_effect.html>`__)

- Part 1 of our analysis revealed that the US air-traffic is heavily influenced by what day of the week it is, especially on Saturdays
- I had a suspicions that this potentially contaminates other interesting patterns inside the signal
- In this notebook, we'll aim to **linearly regress out** the effect of ``day_of_week`` by using a linear regression model, with the ``day_of_week`` used as the regressor

- Example chart from analysis:

.. raw:: html

   <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1807.embed?link=false&logo=false&share_key=gZgt67hPMDug68ug3PsKwf" height="525px" width="75%"></iframe>

.. =========================================================================..
.. rubric:: Part 3. Air-traffic count analysis [**absolutely my favorite part**] (`main notebook <http://takwatanabe.me/airtraffic/flight-count-analysis.html>`__)

- Example chart from analysis: figure in SVG format, so feel free to open in new tab and zoom in closely :)

.. figure:: /_static/img/traffic_mainland_intra_only.svg
    :width: 77%

    The network structre of aircraft movements among different **communities** of airports (detected via Louvain Modularity algorithm. Only the "intra-community" edges are displayed. Click on figure to open in new tab -- SVG format so you can zoom in closely :)




.. Since this is a data science project, much of my effort was spent towards interacting with the data through **coding**, with the goal of identifying some "interesting" trend in the data, which inevitably involves some painstaking trial-and-error process.

