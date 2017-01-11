# -*- coding: utf-8 -*-
""" 
Let's do basic analysis.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn.apionly as sns

from pprint import pprint

import util
reload(util)
#%%
df_data = util.load_airport_data()

