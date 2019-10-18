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

from datetime import datetime, timedelta
from functools import reduce 



items=['RFR']
#items=['IBR_SGD,1M','IBR_SGD,2M']
#items=['JP.:VolCurve']


multiplier=0.0001


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


#PROD
path = '\\\\apw-grskfs01\\GVAR2\\MikeC\\ADA'

file = 'MarketArchive.2019-10-10.ada'

df_input=pd.read_table(os.path.join(path,file), skiprows=3)
df_input=df_input.set_index('DATE')
df_input.index=from_excelordinal(df_input.index)

items =list(df_input.columns.values)

allcols=[]


for item in items:
    cols = [col for col in df_input.columns if item.upper() in col.upper()]
    #cols = [col for col in df_input.columns if (item.upper() in col.upper() and ',5Y' in col.upper()) ]
    allcols.append(cols)

#
#for item in items:
#    cols = [col for col in df_input.columns if item.upper() in col.upper()]
#    #cols = [col for col in df_input.columns if (item.upper() in col.upper() and ',5Y' in col.upper()) ]
#    allcols.append(cols)

allcols=reduce(lambda x,y: x+y, allcols)


df_filtered=df_input.filter(items=allcols, axis=1)

# compute 1st differences of dataframe data
df_diff=multiplier*df_filtered.diff(periods=1)



# Count zero changes
df_diff_0=(df_diff==0).astype(int).sum(axis=0)


df_diff_0_1=(df_diff==0).tail(10).astype(int).sum(axis=0)



# Copy to clipboard the summary stats
x=df_diff.describe(percentiles=[0.01,0.025,0.975,0.99])
x.to_clipboard()








