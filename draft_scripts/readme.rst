#################################
Preliminary data analysis scripts
#################################
Folder contains my crude data analysis scripts i used with ipython.

Codes written for interactive data analysis (so python files not intended to be ran as scripts). Nevertheless, the codes may give a rough idea on my thought process and my data-analysis style.

-------------

##################
us population data
##################
nst-est2016-01.xlsx
- http://www.census.gov/data/tables/2016/demo/popest/nation-total.html


Get U.S. population date (2012 so kinda outdated...ideally would use api provided from the us census but skipped this in the interest of time....)

.. code-block:: bash

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ wget http://download.maxmind.com/download/worldcities/worldcitiespop.txt.gz
    --2017-01-09 16:56:18--  http://download.maxmind.com/download/worldcities/worldcitiespop.txt.gz
    Resolving download.maxmind.com (download.maxmind.com)... 104.16.37.47, 104.16.38.47, 2400:cb00:2048:1::6810:262f, ...
    Connecting to download.maxmind.com (download.maxmind.com)|104.16.37.47|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 41896101 (40M) [application/octet-stream]
    Saving to: ‘worldcitiespop.txt.gz’

    worldcitiespop.txt. 100%[===================>]  39.96M  3.01MB/s    in 13s

    2017-01-09 16:56:31 (3.05 MB/s) - ‘worldcitiespop.txt.gz’ saved [41896101/41896101]


    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ tar -xvzf worldcitiespop.txt.gz
    tar: This does not look like a tar archive
    tar: Skipping to next header
    tar: Exiting with failure status due to previous errors

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ file worldcitiespop.txt.gz
    worldcitiespop.txt.gz: gzip compressed data, was "worldcitiespop.txt", last modified: Thu May  3 03:08:07 2012, from Unix

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ gunzip worldcitiespop.txt.gz

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ ls worldcitiespop.txt
    worldcitiespop.txt

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ head worldcitiespop.txt
    Country,City,AccentCity,Region,Population,Latitude,Longitude
    ad,aixas,Aix▒s,06,,42.4833333,1.4666667
    ad,aixirivali,Aixirivali,06,,42.4666667,1.5
    ad,aixirivall,Aixirivall,06,,42.4666667,1.5
    ad,aixirvall,Aixirvall,06,,42.4666667,1.5
    ad,aixovall,Aixovall,06,,42.4666667,1.4833333
    ad,andorra,Andorra,07,,42.5,1.5166667
    ad,andorra la vella,Andorra la Vella,07,20430,42.5,1.5166667
    ad,andorra-vieille,Andorra-Vieille,07,,42.5,1.5166667
    ad,andorre,Andorre,07,,42.5,1.5166667

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ sed -n '1 p; /^us,/ p' worldcitiespop.txt > uscitiespop.txt

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ head uscitiespop.txt
    Country,City,AccentCity,Region,Population,Latitude,Longitude
    us,abanda,Abanda,AL,,33.1008333,-85.5297222
    us,abbeville,Abbeville,AL,,31.5716667,-85.2505556
    us,abbot springs,Abbot Springs,AL,,33.3608333,-86.4816667
    us,abel,Abel,AL,,33.5486111,-85.7125000
    us,abercrombie,Abercrombie,AL,,32.8486111,-87.1650000
    us,aberfoil,Aberfoil,AL,,32.0702778,-85.6877778
    us,abernant,Abernant,AL,,33.2902778,-87.1980556
    us,abernathy,Abernathy,AL,,33.6505556,-85.4075000
    us,academy park,Academy Park,AL,,33.2000000,-87.1566667

    takanori@DESKTOP-FJQ41I1 ~/Desktop
    $ mv uscitiespop.txt "/cygdrive/c/Users/takanori/Dropbox/git/spotify/draft_scripts/"