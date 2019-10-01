or r"""
Created on Tue Jun  6 17:25:10 2017

@author: marek
"""
import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset


def Date_correction(Dates_df):
    '''
    Profit Dates in Notoria are usually one year later then they sould be
    Looking if the report year and fiscal year are the same, if not changes to the fiscal year
    For 4th quarter year should be fiscal year +1
    
    '''    
    for Quarter in Dates_df.index:
        for stock in Dates_df.columns:
            if len(Dates_df.loc[Quarter,stock])==10:
                Profit_Date=pd.to_datetime(Dates_df.loc[Quarter,stock])
                try:
                    # Looking if report is not for the 4th quarter
                    if Quarter.month in [1,7]:
                        # Looking if announcement date is away more than 195 days (90 days Q+90 for announcement)
                        # from begging of the quarter
                        if (Profit_Date-Quarter)>pd.Timedelta(days=195):
                            Corrected_Date=pd.to_datetime(Dates_df.shift(4).loc[Quarter,stock])
                            if (Corrected_Date-Quarter)<pd.Timedelta(days=195) and (Corrected_Date-Quarter)>pd.Timedelta(days=91):
                                print("Date for ", Quarter, "shifted from: ",Profit_Date," to ",Corrected_Date)
                                Dates_df.loc[Quarter,stock]=Corrected_Date
                            else:
                                for Publication_Date in Dates_df[stock].values:
                                    if len(Dates_df.loc[Quarter,stock])==10:
                                        if (Publication_Date-Quarter)<pd.Timedelta(days=195) and (Publication_Date-Quarter)>pd.Timedelta(days=91):
                                            print("Found for ", Quarter, "shifted from: ",Profit_Date," to ",Corrected_Date)
                                            Dates_df.loc[Quarter,stock]=Publication_Date
                                        else:
                                            print("correcting ", stock," for period", Quarter, " Original Date is ",Dates_df.loc[Quarter,stock])
                                            Profit_Date=Profit_Date+DateOffset(years=(Quarter.year-Profit_Date.year))
                                            Dates_df.loc[Quarter,stock]=Profit_Date
                    elif Quarter.month==4:
                        # Looking if announcement date is away more than 250 days (90 days Q+90 for announcement)
                        # from begging of the quarter
                        if (Profit_Date-Quarter)>pd.Timedelta(days=250):
                            Corrected_Date=pd.to_datetime(Dates_df.shift(4).loc[Quarter,stock])
                            if (Corrected_Date-Quarter)<pd.Timedelta(days=250) and (Corrected_Date-Quarter)>pd.Timedelta(days=91):
                                print("Date for ", Quarter, "shifted from: ",Profit_Date," to ",Corrected_Date)
                                Dates_df.loc[Quarter,stock]=Corrected_Date
                            else:
                                for Publication_Date in Dates_df[stock].values:
                                    if len(Dates_df.loc[Quarter,stock])==10:
                                        if (Publication_Date-Quarter)<pd.Timedelta(days=250) and (Publication_Date-Quarter)>pd.Timedelta(days=91):
                                            print("Found for ", Quarter, "shifted from: ",Profit_Date," to ",Corrected_Date)
                                            Dates_df.loc[Quarter,stock]=Publication_Date
                                        else:
                                            print("correcting ", stock," for period", Quarter, " Original Date is ",Dates_df.loc[Quarter,stock])
                                            Profit_Date=Profit_Date+DateOffset(years=(Quarter.year-Profit_Date.year))
                                            Dates_df.loc[Quarter,stock]=Profit_Date
                    # Reports 4th Quarter announcement date will be year+1 from accounting year
                    else:
                        # Looking if announcement date is away more than 240 days (90 days Q+150 for announcement)
                        # from begging of the quarter
                        if (Profit_Date-Quarter)>pd.Timedelta(days=270):
                            Corrected_Date=pd.to_datetime(Dates_df.shift(4).loc[Quarter,stock])
                            if (Corrected_Date-Quarter)<pd.Timedelta(days=270) and (Corrected_Date-Quarter)>pd.Timedelta(days=91):
                                print("Date for ", Quarter, "shifted from: ",Profit_Date," to ",Corrected_Date)
                                Dates_df.loc[Quarter,stock]=Corrected_Date
                            else:
                                for Publication_Date in Dates_df[stock].values:
                                    if len(Dates_df.loc[Quarter,stock])==10:
                                        if (Publication_Date-Quarter)<pd.Timedelta(days=195) and (Publication_Date-Quarter)>pd.Timedelta(days=91):
                                            print("Found for ", Quarter, "shifted from: ",Profit_Date," to ",Corrected_Date)
                                            Dates_df.loc[Quarter,stock]=Publication_Date
                                        else:
                                            print("correcting ", stock," for period", Quarter, " Date is ",Dates_df.loc[Quarter][stock])
                                            Profit_Date=Profit_Date+DateOffset(years=(Quarter.year-Profit_Date.year+1))
                                            Dates_df.loc[Quarter,stock]=Profit_Date
                except:
                    pass
    return Dates_df


def LoadingExcelData():
    '''
    function loading and preprocessing Excel produced csv files
    saves as csv pandas DataFrame
    '''
    # Loading stocks info from Notoria files
    NotoriaNamesFile='D://Doktorat Marek//dane//Notoria Names data.csv'
    Notoriadata=pd.read_csv(NotoriaNamesFile,parse_dates=True,sep=',',index_col=0,header=0)
    GPW_names_list=list(Notoriadata[Notoriadata['Rynek']=='GPW'].index)
    # Creating file NoShares based on Notoria Names data.csv'
    Notoria_NoShares=pd.DataFrame(index=pd.date_range('19980101','20170701',freq='QS-JAN'),columns=GPW_names_list)
    Notoria_NoShares.loc['19980101',GPW_names_list]=Notoriadata.loc[GPW_names_list,'Number of shares']
    Notoria_NoShares.fillna(method='ffill',inplace=True)
    Notoria_NoShares.to_csv('D://Doktorat Marek//dane//NoShares.csv',encoding = "UTF-8")
    #Data loading from Excel exported sheet Profit csv
    quarterly_profit=pd.read_csv('D://Doktorat Marek//dane//Zyski z notorii Profit.csv',sep=',',encoding = "UTF-8",index_col='names',header=0)
    quarterly_profit.drop(quarterly_profit.columns[[0]],axis=1,inplace=True)
    quarterly_profit.columns=pd.to_datetime(quarterly_profit.columns)
    quarterly_profit=quarterly_profit.transpose()
    Notoria_Profit=quarterly_profit.loc[:,GPW_names_list]
    Notoria_Profit.to_csv('D://Doktorat Marek//dane//Profits.csv',encoding = "UTF-8")
    
    
    # Data loading from Excecl exportet sheet PubDates
    Dates_profit=pd.read_csv('D://Doktorat Marek//dane//Zyski z notorii PubDates.csv',sep=',',encoding = "UTF-8",index_col='names',header=0)
    Dates_profit.drop(Dates_profit.columns[[0]],axis=1,inplace=True)
    Dates_profit.columns=pd.to_datetime(Dates_profit.columns)
    Dates_profit=Dates_profit.transpose()
    Notoria_Dates=Dates_profit.loc[:,GPW_names_list]
    Notoria_Dates=Date_correction(Notoria_Dates)
    Notoria_Dates.to_csv('D://Doktorat Marek//dane//ProfitDates.csv',encoding = "UTF-8")
