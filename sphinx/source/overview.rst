Project Overview
""""""""""""""""
To narrow our focus, I decided to limit the scope of the analysis from Nov-1-2015 to Oct-31-2016 (this is the latest available data provided by BTS).

The project is broken down into three-parts, each having its own separate `Jupyter notebook <http://jupyter.org/>`__ page (which allows me to present the result alongside wit the code):

1. Air-traffic trend analysis (`notebook <http://takwatanabe.me/airtraffic/flight-count-analysis.html>`__)

  - Here I begin my acclimating myself  with the dataset through basic exploratory data analysis.
  - 
  - I've gained insights on the type of preprocessing I need to apply in order to convert the data-table in a *"nice"* format that has convenient structure that are amenable for grouping and plotting (i.e., "tidying" the data).
2. Air-traffic count analysis (`notebook <http://takwatanabe.me/airtraffic/flight-count-analysis.html>`__)
3. Air-traffic count analysis (`notebook <http://takwatanabe.me/airtraffic/flight-count-analysis.html>`__)

.. rubric:: A quick remark

Since this is a data science project, much of my effort was spent towards interacting with the data through **coding**, with the goal of identifying some "interesting" trend in the data, which inevitably involves some painstaking trial-and-error process.


##############################
Analyasis 1: Air-traffic Trend
##############################

http://takwatanabe.me/airtraffic/flight-count-analysis.html

.. toctree::
    :maxdepth: 2
    :caption: Gallery
    :name: hi

    flight-count-analysis-gallery

.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1853.embed?link=false&logo=false&share_key=xcDy8dp7T93r2qLV5WLTCI" height="525px" width="100%"></iframe>


#############################
Air-traffic Residual Analysis
#############################

http://takwatanabe.me/airtraffic/regressing_out_weekday_effect.html

.. toctree::
    :maxdepth: 2
    :caption: Gallery
    :name: hii

    regression-gallery


.. raw:: html

   <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1807.embed?link=false&logo=false&share_key=gZgt67hPMDug68ug3PsKwf" height="525px" width="100%"></iframe>


#############################################
Network Theoretic Analysis of US Airline Data
#############################################

http://takwatanabe.me/airtraffic/network_analysis.html

.. toctree::
    :maxdepth: 2
    :caption: Gallery
    :name: hiii

    network-analysis-gallery


.. figure:: /_static/img/traffic_mainland_intra_only.svg
    :align: center
    :width: 100%

    caption



