# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:30:19 2018

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

#PAP konsensus analsts forecasts
Profitfile='pap//PAPProfit.csv'
DatesFile='pap//PAPDates.csv'
KonsensusFile='pap//Konsensusy.csv'


#Loading Stock Data Files
WIG_data=pd.read_csv('D://Doktorat Marek//dane//notowania//omegacgl//WIG.txt',header=0,index_col='Date',encoding ="UTF-8",parse_dates=True,dayfirst=True)
Stock_prices_close=pd.read_csv('D://Doktorat Marek//dane//Notowania//Stock_price_close.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')
Stock_prices_open=pd.read_csv('D://Doktorat Marek//dane//Notowania//Stock_price_open.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')

#Loading Profit and Date Files
path='D://Doktorat Marek//dane//'
ProfitsFilePath=path+Profitfile
DatesFilePath=path+DatesFile
KonsensusFilePath=path+KonsensusFile
quarterly_profit=pd.read_csv(ProfitsFilePath,index_col=0,header=0,parse_dates=True)
Dates_profit=pd.read_csv(DatesFilePath,index_col=0,header=0,parse_dates=True,dtype='str')
Q_forecast_df=pd.read_csv(KonsensusFilePath,index_col=0,header=0,parse_dates=True)
Konsensus_Names=Q_forecast_df.columns.tolist()

# Correcting outliers in Quarterly Reports
quarterly_profit_corrected=PEADFunctions.ReplacingOutliers(quarterly_profit)

quarterly_profit_konsensus=quarterly_profit_corrected.reindex(Q_forecast_df.index)
quarterly_profit_konsensus=quarterly_profit_konsensus[Konsensus_Names]
quarterly_profit_konsensus=quarterly_profit_konsensus[Q_forecast_df.notnull()]
SUE_df=PEADFunctions.SUE_konsensus(quarterly_profit_konsensus,quarterly_profit_corrected,Q_forecast_df)

#%%

period=10


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
    print('In Year '+ str(year)+' Hedge:'+str(round((mean-1)*100,4))+
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


#%% SUE portfolio moovements

def SUE_postition_movements():
    """
    Calculating mean rank in quarters after inital profit announcement
    """
    SUE_prt=SUE_portfolio4
    SUE_prt[SUE_portfolio3==1]=2
    SUE_prt[SUE_portfolio2==1]=3
    SUE_prt[SUE_portfolio1==1]=4
    
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
    
    SUE_prt=SUE_portfolio4
    SUE_prt[SUE_portfolio3==1]=2
    SUE_prt[SUE_portfolio2==1]=3
    SUE_prt[SUE_portfolio1==1]=4
    
    q_list=SUE_prt.count(1)[SUE_prt.count(1)!=0].index
    Following_rank=pd.DataFrame(index=q_list,columns=['4th','3rd','2nd','1st'])
    for i in range(0,len(q_list)-1):
        quarter=q_list[i]
        Names1=SUE_prt.loc[quarter][SUE_prt.loc[quarter]==rank].index
        if i+4<len(q_list):
            quarter2=q_list[i+4]
            Following_rank.loc[quarter,'1st']=(SUE_prt.loc[quarter2,Names1]==1).sum()/len(Names1)
            Following_rank.loc[quarter,'2nd']=(SUE_prt.loc[quarter2,Names1]==2).sum()/len(Names1)
            Following_rank.loc[quarter,'3rd']=(SUE_prt.loc[quarter2,Names1]==3).sum()/len(Names1)
            Following_rank.loc[quarter,'4th']=(SUE_prt.loc[quarter2,Names1]==4).sum()/len(Names1)
    return Following_rank