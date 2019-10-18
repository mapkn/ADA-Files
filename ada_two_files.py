# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:15:28 2017

@author: patemi
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:59:13 2017

@author: patemi

This script allow the user to compare the statistics for a particular factor from two
separate ADA files

Optionally the time series data can be saved to a separate CSV file

"""
import pandas as pd
import os.path
import numpy as np
#import clipboard
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from functools import reduce 





items=['GOV_US,1M']

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
path1 = '\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\MSUSA T Bill Clean Price Calculation Correction'
#file1 = 'MarketArchiveSt.2018-03-13_PRD.csv'
file1 = 'UAT.MarketArchive.2018-04-24.ada'

# 2 for PROD file
path2 = '\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\MSUSA T Bill Clean Price Calculation Correction'
#file2 = 'MarketArchiveSt.2018-03-13_PRD2.csv'
file2 = 'MarketArchive.2018-04-24.ada'

# 3 for Output file
path3 = '\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\MSUSA T Bill Clean Price Calculation Correction'
file3 = 'Output.csv'



#df1=pd.read_csv(os.path.join(path1,file1), encoding='latin-1', low_memory=False, parse_dates=[0])
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


#plt.

df1_filtered.plot();
df2_filtered.plot();

# compute 1st differences of dataframe data
df1_diff=df1_filtered.diff(periods=1)
df2_diff=df2_filtered.diff(periods=1)



# Copy to clipboard the summary stats
df1_stats=df1_diff.describe(percentiles=[0.01,0.025,0.975,0.99])
df1_stats.to_clipboard()

df2_stats=df2_diff.describe(percentiles=[0.01,0.025,0.975,0.99])
df2_stats.to_clipboard()


# Count zero changes
#df_diff_0=(df_diff==0).astype(int).sum(axis=0)

#print(df_diff.describe())

# Historgram
#df_diff.hist(bins=20)


# Optionally export the data to a separate CSV (setting x=1 below)
x=1

if x==1:
    # Create DF for the output data, copy from df2
    df3=df2.copy()
    #df3.loc[:,allcols]=0
    df3.loc[:,allcols]=df1.loc[:,allcols]
    #print(df3.loc[:,allcols].head())
    df3.to_csv(os.path.join(path3,file3), float_format='%.3f')
#df3.index=int(df3.index)
#df3.to_csv(os.path.join(path3,file3))

