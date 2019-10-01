# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:48:10 2019

@author: marek
"""

#%%
import os
os.chdir('D://Doktorat Marek//dane')

import pandas as pd
import numpy as np
from pandas.tseries.offsets import Day,QuarterBegin
from scipy import stats
import statsmodels.api as sm

import stockdata
import PEADFunctions


#%%
# Loading Data from csv processed earlier

#PAP files full hitory filled with Notoria 2004-2017
Profitfile='pap//PAPProfit.csv'
DatesFile='pap//PAPDates.csv'

# Loading Stock Data - based on Zmiana field
Stock_returns = pd.read_csv('D://Doktorat Marek//dane//Notowania//Stock_returns.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')

#Loading Profit and Date Files
path='D://Doktorat Marek//dane//'
ProfitsFilePath=path+Profitfile
DatesFilePath=path+DatesFile
Dates_profit=pd.read_csv(DatesFilePath,index_col=0,header=0,parse_dates=True,dtype='str')



#%% Creating Performance after profit announcement

period = 1

Portfolio_returns = pd.DataFrame(index=Dates_profit.index,columns=Dates_profit.columns)
Stock_returns_period = Stock_returns.rolling(period).apply(lambda x: np.prod(x),'raw=True').shift(-period)
for stock in Portfolio_returns.columns.tolist():
    for quarter in Portfolio_returns.index.tolist():
        if pd.notna(Dates_profit.loc[quarter,stock]):
            Profit_Date=pd.to_datetime(Dates_profit.loc[quarter,stock])
            if Profit_Date.hour>9 or Profit_Date.hour==0:
                Start_Date = (Profit_Date+pd.offsets.Day(1)).date()
            else:
                Start_Date = Profit_Date.date()
            Portfolio_returns.loc[quarter,stock] = Stock_returns_period.loc[Start_Date,stock]/Stock_returns_period.loc[Start_Date,'WIG']

(Portfolio_returns.mean(1).mean()-1)*100
#%% Statistical analysis of results

mean_PEAD=(Portfolio_returns.mean(axis=1)-1).mean()      
print("\n\n Mean PEAD Result: ",round(mean_PEAD*100,4))
mask_1Q=Portfolio_returns.index.month==1
mask_2Q=Portfolio_returns.index.month==4
mask_3Q=Portfolio_returns.index.month==7
mask_4Q=Portfolio_returns.index.month==10
mean_1Q=(Portfolio_returns[mask_1Q].mean(1)-1).mean()
mean_2Q=(Portfolio_returns[mask_2Q].mean(1)-1).mean()
mean_3Q=(Portfolio_returns[mask_3Q].mean(1)-1).mean()
mean_4Q=(Portfolio_returns[mask_4Q].mean(1)-1).mean()
print("\nMean 1Q PEAD Result: ",round(mean_1Q*100,4))
print("Mean 2Q PEAD Result: ",round(mean_2Q*100,4))
print("Mean 3Q PEAD Result: ",round(mean_3Q*100,4))
print("Mean 4Q PEAD Result: ",round(mean_4Q*100,4))
print(((Portfolio_returns.mean(axis=1)[4:].resample('A').mean()-1)*100).dropna())
#%% p value of difference of means

# Test ttest if mean of two series are the same, p>0.05 means we cant reject that they are infact equal
print("\n\n\n")
print(stats.ttest(Portfolio_returns.mean(axis=1).dropna().values).dropna().values)
