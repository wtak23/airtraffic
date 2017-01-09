# -*- coding: utf-8 -*-
#%%
from tak import reset; reset()

import tak as tw
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import os
import time
os.getcwd()

from util import *
#%%
for i in range(5):
    plt.figure();
    plt.plot(np.random.randn(500,1))
    
save_all_figs(os.path.basename(__file__)[:-3])