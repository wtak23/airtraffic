# -*- coding: utf-8 -*-
import util
import pandas as pd

df_data = util.load_airport_data()

df_counts_month = df_data.groupby(['MONTH','DAY_OF_WEEK']).count()['YEAR'].to_frame(name='counts').reset_index(level=0)
#%%
tmp = df_data.groupby(['MONTH','DAY_OF_WEEK']).count()['YEAR'].to_frame(name='counts')


tmp.un