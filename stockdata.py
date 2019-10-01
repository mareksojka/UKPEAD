# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:53:32 2017

@author: marek
"""
import os
from datetime import timedelta,datetime
import pandas as pd
import QuandlData

    
def stock_return_period(Notoria_Stock_Name,stock_data, Date,period,version='Close'):
    '''
    Input Name from Notoria database
    Date - to pandas parser
    period in days - int
    version of market 'Open','Close','High,'Low'
    returns float type value
    return as index (1+ return)
    '''
    try:
        Date = pd.to_datetime(Date)
        DateinStockDataStart = stock_data.index.get_loc(Date,method='pad')
    except:
        print("Cant find index in stock price Data Frame ", Notoria_Stock_Name, "for date: ", Date)
        return None
    try:
        StartDate=stock_data.index[DateinStockDataStart]
    except:
        print("Cant find Date for ", Notoria_Stock_Name, "at index ", DateinStockDataStart)
        return None 
    try:    
        EndDate=stock_data.index[DateinStockDataStart]+timedelta(days=period)
    except:
        print("Cant find index in stock price Data Frame ", Notoria_Stock_Name, "for date: ", Date," + ",period)
        return None     
    try:
        DateinStockDataEnd=stock_data.index.get_loc(EndDate,method='pad')
    except:
        print("Cant find Date for ", Notoria_Stock_Name, "at index ", EndDate)
        return None
            
    stockPriceStart=stock_data[version].iloc[DateinStockDataStart]
    stockPriceEnd=stock_data[version].iloc[DateinStockDataEnd]
    try:
        if EndDate>StartDate:
            stockReturn=stockPriceEnd/stockPriceStart
        else:
            stockReturn=stockPriceStart/stockPriceEnd
    except ZeroDivisionError:
        stockReturn=1
        print('Price at ', EndDate,'or ',StartDate, ' does not exist')           
           
    return stockReturn

def Stock_return_to_next(Notoria_Stock_Name,Dates_df,stock_data,Quarter,version='Close'):
    '''
    Input
    Notoria_stock_Name - stock name from Notoria database
    Dates_df - DataFramce object read from file ProfitDates.csv, includes set of announcement dates for companies
    stock_data - DataFrame with stock price data for Stock
    Quarter - date quarter start date like '2016-10-01', day is always '01'
    version - verison of price, default 'Close' option 'Open'
    returns return index as 1+return for period date to next Quarter annoucement date
    
    '''
    try:
        StartDate = Dates_df[Notoria_Stock_Name][Quarter]
        DateinStockDataStart = stock_data.index.get_loc(StartDate,method='pad')
        EndQuarterLoc = Dates_df[Notoria_Stock_Name].index.get_loc(Quarter)+1
        EndDate = Dates_df[Notoria_Stock_Name][EndQuarterLoc]
        DateinStockDataEnd = stock_data.index.get_loc(EndDate,method='pad')
    except:
        print("Date in stock data for ", Notoria_Stock_Name, "not avaialble at: ", StartDate)
        return None
    stockPriceStart = stock_data[version].iloc[DateinStockDataStart]
    stockPriceEnd = stock_data[version].iloc[DateinStockDataEnd]
    try:
        if EndDate>StartDate:
            stockReturn=stockPriceEnd/stockPriceStart
        else:
            stockReturn=stockPriceStart/stockPriceEnd
    except ZeroDivisionError:
        stockReturn=1
        print('Price at ', EndDate,'or ',StartDate, ' does not exist')           
           
    return stockReturn
    
def Generating_stock_price_table():
    """
    The function generates and returns a combined table with names of stocks
    in columns and quarter start dates in indexes. Profit tables for individual
    stocks are taken from stock_prices function.
    There are verions Open or Close
    """
    #Getting Names list
    Profitfile='pap//CombProfit.csv'
    path='D://Doktorat Marek//dane//'
    ProfitsFilePath=path+Profitfile
    quarterly_profit=pd.read_csv(ProfitsFilePath,index_col=0,header=0,parse_dates=True)
    Names_list=quarterly_profit.columns.tolist()
    
    Stock_prices_close=pd.DataFrame(index=pd.date_range('19980101','20171201',freq='D'),columns=Names_list)
    Stock_prices_open=pd.DataFrame(index=pd.date_range('19980101','20171201',freq='D'),columns=Names_list)
    for name in Names_list:
        Stock_prices_close[name]=stock_prices(name)['Close']
        Stock_prices_open[name]=stock_prices(name)['Open']
        Stock_prices_close[name].replace(to_replace=0,value=None,inplace=True)
        Stock_prices_open[name].replace(to_replace=0,value=None,inplace=True)
        Stock_prices_open.fillna(Stock_prices_close,inplace=True)
        Stock_prices_close[name].fillna(method='ffill',inplace=True)
        Stock_prices_close[name].fillna(method='bfill',inplace=True)
        Stock_prices_open[name].fillna(method='ffill',inplace=True)
        Stock_prices_open[name].fillna(method='bfill',inplace=True)
    FileClose='D://Doktorat Marek//dane//Notowania//Stock_price_close.csv'
    FileOpen='D://Doktorat Marek//dane//Notowania//Stock_price_open.csv'
    Stock_prices_close.to_csv(FileClose,encoding='UTF-8')
    Stock_prices_open.to_csv(FileOpen,encoding='UTF-8')
    return 0

def Generating_stock_daily_return_table():
    """
    The function generates and returns a combined table with names of stocks
    in columns and quarter start dates in indexes. Profit tables for individual
    stocks are taken from stock_prices function.
    There are verions Open or Close
    """
    #Getting Names list
    Profitfile='pap//CombProfit.csv'
    path='D://Doktorat Marek//dane//'
    ProfitsFilePath=path+Profitfile
    quarterly_profit=pd.read_csv(ProfitsFilePath,index_col=0,header=0,parse_dates=True)
    Names_list=quarterly_profit.columns.tolist()
    
    Stock_prices_close=pd.DataFrame(index=pd.date_range('19980101','20171201',freq='D'),columns=Names_list)
    Stock_prices_open=pd.DataFrame(index=pd.date_range('19980101','20171201',freq='D'),columns=Names_list)
    for name in Names_list:
        Stock_prices_close[name]=stock_prices(name)['Close']
        Stock_prices_open[name]=stock_prices(name)['Open']
        Stock_prices_close[name].replace(to_replace=0,value=None,inplace=True)
        Stock_prices_open[name].replace(to_replace=0,value=None,inplace=True)
        Stock_prices_open.fillna(Stock_prices_close,inplace=True)
        Stock_prices_close[name].fillna(method='ffill',inplace=True)
        Stock_prices_close[name].fillna(method='bfill',inplace=True)
        Stock_prices_open[name].fillna(method='ffill',inplace=True)
        Stock_prices_open[name].fillna(method='bfill',inplace=True)
    FileClose='D://Doktorat Marek//dane//Notowania//Stock_price_close.csv'
    FileOpen='D://Doktorat Marek//dane//Notowania//Stock_price_open.csv'
    Stock_prices_close.to_csv(FileClose,encoding='UTF-8')
    Stock_prices_open.to_csv(FileOpen,encoding='UTF-8')
    return 0



def Generating_stock_price_table_quarterly():
    """
    The function generates and returns a combined table with names of stocks
    in columns and quarter start dates in indexes. Profit tables for individual
    stocks are taken from stock_prices function.
    Stock prices are not filled in for the missing values, file is used in MCap calculations
    Stock prices are resampled for beggining of quarter
    There are verions Open or Close
    """
    #Getting Names list
    Profitfile='pap//CombProfit.csv'
    path='D://Doktorat Marek//dane//'
    ProfitsFilePath=path+Profitfile
    quarterly_profit=pd.read_csv(ProfitsFilePath,index_col=0,header=0,parse_dates=True)
    Names_list=quarterly_profit.columns.tolist()
    
    Stock_prices_close=pd.DataFrame(index=pd.date_range('19980101','20171201',freq='QS-JAN'),columns=Names_list)
    Stock_prices_open=pd.DataFrame(index=pd.date_range('19980101','20171201',freq='QS-JAN'),columns=Names_list)
    for name in Names_list:
        Stock_prices_close[name]=stock_prices(name)['Close']
        Stock_prices_open[name]=stock_prices(name)['Open']
        Stock_prices_close[name].replace(to_replace=0,value=None,inplace=True)
        Stock_prices_open[name].replace(to_replace=0,value=None,inplace=True)

    FileClose='D://Doktorat Marek//dane//Notowania//QStock_price_close.csv'
    FileOpen='D://Doktorat Marek//dane//Notowania//QStock_price_open.csv'
    Stock_prices_close.to_csv(FileClose,encoding='UTF-8')
    Stock_prices_open.to_csv(FileOpen,encoding='UTF-8')
    return 0

def PeriodReturnTable(Dates_profit,period):
    '''
    Dates_profit - DataFrame object read from file ProfitDates.csv, includes 
    set of announcement dates for companies - period in days
    creates a file 'ReturnsTablePeriod+period+.csv which includes stock return for period 
    starting at the announcement date for all companies and quarters that exist in Dates_profit
    returns 1 if succesful
    
    '''
    print("\n\nCreating Returns Table\n")
    portfolioReturns=pd.DataFrame(index=Dates_profit.index,columns=Dates_profit.columns)
    for stock in Dates_profit.columns:
        stock_data=stock_prices(stock)
        for date in Dates_profit.index:
            try:
                DateinStockDataStart=stock_data.index.get_loc(date,method='pad')
                StartDate=stock_data.index[DateinStockDataStart]
                portfolioReturns[stock].loc[date]=stock_return_period(stock,stock_data, StartDate,period)
            except:
                portfolioReturns[stock].loc[date]=None
    FileNameTable='D://Doktorat Marek//dane//returns//ReturnsTablePeriod'+str(period)+'.csv'
    portfolioReturns.to_csv(FileNameTable,encoding='UTF-8')
    return 0

def OmegaPricesTable():
    """
    Creating a single file with stockreturns from omegacgle files for all companies in CombProfit
    Files AllOpen and AllClose created
    """            
    import os
    omega_wse=[]
    L=os.listdir("D://Doktorat Marek//dane//Notowania//omegacgl")
    for line in L:
       name=line.replace(".txt","")
       omega_wse.append(name)
    Stock_Prices=pd.DataFrame(index=pd.date_range('19980101','20171201'),columns=omega_wse)
    for stock in omega_wse:
        FileName="D://Doktorat Marek//dane//Notowania//omegacgl//"+str(stock)+".txt"
        stock_data=pd.read_csv(FileName,header=0,index_col='Date',encoding ="UTF-8",parse_dates=True,dayfirst=True)
        Stock_Prices[stock]=stock_data['Open']
    FileName2="D://Doktorat Marek//dane//Notowania//AllOpen.txt"
    Stock_Prices.to_csv(FileName2,encoding='UTF-8')
        
    
    

#for period in range(-60,61):
#    PeriodReturnTable(Dates_profit,period)


            