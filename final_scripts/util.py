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
    
    #%%

    #%%
#%% === data loader ====
def load_airport_data():
    """ Load one year worth of airport traffic data (2015-11 to 2016-10) """
    df = None
    
    # create list of files.
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        print ' ... load dataframe from {} '.format(filename)
        if df is None:
            df = pd.read_csv('../data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('../data/'+filename).ix[:,:-1])

    return df
    
def load_airport_data_3years():
    """ Load 3 years worth of airport traffic data (2013-11 to 2016-10) """
    df = None
    
    # create list of files.
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2013-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2014-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        #print ' ... load dataframe from {} '.format(filename)
        if df is None:
            df = pd.read_csv('../data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('../data/'+filename).ix[:,:-1])

    return df
#%%
if __name__ == '__main__':
    df_data = load_airport_data()