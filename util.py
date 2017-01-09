import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import os
import seaborn.apionly as sns
import sys
import time
import networkx as nx
#%% === starting members ====
def load_data_1year():
    """ Load data from 2015-11 to 2016-10 """
    df = None
    
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        print filename
        if df is None:
            df = pd.read_csv('./data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('./data/'+filename).ix[:,:-1])

    return df

def load_data_1year2014_2015():
    """ Load data from 2015-11 to 2016-10 """
    df = None
    
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2014-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        print filename
        if df is None:
            df = pd.read_csv('./data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('./data/'+filename).ix[:,:-1])

    return df

def load_data_2year():
    """ Load data from 2014-11 to 2016-10 """
    df = None
    
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2014-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        print filename
        if df is None:
            df = pd.read_csv('./data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('./data/'+filename).ix[:,:-1])

    assert np.all(np.sort(df['MONTH'].unique()) == np.arange(1,13))
    return df

def load_data_3year():
    """ Load data from 2013-11 to 2016-10 """
    df = None
    
    # rjust prepends '0' if month has single-digit
    # ( so '1' gets mapped to '01', whereas '11' remains as is)
    full_files = map(lambda x: '2013-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2014-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        print filename
        if df is None:
            df = pd.read_csv('./data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('./data/'+filename).ix[:,:-1])

    assert np.all(np.sort(df['MONTH'].unique()) == np.arange(1,13))
    return df
    
def load_airport_idcode(df):
    df_air_id = pd.read_csv('./data/L_AIRPORT_ID.csv')
    #df_air_id.head()
    
    # only keep the items in the main dataframe
    _mask = df_air_id['Code'].isin( df['ORIGIN_AIRPORT_ID'])
    df_air_id = df_air_id[ _mask ].reset_index(drop=True)
    
    # The 'Description' column uses a comma and colon to delimit the City,State,Airilne info...
    # Create a field for each of these information
    _df = pd.DataFrame(map(lambda x: {'City':x[0], 'State':x[2], 'Airport':x[4]}, 
                           df_air_id['Description'].str.split(r'(,\s|:\s)')))
    #_df.head()
    df_air_id = df_air_id.join(_df)
    return df_air_id

def get_roundtrips(trip_counts):
    """ Get round-trip counts (undirected graph)
    
    >>> trip_counts = df['Trips'].value_counts()
    """
    # drop *counts* not involved in two-way-trips
    _mask1 = pd.Index(trip_counts.index.map(lambda x: (min(x),max(x)))).duplicated(keep='first')
    _mask2 = pd.Index(trip_counts.index.map(lambda x: (min(x),max(x)))).duplicated(keep='last')
    _mask = _mask1 | _mask2
    
    # keep only round trips
    trip_counts = trip_counts[_mask]
    
    # === take the smallest counts of the "round-trip" ===
    # get one of the direction in the round-trip to use as Index (say, an outbound flight)
    _mask = pd.Index(trip_counts.index.map(lambda x: (min(x),max(x)))).duplicated(keep='first')
    
    # create Series containing round-trip counts...which is an undirected graph
    trip_counts_und = pd.Series(0,index = trip_counts.index[_mask],name='Counts')
    
    # take the smaller of the trips to eliminate "one-way-flights"
    swap = lambda x: (x[1],x[0])
    for i in trip_counts_und.index:
        trip_counts_und[i] = min(trip_counts[i], trip_counts[swap(i)])
    
    return trip_counts_und
    
def print_time(t):
    """ Return string indicating times elapsed wrt a time.time() instance

    Parameters
    ----------
    t : time object
        Instance of the time.time() object

    >>> import time
    >>> t = time.time()
    >>> # some code doing work
    >>> print_time(t)
    """
    return "Elapsed time: {:>5.2f} seconds".format(time.time()-t)
    
#%%
def make_networkx_graph(trip_counts,df_id,apply_hash=True):
    """ Create networkx graph
    
    Example usage
    
    >>> trip_counts = df.query['Trips'].value_counts()
    >>> G = make_networkx_graph(trip_counts,df_id,hash_table)
    """
    trip_counts = trip_counts.copy()
    #trip_counts = get_roundtrips( trip_counts )
    
    # nodes must be unique... use City_State info
    node_label = 'City_State'
    hash_table = df_id.set_index('Code')[node_label].to_dict()
    nodes = df_id[node_label].tolist()
    
    # replace code with city-state-name for interpretation (uniqueness required!)
    if apply_hash:
        trip_counts.index = trip_counts.index.map(lambda x: (hash_table[x[0]], hash_table[x[1]]))
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    
    lat_dict = {key:float(val) for key,val in df_id.set_index(node_label)['lat'].to_dict().iteritems()}
    lon_dict = {key:float(val) for key,val in df_id.set_index(node_label)['lon'].to_dict().iteritems()}
    
    nx.set_node_attributes(G, 'lat', lat_dict)
    nx.set_node_attributes(G, 'lon', lon_dict)

    # add edges
    edges = map(lambda x:(x[0][0],x[0][1],{'weight':x[1]}), zip(trip_counts.index,trip_counts.values))
    G.add_edges_from(edges)
    
    return G
#%%
def df_to_flightcount_ts(df):
    ts_flightcounts = pd.DataFrame(df['time'].value_counts()).rename(columns={'time':'counts'})
    ts_flightcounts.index = ts_flightcounts.index.to_datetime()
    ts_flightcounts.sort_index(inplace=True) # need to sort by date
    
    # explicitly add extra date-info as dataframe columns (to apply `groupby` later)
    ts_flightcounts['day'] = ts_flightcounts.index.day
    ts_flightcounts['year'] = ts_flightcounts.index.year
    ts_flightcounts['month'] = ts_flightcounts.index.month
    ts_flightcounts['day_of_week'] = ts_flightcounts.index.dayofweek
    
    from math import ceil
    ts_flightcounts['quarter'] = ts_flightcounts['month'].map(lambda x: int(ceil(x/3.)))
    
    # `dayofweek` uses encoding Monday=0 ... Sunday=6...make this explicit
    #print ts_flightcounts['day_of_week'][:5]
    ts_flightcounts['day_of_week'] = ts_flightcounts['day_of_week'].map({0:'MON',
                                                                         1:'TUE',
                                                                         2:'WED',
                                                                         3:'THU',
                                                                         4:'FRI',
                                                                         5:'SAT',
                                                                         6:'SUN'})
    return ts_flightcounts
    
def state_abbrev_dict():
    """ Credit: https://gist.github.com/rogerallen/1583593 """
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
#%% === temporary convenience functions
def load_airport_idcode_shortcut():
    """ Based on spotify01_08a_study_edges_cleaned.py"""
    df_id = pd.read_csv('df_lookup_from_0107a.csv')

    df_id['City_State'] = df_id['City'] + ' (' + df_id['State'] + ')'

    cleaner = [
        ('Houston (TX) [Ell]', 'Ellington'), 
        ('Houston (TX) [WP.Hobby]', 'William P Hobby'), 
        ('Houston (TX) [G.Bush]',  'George Bush Intercontinental/Houston'), 
        ('Washington (DC) [R.Reagan]',   'Ronald Reagan Washington National'),
        ('Washington (DC) [W.Dulles]',   'Washington Dulles International'),
        ('Chicago (IL) [Midway]',   'Chicago Midway International'),
        ("Chicago (IL) [O'Hare]",   "Chicago O'Hare International"),
        ("New York (NY) [JFK]",   "John F. Kennedy International"),
        ("New York (NY) [Lag]",   "LaGuardia"),
    ]
    
    for _replace, _airport in cleaner:
        df_id.loc[df_id['Airport'] == _airport, 'City_State'] = _replace
    
    return df_id

#%% ========================== 
def sns_set_colorpalette():
    """ My preferred seaborn plotting style """
    tmp = sns.color_palette("muted")
    # swap red and green
    tmp[1],tmp[2] = tmp[2],tmp[1]
    #sns.palplot(tmp)
    #% once happy, set!
    sns.set_palette(tmp)
    
def load_all_data():
    """ Load data from 2015-01 to 2016-10 """
    df = None
    
    # (rjust prepends '0' if month has single-digit)
    full_files = map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        print filename
        if df is None:
            df = pd.read_csv('./data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('./data/'+filename).ix[:,:-1])

    assert np.all(np.sort(df['MONTH'].unique()) == np.arange(1,13))
    return df
    
    
def load_all_data_2years():
    """ Load data from 2015-01 to 2016-10 """
    df = None
    
    # (rjust prepends '0' if month has single-digit)
    full_files = map(lambda x: '2014-'+str(x).rjust(2,'0')+'.zip', [11,12]) + \
                 map(lambda x: '2015-'+str(x).rjust(2,'0')+'.zip', range(1,13)) + \
                 map(lambda x: '2016-'+str(x).rjust(2,'0')+'.zip', range(1,11))
    
    for filename in full_files:
        print filename
        if df is None:
            df = pd.read_csv('./data/'+filename).ix[:,:-1]
        else:
            df = df.append(pd.read_csv('./data/'+filename).ix[:,:-1])

    assert np.all(np.sort(df['MONTH'].unique()) == np.arange(1,13))
    return df
    
def load_by_year_date(year_date = '2015-01'):
    df = pd.read_csv('./data/{}.zip'.format(year_date)).iloc[:,:-1]
    
    #--- are the unique ORIGIN and DEST items all the same? ---
    # YES!
    test1 = np.array_equal(np.sort(df['ORIGIN_AIRPORT_ID'].unique()), 
                           np.sort(df['DEST_AIRPORT_ID'].unique()))
                           
    test2 = np.array_equal(np.sort(df['ORIGIN_AIRPORT_SEQ_ID'].unique()), 
                           np.sort(df['DEST_AIRPORT_SEQ_ID'].unique()))
                           
    test3 = np.array_equal(np.sort(df['ORIGIN_CITY_MARKET_ID'].unique()), 
                           np.sort(df['DEST_CITY_MARKET_ID'].unique()))
    assert test1 and test2 and test3
    
    return df
    
    
def load_main_data():
    df_main = pd.read_csv('./data/690907700_T_ONTIME.csv').iloc[:,:6]
    
    #--- are the unique ORIGIN and DEST items all the same? ---
    # YES!
    test1 = np.array_equal(np.sort(df_main['ORIGIN_AIRPORT_ID'].unique()), 
                           np.sort(df_main['DEST_AIRPORT_ID'].unique()))
                           
    test2 = np.array_equal(np.sort(df_main['ORIGIN_AIRPORT_SEQ_ID'].unique()), 
                           np.sort(df_main['DEST_AIRPORT_SEQ_ID'].unique()))
                           
    test3 = np.array_equal(np.sort(df_main['ORIGIN_CITY_MARKET_ID'].unique()), 
                           np.sort(df_main['DEST_CITY_MARKET_ID'].unique()))
    assert test1 and test2 and test3
    
    return df_main

def load_aux_data(df_main=None):
    if df_main is None:
        df_main = pd.read_csv('./data/690907700_T_ONTIME.csv').iloc[:,:6]
        
    df_air_id = pd.read_csv('./data/L_AIRPORT_ID.csv')
    df_seq_id = pd.read_csv('./data/L_AIRPORT_SEQ_ID.csv')
    df_market = pd.read_csv('./data/L_CITY_MARKET_ID.csv')

    # only keep the items in the main dataframe
    df_air_id = df_air_id[ df_air_id['Code'].isin( df_main['ORIGIN_AIRPORT_ID']) ].reset_index(drop=True)
    df_seq_id = df_seq_id[ df_seq_id['Code'].isin( df_main['ORIGIN_AIRPORT_SEQ_ID']) ].reset_index(drop=True)
    df_market = df_market[ df_market['Code'].isin( df_main['ORIGIN_CITY_MARKET_ID']) ].reset_index(drop=True)
    
    # The 'Description' column uses a comma and colon to delimit the City,State,Airilne info...
    # append info as three new columns 
    #df_air_id[['City','State','Airline']] = pd.DataFrame(df_air_id['Description'].str.split('[,:]').tolist())
    #df_seq_id[['City','State','Airline']] = pd.DataFrame(df_seq_id['Description'].str.split('[,:]').tolist())
    df_air_id[['City','State','Airline']] = pd.DataFrame(df_air_id['Description'].str.split(r'(,\s|:\s)').tolist()).iloc[:,[0,2,4]]
    df_seq_id[['City','State','Airline']] = pd.DataFrame(df_seq_id['Description'].str.split(r'(,\s|:\s)').tolist()).iloc[:,[0,2,4]]
    
    # for Market there's only City and State information (separated by column)
    df_market[['City','State']] = pd.DataFrame(df_market['Description'].str.split(',\s').tolist())
    
    # some entry has superfluous info on top of the state abbrev...drop them
    #print df_market['State'].str.len().value_counts()
    df_market['State'] = df_market['State'].str[:3]
    
    # drop the "Description" column for brevity
    #del df_air_id['Description']
    #del df_seq_id['Description']
    #del df_market['Description']
    
    # check there's no overlap in the code
    _check = 0
    _check += df_air_id['Code'].isin(df_seq_id['Code']).sum()
    _check += df_air_id['Code'].isin(df_market['Code']).sum()
    _check += df_seq_id['Code'].isin(df_market['Code']).sum()
    assert _check == 0
    
    return df_air_id, df_seq_id, df_market

def load_carriers():
    df_carr = pd.read_excel('./data/carriers.xls')
    
    # --- data cleansing ---
    # remove record containing any nans
    df_carr = df_carr.ix[~df_carr.isnull().any(axis=1)].reset_index(drop=True)
    
    # convert columns to unicode (realized some elements are treated as 'int'
    df_carr['Code'] = df_carr['Code'].apply(unicode)
    df_carr['Description'] = df_carr['Description'].apply(unicode)
    
    return df_carr

def load_airports():
    df_airports = pd.read_excel('./data/airports new.xlt')
    
    # convert columns to unicode (realized some elements are treated as 'int'
    df_airports['iata'] = df_airports['iata'].apply(unicode)
    
    return df_airports
    
def get_lookup_tables(df_main=None):
    # create lookup tables (hash-table) using 'Code' as the key
    # (note: none of the "Code" overlaps among the 3 dataframes (assertion made
    #        in function ``load_aux_data``)
    print ' WARNING! BUG IN CODE!!! '.center(50,'=')
    df1,df2,df3 = load_aux_data(df_main)
    city_lookup = dict(zip( df1['Code'].tolist() + df2['Code'].tolist() + df3['Code'].tolist(), 
                            df1['City'].tolist() + df2['City'].tolist() + df3['City'].tolist() ))
    state_lookup = dict(zip( df1['Code'].tolist()  + df2['Code'].tolist()  + df3['Code'].tolist(), 
                             df1['State'].tolist() + df2['State'].tolist() + df3['State'].tolist() ))
    airl_lookup = dict(zip( df1['Code'].tolist()    + df2['Code'].tolist(), 
                            df1['Airline'].tolist() + df2['Airline'].tolist()  ))
    descr_lookup = dict(zip( df1['Code'].tolist()    + df2['Code'].tolist(), 
                            df1['Description'].tolist() + df2['Description'].tolist()  ))

    return city_lookup,state_lookup,airl_lookup,descr_lookup

def get_hash(df,column='City'):
    """
    column = "City", "Airline", "Description"
    """
    df_air_id,df_seq_id,df_market = load_aux_data(df)
    myhash = {}
    myhash['air_id'] = dict(zip( df_air_id['Code'].tolist(), df_air_id[column].tolist() ))
    myhash['seq_id'] = dict(zip( df_seq_id['Code'].tolist(), df_seq_id[column].tolist() ))
    myhash['market'] = dict(zip( df_market['Code'].tolist(), df_market[column].tolist() ))
    return myhash
                            
def myplt():
    # bring plot up front
    plt.gcf().canvas.manager.window.activateWindow()
    
#%% === saver helper ===
def get_fileinfo(__file__):
    """ Get file info as dict 
    
    Usage
    -----
    >>> file_info = get_fileinfo(__file__)
    >>> print file_info.keys()
    ['file_name', 'output_dir', 'file_dir']
    """
    file_dir, file_name = os.path.split(__file__.rstrip('.py'))
    
    # output directory ($PWD/results/filename)
    output_dir = os.path.join(file_dir,'results',file_name)
    
    print "=== results will be saved at {} ===".format(output_dir)
    file_info = dict(
        file_name=file_name,
        file_dir=file_dir,
        output_dir=output_dir
    )
    return file_info
    
def get_outputdir(output_dir):
    """ Create output directory if it doesn't exist 
    
    I used to call this ``check_dir``
    
    Usage
    -----
    >>> file_info = get_fileinfo(__file__)
    >>> output_dir = get_outputdir(file_info['output_dir'])
    """
    if not os.path.isdir(output_dir):
        print "Directory {} doesn't exist.".format(output_dir)
        print "create directory -> " + output_dir
        os.makedirs(output_dir)
    
    
def mysavefig(outfilename,file_info,suptitle=None,fsave=True):
    """ Save figure as png."""
    plt.gcf()
    if suptitle is None:
        pass
    elif suptitle == '__file__':
        plt.suptitle(file_info['file_name'])
    elif suptitle == 'outfilename':
        plt.suptitle(outfilename)
    else:
        plt.suptitle(suptitle)
        
    if outfilename[-4:] != '.png':
        outfilename += '.png'
        
    #plt.tight_layout()
    #tw.browser('http://stackoverflow.com/questions/8248467/')
    #plt.subplots_adjust(top=1.25)
    if fsave:
        savepath = os.path.join(file_info['output_dir'],outfilename)
        print 'save result at ' + savepath
        plt.savefig(savepath,bbox_inches='tight')
        
def save_all_figs(head_str):
    for i in plt.get_fignums():
        plt.figure(i)
        plt.savefig('./figures/'+head_str+'({}).png'.format(i),bbox_inches='tight')
#%% ===
if __name__ == '__main__':
    df = load_main_data()
    df1,df2,df3 = load_aux_data()
    df_carr = load_carriers()
    df_airp = load_airports()
    dict_city,dict_state,dict_airline = get_lookup_tables()