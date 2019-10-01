# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:28:00 2018

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

# Combined database PAP and Notoria
Profitfile='pap//CombProfit.csv'
DatesFile='pap//CombDates.csv'

#Loading Stock Data Files
WIG_data=pd.read_csv('D://Doktorat Marek//dane//notowania//omegacgl//WIG.txt',header=0,index_col='Date',encoding ="UTF-8",parse_dates=True,dayfirst=True)
Stock_prices_close=pd.read_csv('D://Doktorat Marek//dane//Notowania//Stock_price_close.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')
Stock_prices_open=pd.read_csv('D://Doktorat Marek//dane//Notowania//Stock_price_open.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')

# Loading Stock Data - based on Zmiana field
Stock_returns = pd.read_csv('D://Doktorat Marek//dane//Notowania//Stock_returns.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')

#Loading Profit and Date Files
path='D://Doktorat Marek//dane//'
ProfitsFilePath=path+Profitfile
DatesFilePath=path+DatesFile
quarterly_profit=pd.read_csv(ProfitsFilePath,index_col=0,header=0,parse_dates=True)
Dates_profit=pd.read_csv(DatesFilePath,index_col=0,header=0,parse_dates=True,dtype='str')

# Correcting outliers in Quarterly Reports
quarterly_profit_corrected=PEADFunctions.ReplacingOutliers(quarterly_profit)

# Preparing Q Profit forecasts according to Model2 
Q_forecast_df=PEADFunctions.ProfitQ_forecast(quarterly_profit_corrected)

# Calculating Standardized Unexpected Error based on Earnings Surprise and
# profit standard deviation
SUE_df=PEADFunctions.SUE(quarterly_profit_corrected,Q_forecast_df)

#%%

SUE_portfolio1=PEADFunctions.SUE_portfolio(SUE_df,1,'D')
SUE_portfolio2=PEADFunctions.SUE_portfolio(SUE_df,2,'D')
SUE_portfolio3=PEADFunctions.SUE_portfolio(SUE_df,3,'D')
SUE_portfolio4=PEADFunctions.SUE_portfolio(SUE_df,4,'D')
SUE_portfolio5=PEADFunctions.SUE_portfolio(SUE_df,5,'D')
SUE_portfolio6=PEADFunctions.SUE_portfolio(SUE_df,6,'D')
SUE_portfolio7=PEADFunctions.SUE_portfolio(SUE_df,7,'D')
SUE_portfolio8=PEADFunctions.SUE_portfolio(SUE_df,8,'D')
SUE_portfolio9=PEADFunctions.SUE_portfolio(SUE_df,9,'D')
SUE_portfolio10=PEADFunctions.SUE_portfolio(SUE_df,10,'D')

#%% Calculating Portfolio returns 

period=360

Portfolio_returns10=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio10,Stock_returns,period)
Portfolio_returns9=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio9,Stock_returns,period)
Portfolio_returns8=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio8,Stock_returns,period)
Portfolio_returns7=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio7,Stock_returns,period)
Portfolio_returns6=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio6,Stock_returns,period)
Portfolio_returns5=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio5,Stock_returns,period)
Portfolio_returns4=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio4,Stock_returns,period)
Portfolio_returns3=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio3,Stock_returns,period)
Portfolio_returns2=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio2,Stock_returns,period)
Portfolio_returns1=PEADFunctions.Portfolio_returns_change_rel_WIG(Dates_profit,SUE_portfolio1,Stock_returns,period)

'''
Portfolio_returns10=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio10,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns9=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio9,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns8=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio8,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns7=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio7,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns6=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio6,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns5=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio5,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns4=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio4,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns3=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio3,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns2=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio2,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns1=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio1,Stock_prices_close,Stock_prices_open,WIG_data,period)
'''
#%% Statistical analysis of results

