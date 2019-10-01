# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:37:38 2019

@author: marek
"""

import os
os.chdir('D://Doktorat Marek//dane')

import pandas as pd
import numpy as np
from pandas.tseries.offsets import Day,QuarterBegin
from scipy import stats
import statsmodels.api as sm
import math

import stockdata
import PEADFunctions

#%%

class StockPrices ():
    
    def __init__(self,PricesArray):
        self.Prices = PricesArray
        
    def ReturnLastPeriodDays(self,period):
        PeriodReturns = self.Prices.rolling(period).apply(lambda x: np.prod(x),'raw=True')
        return PeriodReturns
    
    def ReturnNextPeriodDays(self,period):
        PeriodReturns = self.Prices.rolling(period).apply(lambda x: np.prod(x),'raw=True').shift(-period)
        return PeriodReturns
    
    def ReturnLastPeriodDaysRelWIG(self,period):
        PeriodReturns = self.Prices.rolling(period).apply(lambda x: np.prod(x),'raw=True')
        PeriodReturns = PeriodReturns.add(1-PeriodReturns['WIG'],axis=0)
        return PeriodReturns
    
    def ReturnNextPeriodDaysRelWIG(self,period):
        PeriodReturns = self.Prices.rolling(period).apply(lambda x: np.prod(x),'raw=True').shift(-period)
        PeriodReturns = PeriodReturns.add(1-PeriodReturns['WIG'],axis=0)
        return PeriodReturns
    
    def ReturnRank(self,numberOfPortfolios,period):
        PercentageRank = self.ReturnLastPeriodDaysRelWIG(period).rank(axis=1,pct=True)
        PortfolioRank = round(PercentageRank*numberOfPortfolios+0.499,0)
        return PortfolioRank
    
    def RankPortfolio(self,PortfolioRank,numberOfPortfolios,period):
        Portfolio = self.ReturnRank(numberOfPortfolios,period)
        Portfolio[Portfolio != PortfolioRank]=None
        Portfolio[Portfolio == PortfolioRank]=1
        return Portfolio
    
    def RankPortfolioReturn(self,investmentPeriod,PortfolioRank,numberOfPortfolios,period):
        Portfolio = self.RankPortfolio(PortfolioRank,numberOfPortfolios,period)
        ReturnArray = self.ReturnNextPeriodDays(investmentPeriod)
        PortfolioReturn = Portfolio.multiply(ReturnArray)
        return PortfolioReturn

    def MomentumTable(self,PortfolioRank,numberOfPortfolios):
        signalPeriod = [10,30,60,90,360]
        investmentPeriod = [10,30,60,90,120,180,360]
        MomentumTable = pd.DataFrame(index=signalPeriod,columns=investmentPeriod)
        for signalDays in MomentumTable.index:
            Portfolio = self.RankPortfolio(PortfolioRank,numberOfPortfolios,signalDays)
            for investmentDays in MomentumTable.columns:
                ReturnArray = self.ReturnNextPeriodDaysRelWIG(investmentDays)
                PortfolioReturn = Portfolio.multiply(ReturnArray)
                MeanReturn = round(((PortfolioReturn.sum(1)/PortfolioReturn.count(1)).mean()-1)*100,3)
                MomentumTable.loc[signalDays,investmentDays] = MeanReturn
        return MomentumTable
        
            
    
#%%
        
        
Returns_csv = pd.read_csv('D://Doktorat Marek//dane//Notowania//Stock_returns.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')

Returns = StockPrices(Returns_csv)

#%%

P1=Returns.RankPortfolioReturn(30,1,4,30)
P4=Returns.RankPortfolioReturn(30,4,4,30)

print('Worst portfolio performance '+str(round(((P1.sum(1)/P1.count(1)).mean()-1)*100,3))+'%')
print('Best portfolio performance ' +str(round(((P4.sum(1)/P4.count(1)).mean()-1)*100,3))+'%')
print()

(P4.sum(1)/P4.count(1)).resample('A').mean()
(P4.sum(1)/P4.count(1)).resample('A').mean()
#%%

MomentumTable = pd.DataFrame(index=[10,30,60,90,360],columns=[10,30,60,90,120,180,360])
for period in MomentumTable.index:
    for investmentPeriod in MomentumTable.columns:
        PortfolioPerformance = Returns.RankPortfolioReturn(investmentPeriod,4,4,period)
        MeanReturn = round(((PortfolioPerformance.sum(1)/PortfolioPerformance.count(1)).mean()-1)*100,3)
        MomentumTable.loc[period,investmentPeriod] = MeanReturn
    