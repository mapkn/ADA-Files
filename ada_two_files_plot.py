# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:15:28 2017

@author: patemi
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:59:13 2017

@author: patemi
"""
import pandas as pd
import os.path
import numpy as np
#import clipboard
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from functools import reduce 


items=['InterestRate.:SPRDCURVE_P.CDS_GB_FIN_AA,0Y']


multiplier=10000


def from_excel_ordinal(ordinal, epoch=datetime(1900, 1, 1)):
    # Adapted from above, thanks to @Martijn Pieters 

    ord=float(ordinal)    
    if ord > 59:
        ord -= 1  # Excel leap year bug, 1900 is not a leap year!
    inDays = int(ord)
    frac = ord - inDays
    inSecs = int(round(frac * 86400.0))
    return epoch + timedelta(days=inDays - 1, seconds=inSecs) # epoch is day 1

from_excelordinal=np.vectorize(from_excel_ordinal)

# 1 for Test
path1 = '\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\MHI Level Corrections April 2019'
file1 = 'MarketArchiveSt.2019-04-01.UAT.2.ada'

# 2 for PROD file
path2 = '\\\\apw-grskavap01\\Data\\MarketArchive\\'
file2 = 'MarketArchiveSt.2019-04-01.ada'

# Read in from file1
df1=pd.read_table(os.path.join(path1,file1), encoding='latin-1', low_memory=False, parse_dates=[1],skiprows=3)
df1=df1.set_index('DATE')
df1.index=from_excelordinal(df1.index)

# Read in from file2
df2=pd.read_table(os.path.join(path2,file2), encoding='latin-1', low_memory=False, parse_dates=[1],skiprows=3)
df2=df2.set_index('DATE')
df2.index=from_excelordinal(df2.index)


allcols=[]


for item in items:
    cols = [col for col in df1.columns if item.upper() in col.upper()]
    allcols.append(cols)

allcols=reduce(lambda x,y: x+y, allcols)


df1_filtered=multiplier*df1.filter(items=allcols, axis=1)
df2_filtered=multiplier*df2.filter(items=allcols, axis=1)

plt.plot(df1_filtered.index.tolist(), df1_filtered[items[0]])
plt.plot(df2_filtered.index.tolist(), df2_filtered[items[0]])


# compute 1st differences of dataframe data
df1_diff=df1_filtered.diff(periods=1)
df2_diff=df2_filtered.diff(periods=1)

# Scatter Plot
#df1_diff.plot.scatter(df1_diff.index, y='');


