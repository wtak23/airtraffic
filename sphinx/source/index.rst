US Airport Traffic Analysis
===========================

Hello, and welcome to my project! My name is Takanori Watanabe, and I am  a postdoctoral researcher at the University of Pennsylvania. My research focuses on developing new machine learning algorithms targeted for neuroimaging application.

This project analyzes the airline travel within the United States during the following one year time period: November 1, 2015 to October 31, 2016. The dataset is provided by the Bureau of Transportation Statistics and is available for download `here <www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time>`__.

The goal of the project is two-folds:

(1) get additional hands on training with real-world data analysis (e.g., web scraping, `data tidying <https://en.wikipedia.org/wiki/Tidy_data>`__, and creating informative visualization charts), and 

(2) to have fun --- I learned a lot about the air-traffic trend in the United States, and gained insights about the network topology present in the airline system.

Analysis was conducted mainly through Python, and the results are presented along with the code using Jupyter-notebook .The source code to reproduce the main figures are available in my `Github repository <https://github.com/wtak23/airtraffic/tree/master/final_scripts>`__.

.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1955.embed?link=false&logo=false&share_key=b2DdhlljEH0JZMTRVPlUjf" height="525px" width="100%"></iframe>


.. toctree::
   :maxdepth: 2
   :caption: Contents

   overview
   flight-count-analysis
   regressing_out_weekday_effect
   network_analysis
   data_munging


.. raw:: html

    <iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~takanori/1953.embed?link=false&logo=false&share_key=gGIBKQOHB5hkU1UgIIoq2z" height="850px" width="1000px"></iframe>


..   Network representing community structure in the US airport traffic during the past year (Nov 2015 - Oct 2016), with the node-color representing the community each airport belongs to.  Click on figure to open in a separate tab and zoom; figures are in SVG format, so zoom in as you wish :)

.. Here, node-size is proportional to the number of flights made to/at the airport, whereas the edge-width is proportional to the number of flights made between two airports.
.. All modules for which code is available (`link <./_modules/index.html>`_)