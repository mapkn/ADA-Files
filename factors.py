# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:41:58 2019

@author: patemi
"""

import pandas as pd
import os.path
import xlwings as xw


path='\\\\FS002\\patemi$\\Python\\ADA File\\'
file = 'Factors.csv'

path_factorattributes='\\\\apw-grskfs01\\GVAR2\\Global Risk Management\\FRTB\\IMA\\Hanabi\\'
file_factorattributes = 'Memo for Market data_v3.11.xlsm'

df_factorattributes=pd.read_excel(os.path.join(path_factorattributes,file_factorattributes), sheet_name='Current PF', skiprows=1)

df_factorattributes['TimeScape ID']=df_factorattributes['TimeScape ID'].str.upper()

@xw.func
def get_factor_grid(TSID):
    # Given the TimeScape ID (which includes the tenor), return the tenor
    
    if TSID.find("SURFACE")>0:
        # Returns the two grids for a surface
        return [TSID[find_second_last(TSID,"_")+1:TSID.rfind("_")],TSID[TSID.rfind("_")+1:]]    
    else:
        return TSID[TSID.rfind("_")+1:]
    

def get_factor_name(TSID):
    # Given the TimeScape ID (which includes the tenor), return the factor name (exclude tenors)
    if TSID.find("SURFACE")>0:
        return TSID[:find_second_last(TSID,"_")]
    elif TSID.find("CURVE")>0:
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


def left(aString, howMany):
    if howMany <1:
        return ''
    else:
        return aString[:howMany]


class FXRateFactor:
    FactorCategory='FXRate'
    Currency=''
    Currency2=''
    
    def __init__(self, ccy,ccy2):
        self.Currency = ccy
        self.Currency2 = ccy2
    


def getFactorAttribute(TimeScapeCode, Attribute):
    df=df_factorattributes[df_factorattributes['TimeScape ID']==TimeScapeCode]
    #print(df['Category'].str.split

    return df[Attribute]

def getFactorGrid(TimeScapeCode):
    
    
    if TimeScapeCode.find('SURFACE')>0:
        print(TimeScapeCode.rfind('_'))
        
        return True
    else:
        return False
    
 #   df=df_factorattributes[df_factorattributes['TimeScape ID']==TimeScapeCode]
    #print(df['Category'].str.split

    #return df[Attribute]



def getFactorCategory2(TimeScapeCode):
    df=df_factorattributes[df_factorattributes['TimeScape ID']==TimeScapeCode]
    #print(df['Category'].str.split
    return df['Category']

#    return df['Category'].to_string()



x=getFactorCategory2(':BASECURVE.MUN_US')
x=getFactorAttribute(':BASECURVE.MUN_US', 'IndexID')

x=getFactorAttribute(':BASECURVE.MUN_US', 'IndexID')
z=getFactorGrid(':VOLSURFACE_JSW_JPY_25Y_25Y')


z=get_factor_grid(':VOLSURFACE_JSW_JPY_25Y_50Y')


def getFactorCategory(ADACode):
    if ADACode.find('IBR')>0:
        return 'BOR'
    elif ADACode.find('OIS')>0:
        return 'OIS'
    elif ADACode.find('BASECURVE.REP')>0:
        return 'BondRepoIndex'
    elif ADACode.find(':SPRD')>0:
        return 'CreditIndex'
    elif ADACode.find(':BASISCURVE.CCY')>0:
        return 'CurrencyBasis'
    elif len(ADACode)==2:
        return 'EquityIndex'
    #elif len(ADACode)==2:
    #    return 'EquityIndex'
    elif len(ADACode)==3:
        return 'FXRate'
    else:
        return 0
    
#def getCurrency(ADACode):
    

print(getFactorCategory('BASECURVE.REP'))
FX1=FXRateFactor('AUD','USD')


#print(FX1.Currency)
#print(FX1.Currency2)
#print(FX1.FactorCategory)





df=pd.read_csv(os.path.join(path,file),encoding='iso-8859-15', low_memory=False)





df['TimeScape Factor']=df['ADA Factor'].str.replace(',','_')


#df['TimeScape Factor']=df['ADA Factor'].str[df['ADA Factor'].str.index('.'):]


df['Loc']=df['ADA Factor'].str.index('.')



#p=df['Loc'].astype(int)


x1=df['TimeScape Factor'].str.split('.')

a=df['TimeScape Factor'].str.split('.',1).str[0]
b=df['TimeScape Factor'].str.split('.',1).str[1]
#c=df['TimeScape Factor'].str.split('.').str[2]


#x=df['TimeScape Factor'].str[df['ADA Factor'].str.index('.'):]
#string[string.find(","):string.find("r")]

#x=df['TimeScape Factor'].str[:]

#df['TimeScape Factor']=df['ADA Factor'].str[2:]