mean_PEAD=(Portfolio_returns10.mean(axis=1)-Portfolio_returns1.mean(axis=1)).mean()      
print("\n\n Mean PEAD Result: ",round(mean_PEAD*100,4))
mask_1Q=Portfolio_returns10.index.month==1
mask_2Q=Portfolio_returns10.index.month==4
mask_3Q=Portfolio_returns10.index.month==7
mask_4Q=Portfolio_returns10.index.month==10
mean_1Q=(Portfolio_returns10[mask_1Q].mean(1)-Portfolio_returns1[mask_1Q].mean(1)).mean()
mean_2Q=(Portfolio_returns10[mask_2Q].mean(1)-Portfolio_returns1[mask_2Q].mean(1)).mean()
mean_3Q=(Portfolio_returns10[mask_3Q].mean(1)-Portfolio_returns1[mask_3Q].mean(1)).mean()
mean_4Q=(Portfolio_returns10[mask_4Q].mean(1)-Portfolio_returns1[mask_4Q].mean(1)).mean()
print("\nMean 1Q PEAD Result: ",round(mean_1Q*100,4))
print("Mean 2Q PEAD Result: ",round(mean_2Q*100,4))
print("Mean 3Q PEAD Result: ",round(mean_3Q*100,4))
print("Mean 4Q PEAD Result: ",round(mean_4Q*100,4))
print(((Portfolio_returns10.mean(axis=1)[4:].resample('A').mean()-Portfolio_returns1.mean(axis=1)[4:].resample('A').mean())*100).dropna())
mean_year={}
for year in Portfolio_returns10.mean(1).dropna().index.year.unique():
    mask=Portfolio_returns10.index.year==year
    mean10=Portfolio_returns10[mask].mean(1).mean()
    mean9=Portfolio_returns9[mask].mean(1).mean()
    mean8=Portfolio_returns8[mask].mean(1).mean()
    mean7=Portfolio_returns7[mask].mean(1).mean()
    mean6=Portfolio_returns6[mask].mean(1).mean()
    mean5=Portfolio_returns5[mask].mean(1).mean()
    mean4=Portfolio_returns4[mask].mean(1).mean()
    mean3=Portfolio_returns3[mask].mean(1).mean()
    mean2=Portfolio_returns2[mask].mean(1).mean()
    mean1=Portfolio_returns1[mask].mean(1).mean()
    mean=((Portfolio_returns10[mask].mean(1)-Portfolio_returns1[mask].mean(1)).mean()+1)
    means=[mean,mean10,mean9,mean8,mean7,mean6,mean5,mean4,mean3,mean2,mean1]
    mean_year[str(year)]=means
for key,value in mean_year.items():
    print("{0}  first decile {2}, last decile {3},Hedge PEAD is {1}".format(key,round(value[0]*100-100,4),round(value[1]*100-100,4),round(value[10]*100-100,4)))
graph_df=pd.DataFrame(mean_year,index=['Hedge','10th','9th','8th','7th','6th','5th','4th','3rd','2nd','1st']).transpose()
graph2_df=graph_df.cumprod()
graph2_df=round((graph2_df-1)*100,4)
graph2_df.plot(figsize=(12,8),table=True,title='Cumulative perofrmance of portfolios')

#%% p value of difference of means

# Test ttest if mean of two series are the same, p>0.05 means we cant reject that they are infact equal
print("\n\n\n")
print(stats.ttest_ind(Portfolio_returns10.mean(axis=1).dropna().values,Portfolio_returns1.mean(axis=1).dropna().values))
print("10th portfolio - First decile tstat: ",stats.ttest_1samp(Portfolio_returns1.mean(1).dropna(),1))
print("1st portfolio - Tenth decile tstat: ",stats.ttest_1samp(Portfolio_returns10.mean(1).dropna(),1))

#%% SUE measure evaluation


SUE_df[SUE_portfolio10==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio10==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio10==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio9==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio9==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio9==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio8==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio8==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio8==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio7==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio7==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio7==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio6==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio6==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio6==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio5==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio5==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio5==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio4==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio4==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio4==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio3==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio3==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio3==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio2==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio2==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio2==1].mean(1).dropna(),0)

SUE_df[SUE_portfolio1==1].mean(1).resample('A').mean()
SUE_df[SUE_portfolio1==1].mean(1).mean()
stats.ttest_1samp(SUE_df[SUE_portfolio1==1].mean(1).dropna(),0)

#%% SUE portfolio moovements

