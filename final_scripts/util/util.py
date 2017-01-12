import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn.apionly as sns
import os
import time
import sys
import networkx as nx

from datetime import datetime
from pprint import pprint
#%% === set plotting options ====
def sns_figure(style='darkgrid',**kwargs):
    """ Create new figure in seaborn with temporary style change
    
    A simple convenience function used to temporarily change figure style
    using seaborn (``'darkgrid'`` is my favorite style)
    
    Usage:
    
    >>> sns_figure("darkgrid")
    >>> plt.plot(np.random.randn(100,3))
    
    See http://seaborn.pydata.org/tutorial/aesthetics.html#temporarily-setting-figure-style
    
    Parameters
    ----------
    style : string
        One of the five preset styles in seaborn: 'darkgrid', 'whitegrid', 
        'dark', 'white', and 'ticks'
    **kwargs : dict
        Keyword arguments passed to ``pyplot.figure``
    """
    with sns.axes_style(style):
        plt.figure(**kwargs)
        plt.plot()

def sns_subplots(nrows,ncols,style='darkgrid',ravel=True,**kwargs):
    """ Create subplots in seaborn with temporary style change
    
    Used to temporaritly change figure style in seaborn
    
    ``**kwargs`` take arguments to :func:`plt.subplots`
    
    Usage:
    
    >>> fig,axes = sns_subplots(nrows=2,ncols=3,style='darkgrid',figsize=(16,8))
    >>> for ax in axes:
    >>>     ax.plot(np.random.randn(100))
    
    Parameters
    ----------
    nrows : int
        Number of rows to include in the subplot
    ncols : int
        Number of columns to include in the subplot
    style : string
        One of the five preset styles in seaborn: 'darkgrid', 'whitegrid', 
        'dark', 'white', and 'ticks'
    **kwargs : dict
        Keyword arguments passed to ``pyplot.subplots``
        
    Returns
    -------
    fig : plt.figure object
        ``plt.figure object``
    axes : plt.axes list-array
        ``plt.axes list-array``
    """
    from seaborn import axes_style
    with axes_style(style):
        fig,axes = plt.subplots(nrows,ncols,**kwargs)
    
    if ravel:
        # this way, i don't have to use 2-d indexing when individual axes
        axes = axes.ravel()
    return fig,axes
    
def sns_set_colorpalette():
    """ Set seaborn plotting  to my preferred style """
    tmp = sns.color_palette("muted")
    
    # swap red and green
    tmp[1],tmp[2] = tmp[2],tmp[1]
    
    sns.set_palette(tmp)
    
#%% === data loader ====
def load_airport_data(verbose=True):
    """ Load one year worth of airport traffic data (2015-11 to 2016-10) """
    df = None
    
    # create list of files.
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    # columns to read from zipped spreadsheet
    usecols = ['YEAR','QUARTER','MONTH','DAY_OF_MONTH','DAY_OF_WEEK',
               'ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID']
               
    df = None
    for filename in full_files:
        if verbose: print ' ... load dataframe from {} '.format(filename)
        if df is None:
            df = pd.read_csv('../data/'+filename,usecols=usecols)
        else:
            df = df.append(pd.read_csv('../data/'+filename,usecols=usecols))

    return df
    
def load_airport_data_3years(verbose=True):
    """ Load 3 years worth of airport traffic data (2013-11 to 2016-10) """
    # create list of files.
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2013-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2014-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    # columns to read from zipped spreadsheet
    usecols = ['YEAR','QUARTER','MONTH','DAY_OF_MONTH','DAY_OF_WEEK',
               'ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID']
               
    df = None
    for filename in full_files:
        if verbose: print ' ... load dataframe from {} '.format(filename)
        if df is None:
            df = pd.read_csv('../data/'+filename,usecols=usecols)
        else:
            df = df.append(pd.read_csv('../data/'+filename,usecols=usecols))

    return df
    
def make_hash_tables(df_lookup):
    hash_tables = {}
    for col in df_lookup.columns:
        if col == 'Code':
            continue
        elif col in ['lat','lon']:
            """
            Warning: Pandas returns data type in numpy.float64 for floats,
            which is not supported in networkx.write_gexf. So typecast to float
            http://stackoverflow.com/questions/22037360/keyerror-when-writing-numpy-values-to-gexf-with-networkx
            """
            tmp_dict = df_lookup.set_index('Code')[col].to_dict()
            hash_tables[col] = {key:float(val) for key,val in tmp_dict.iteritems()}
        else:
            hash_tables[col] = df_lookup.set_index('Code')[col].to_dict()

    return hash_tables
#%% === other utility functions ===
def print_time(t):
    """ Return string indicating times elapsed wrt a time.time() instance

    Usage: 
    
    >>> import time
    >>> t = time.time()
    >>> time.sleep(2.5)
    >>> print_time(t)
    'Elapsed time:  2.50 seconds'
    
    Parameters
    ----------
    t : time object
        Instance of the time.time() object
        
    Returns
    -------
    time_str : string
        String with elapsed time
    """
    return "Elapsed time: {:>5.2f} seconds".format(time.time()-t)
#%%
def hash_state_to_abbrev():
    """ Return a hash-table mapping state name to its abbreviation.
    
    Credit: https://gist.github.com/rogerallen/1583593
    """
    return {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }
#%%
if __name__ == '__main__':
    df_data = load_airport_data()