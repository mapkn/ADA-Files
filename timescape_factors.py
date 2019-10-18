# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:06:10 2019

@author: patemi
"""
import pandas as pd
import os.path

#path='\\\\FS002\\patemi$\\'

path='\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\FRTB\\IMA\\Hanabi\\'


#file = 'Gold Items - Hanabi Inclusion Status - Snapshot_20190425.xlsm'
file = 'TimeScapeMetaData.xlsx'


#\\fs002\patemi$\Python\ADA File\factors.py

#df=pd.read_excel(os.path.join(path,file), sheet_name='Counts')
df=pd.read_excel(os.path.join(path,file), sheet_name='Factors')


def get_factor_grid(TSID):
    # Given the TimeScape ID (which includes the tenor), return the tenor
    
    if TSID.find("Surface")>0:
        return [TSID[find_second_last(TSID,"_")+1:TSID.rfind("_")],TSID[TSID.rfind("_")+1:]]    
    else:
        return TSID[TSID.rfind("_")+1:]
    

def get_factor_name(TSID):
    # Given the TimeScape ID (which includes the tenor), return the factor name (exclude tenors)
    
    if TSID.upper().find("SURFACE")>0:
        return TSID[:find_second_last(TSID,"_")]
    elif TSID.upper().find("CURVE")>0:
        return TSID[:TSID.rfind("_")]
    else:
        return TSID


def find_nth(string, substring, n):
    if (n == 1):
       return string.find(substring)
    else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)

def find_second_last(text, pattern):
   return text.rfind(pattern, 0, text.rfind(pattern))




factor_names=df[['Timescape Code']].applymap(get_factor_name)
#factor_names=df[['Code']].loc[df['Hanabi?']=='Yes'].applymap(get_factor_name)

#factor_names=pd.DataFrame(factor_names['Timescape Code'].unique())

#factor_names.to_clipboard()
print(factor_names)


factor_grids=df[['Timescape Code']].applymap(get_factor_grid)