def SUE_postition_movements():
    """
    Calculating mean rank in quarters after inital profit announcement
    """
    SUE_prt=SUE_portfolio10
    SUE_prt[SUE_portfolio9==1]=2
    SUE_prt[SUE_portfolio8==1]=3
    SUE_prt[SUE_portfolio7==1]=4
    SUE_prt[SUE_portfolio6==1]=5
    SUE_prt[SUE_portfolio5==1]=6
    SUE_prt[SUE_portfolio4==1]=7
    SUE_prt[SUE_portfolio3==1]=8
    SUE_prt[SUE_portfolio2==1]=9
    SUE_prt[SUE_portfolio1==1]=10
    
    q_list=SUE_prt.count(1)[SUE_prt.count(1)!=0].index
    Mean_rank=pd.DataFrame(index=q_list,columns=['mean_rank2','mean_rank3','mean_rank4','mean_rank5','mean_rank6','mean_rank7'])
    
    for i in range(0,len(q_list)-1):
        quarter=q_list[i]
        Names1=SUE_prt.loc[quarter][SUE_prt.loc[quarter]==10].index
        if i+1<len(q_list):
            quarter2=q_list[i+1]
            Mean_rank.loc[quarter,'mean_rank2']=SUE_prt.loc[quarter2,Names1].mean()
        if i+2<len(q_list):
            quarter3=q_list[i+2]
            Mean_rank.loc[quarter,'mean_rank3']=SUE_prt.loc[quarter3,Names1].mean()
        if i+3<len(q_list):
            quarter4=q_list[i+3]
            Mean_rank.loc[quarter,'mean_rank4']=SUE_prt.loc[quarter4,Names1].mean()
        if i+4<len(q_list):
            quarter5=q_list[i+4]
            Mean_rank.loc[quarter,'mean_rank5']=SUE_prt.loc[quarter5,Names1].mean()
        if i+5<len(q_list):
            quarter6=q_list[i+5]
            Mean_rank.loc[quarter,'mean_rank6']=SUE_prt.loc[quarter6,Names1].mean()
        if i+6<len(q_list):
            quarter7=q_list[i+6]
            Mean_rank.loc[quarter,'mean_rank7']=SUE_prt.loc[quarter7,Names1].mean()
        
    
    
def SUE_rank_next_q(rank=1):
    
    SUE_prt=SUE_portfolio10
    SUE_prt[SUE_portfolio9==1]=2
    SUE_prt[SUE_portfolio8==1]=3
    SUE_prt[SUE_portfolio7==1]=4
    SUE_prt[SUE_portfolio6==1]=5
    SUE_prt[SUE_portfolio5==1]=6
    SUE_prt[SUE_portfolio4==1]=7
    SUE_prt[SUE_portfolio3==1]=8
    SUE_prt[SUE_portfolio2==1]=9
    SUE_prt[SUE_portfolio1==1]=10
    q_list=SUE_prt.count(1)[SUE_prt.count(1)!=0].index
    Following_rank=pd.DataFrame(index=q_list,columns=['10th','9th','8th','7th','6th','5th','4th','3rd','2nd','1st'])
    for i in range(0,len(q_list)-1):
        quarter=q_list[i]
        Names1=SUE_prt.loc[quarter][SUE_prt.loc[quarter]==rank].index
        if i+4<len(q_list):
            quarter2=q_list[i+4]
            Following_rank.loc[quarter,'1st']=(SUE_prt.loc[quarter2,Names1]==1).sum()/len(Names1)
            Following_rank.loc[quarter,'2nd']=(SUE_prt.loc[quarter2,Names1]==2).sum()/len(Names1)
            Following_rank.loc[quarter,'3rd']=(SUE_prt.loc[quarter2,Names1]==3).sum()/len(Names1)
            Following_rank.loc[quarter,'4th']=(SUE_prt.loc[quarter2,Names1]==4).sum()/len(Names1)
            Following_rank.loc[quarter,'5th']=(SUE_prt.loc[quarter2,Names1]==5).sum()/len(Names1)
            Following_rank.loc[quarter,'6th']=(SUE_prt.loc[quarter2,Names1]==6).sum()/len(Names1)
            Following_rank.loc[quarter,'7th']=(SUE_prt.loc[quarter2,Names1]==7).sum()/len(Names1)
            Following_rank.loc[quarter,'8th']=(SUE_prt.loc[quarter2,Names1]==8).sum()/len(Names1)
            Following_rank.loc[quarter,'9th']=(SUE_prt.loc[quarter2,Names1]==9).sum()/len(Names1)
            Following_rank.loc[quarter,'10th']=(SUE_prt.loc[quarter2,Names1]==10).sum()/len(Names1)
    return Following_rank