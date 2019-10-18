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
#import mplcursors


#items=['IBR_JPY']
#items=['IBR_SGD,1M','IBR_SGD,2M']
#items=['JP.:VolCurve']
#:SPRDCURVE.BND_EURO_FIN_BBB
#:SPRDCURVE.BND_GB_FIN_BBB
#:SPRDCURVE.CDS_GB_FIN_A
#:SPRDCURVE.SUP_EUR
#:SPRDCURVE.BND_US_FINANCIAL_A-BBB
#:BASISCURVE.CCY_EUR
#:BASISCURVE.LBR_JPY_6M_L-T
#:SPRDCURVE.BND_GB_FIN_A

#items=['BND_EURO_FIN_BBB,7Y', 'BND_GB_FIN_BBB,5Y']

items=[':SPRDCURVE.BND_US_FINANCIAL_A-BBB,3Y', ':SPRDCURVE.BND_US_FINANCIAL_A-BBB,5Y']

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
#path = '\\\\apw-grskavap01\\Data\MarketArchive'
#file = 'MarketArchive.2018-05-18.ada'

#path='\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\StressedVaR Period Change Apr 2019\\ADA Files'
file = 'MarketArchiveSt.2019-07-31.ada'
#file = 'MarketArchiveSt.2019-03-14.ada'


#df_input=pd.read_table(os.path.join(path,file), skiprows=3)
df_input=pd.read_table(file, skiprows=3)
df_input=df_input.set_index('DATE')
df_input.index=from_excelordinal(df_input.index)

allcols=[]


for item in items:
    cols = [col for col in df_input.columns if item.upper() in col.upper()]
    #cols = [col for col in df_input.columns if (item.upper() in col.upper() and ',5Y' in col.upper()) ]
    allcols.append(cols)

allcols=reduce(lambda x,y: x+y, allcols)


# Plot the time series
df_filtered=df_input.filter(items=allcols, axis=1)
#df_filtered=multiplier*df_filtered
df_filtered.plot();




# compute 1st differences of dataframe data
df_diff=multiplier*df_filtered.diff(periods=1)


# Draw the empirical pdf
df_diff.hist(cumulative=False,bins=90)

# Draw the empirical cdf
df_diff.hist(cumulative=True,bins=90)

#mplcursors.cursor().connect("add", lambda sel: sel.annotation.set_text(df_diff['Index'][sel.target.index]))


#mplcursors.cursor(lines)

#data = [go.Histogram(y=df_diff['InterestRate.:SPRDCURVE.BND_EURO_FIN_BBB,7Y'])]

#layout = go.Layout(title='Hover over the points to see the text')

#fig = go.Figure(data=data, layout=layout)
#py.iplot(fig, filename='hover-chart-basic')
#plotly.offline.plot(fig, filename='hover-chart-basic')


