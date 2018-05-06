import datetime
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format

# Read the data panel
fileDir = "E:\code\gateway\db_panel.h5"
panel = pd.read_hdf(fileDir)
datetime_index = panel.major_axis
panel.size