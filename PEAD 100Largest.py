# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:36:51 2018

@author: marek
"""

#%%
import os
os.chdir('D://Doktorat Marek//dane')

import pandas as pd
from scipy import stats
import statsmodels.api as sm

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

Mask_100=PEADFunctions.Largest100()
#Largest 100
SUE_df=SUE_df[Mask_100==1]
# Small
# Comb less Largest100
#SUE_df=SUE_df[Mask_100!=1]

period=180


SUE_portfolio1=PEADFunctions.SUE_portfolio(SUE_df,1,'QR')
SUE_portfolio2=PEADFunctions.SUE_portfolio(SUE_df,2,'QR')
SUE_portfolio3=PEADFunctions.SUE_portfolio(SUE_df,3,'QR')
SUE_portfolio4=PEADFunctions.SUE_portfolio(SUE_df,4,'QR')

Portfolio_returns4=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio4,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns3=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio3,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns2=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio2,Stock_prices_close,Stock_prices_open,WIG_data,period)
Portfolio_returns1=PEADFunctions.Portfolio_returns_rel_WIG(Dates_profit,SUE_portfolio1,Stock_prices_close,Stock_prices_open,WIG_data,period)

#%% Statistical analysis for quartiles

mean_PEAD=(Portfolio_returns4.mean(axis=1)-Portfolio_returns1.mean(axis=1)).mean()      
print("\n\n Mean PEAD in ",period," days Result: ",round(mean_PEAD*100,4),"%\n\n")

mean_year={}
for year in Portfolio_returns1.index.year.unique():
    mask=Portfolio_returns1.index.year==year
    mean1=Portfolio_returns1[mask].mean(1).mean()
    mean2=Portfolio_returns2[mask].mean(1).mean()
    mean3=Portfolio_returns3[mask].mean(1).mean()
    mean4=Portfolio_returns4[mask].mean(1).mean()
    mean=((Portfolio_returns4[mask].mean(1)-Portfolio_returns1[mask].mean(1)).mean()+1)
    means=[mean4,mean3,mean2,mean1,mean]
    print('In Year '+ str(year)+' Hedge:'+str(round((mean)*100,4))+
          '  1st:'+str(round((mean4-1)*100,4))+'  2nd:'+str(round((mean3-1)*100,4))+
          '  3rd:'+str(round((mean2-1)*100,4))+'  4th:'+str(round((mean1-1)*100,4))+'\n')
    mean_year[str(year)]=means
PEAD_by_year=((Portfolio_returns4.mean(axis=1)[4:].resample('A').mean()-Portfolio_returns1.mean(axis=1)[4:].resample('A').mean())*100).dropna()
#PEAD_first=((Portfolio_returns4.mean(axis=1)[4:].resample('A').mean()-1)*100).dropna()
#PEAD_last=((Portfolio_returns1.mean(axis=1)[4:].resample('A').mean()-1)*100).dropna()
print('Mean for 1st Portfolio: '+str(round((Portfolio_returns4.mean(axis=1).mean()-1)*100,4))+'%')
print('Mean for 2nd Portfolio: '+str(round((Portfolio_returns3.mean(axis=1).mean()-1)*100,4))+'%')
print('Mean for 3rd Portfolio: '+str(round((Portfolio_returns2.mean(axis=1).mean()-1)*100,4))+'%')
print('Mean for 4th Portfolio: '+str(round((Portfolio_returns1.mean(axis=1).mean()-1)*100,4))+'%')
print('\n')
print('mean PEAD = ' + str(round(PEAD_by_year.mean(),4)),'\n',PEAD_by_year,'\n')

graph_df=pd.DataFrame(mean_year,index=['First','Second','Third','Fourth','Hedge']).transpose()
graph2_df=graph_df.cumprod()
graph2_df=round((graph2_df-1)*100,4)
graph2_df.plot(figsize=(14,10),table=True,title='Cumulative perofrmance of portfolios rel to WIG')

Hedge=(Portfolio_returns4.mean(1).dropna().cumprod()-1)*100-(Portfolio_returns1.mean(1).dropna().cumprod()-1)*100
First=(Portfolio_returns4.mean(1).dropna().cumprod()-1)*100
Second=(Portfolio_returns3.mean(1).dropna().cumprod()-1)*100
Third=(Portfolio_returns2.mean(1).dropna().cumprod()-1)*100
Fourth=(Portfolio_returns1.mean(1).dropna().cumprod()-1)*100
#graph_data=pd.concat([Hedge,First,Second,Third,Fourth],axis=1)
#graph_data.columns=['Hedge','First','Second','Third','Fourth']
print('\n',stats.ttest_ind(Portfolio_returns4.mean(axis=1).dropna().values,Portfolio_returns1.mean(axis=1).dropna().values))
print("4th portfolio - First decile tstat: ",stats.ttest_1samp(Portfolio_returns1.mean(1).dropna(),1))
print("3rd portfolio - Second decile tstat: ",stats.ttest_1samp(Portfolio_returns2.mean(1).dropna(),1))
print("2nd portfolio - Third decile tstat: ",stats.ttest_1samp(Portfolio_returns3.mean(1).dropna(),1))
print("1st portfolio - Last decile tstat: ",stats.ttest_1samp(Portfolio_returns4.mean(1).dropna(),1))

#%% SUE measure evaluation

print('\nMean SUE measures for First Portfolio')
print(SUE_df[SUE_portfolio4==1].mean(1).resample('A').mean())
print('First Portfolio mean SUE measure ',SUE_df[SUE_portfolio4==1].mean(1).mean())
print('First Portfolio tstat SUE is nill ',stats.ttest_1samp(SUE_df[SUE_portfolio4==1].mean(1).dropna(),0),'\n')

print('\nMean SUE measures for Second Portfolio')
print(SUE_df[SUE_portfolio3==1].mean(1).resample('A').mean())
print('Second Portfolio mean SUE measure ',SUE_df[SUE_portfolio3==1].mean(1).mean())
print('Second Portfolio tstat SUE is nill ',stats.ttest_1samp(SUE_df[SUE_portfolio3==1].mean(1).dropna(),0))

print('\nMean SUE measures for Third Portfolio')
print(SUE_df[SUE_portfolio2==1].mean(1).resample('A').mean())
print('Third Portfolio mean SUE measure ',SUE_df[SUE_portfolio2==1].mean(1).mean())
print('Third Portfolio tstat SUE is nill ',stats.ttest_1samp(SUE_df[SUE_portfolio2==1].mean(1).dropna(),0))

print('\nMean SUE measures for Fourth Portfolio')
print(SUE_df[SUE_portfolio1==1].mean(1).resample('A').mean())
print('Fourth Portfolio mean SUE measure ',SUE_df[SUE_portfolio1==1].mean(1).mean())
print('Fourth Portfolio tstat SUE is nill ',stats.ttest_1samp(SUE_df[SUE_portfolio1==1].mean(1).dropna(),0))

