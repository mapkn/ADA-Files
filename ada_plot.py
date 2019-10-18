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

import matplotlib.pyplot as plt
import seaborn as sns


from datetime import datetime, timedelta
from functools import reduce 



#items=['IBR_JPY']
items=['JSCC']
#items=['BASISCURVE.CCY_SGD']

#items=['JP.:VolCurve']


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


#PROD
path='\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\LCH JSCC Basis Price Factor'

file = 'MarketArchive.2018-10-09.ada'

df_input=pd.read_table(os.path.join(path,file), skiprows=3, index_col='DATE')
#df_input=df_input.set_index('DATE')
df_input.index=from_excelordinal(df_input.index)

allcols=[]


for item in items:
    cols = [col for col in df_input.columns if item.upper() in col.upper()]
    #cols = [col for col in df_input.columns if (item.upper() in col.upper() and ',5Y' in col.upper()) ]
    allcols.append(cols)

allcols=reduce(lambda x,y: x+y, allcols)


df_filtered=df_input.filter(items=allcols, axis=1)



fig=plt.figure(figsize=(7, 4))

#ax=sns.tsplot(df_filtered['InterestRate.:BASECURVE.IBR_SGD,10Y'])


plt.plot(df_filtered, label=df_filtered.columns.values)


plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
#df_filtered.plot();

plt.show()



