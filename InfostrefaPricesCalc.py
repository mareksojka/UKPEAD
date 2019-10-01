# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 12:00:05 2019

@author: marek
"""

import os
os.chdir('D://Doktorat Marek//dane')

import pandas as pd
import numpy as np


def stock_returns(Notoria_Stock_Name):
    '''
    input - Notoria_stock_Name is the name of company used in notoria database
    tries to open Infostrega file from disk,
    if does not exist, tries to open quandl file from disk
    if unsuccesful return empty DataFrame
    returns DataFrame object with date index and one column 'Return'
    which is daily return from GPW
    '''

    try:
        notorianames=pd.read_csv('D://Doktorat Marek//dane//Notoria Names data.csv',sep=',',encoding = "UTF-8",index_col='Name',header=0)
        ISIN=notorianames.loc[Notoria_Stock_Name,'ISIN']
        ExcelFile='D://Doktorat Marek//dane//notowania//Infostrefa//'+ISIN+'.xls'
        Excel=pd.read_excel(ExcelFile)
        Excel['Date']=pd.to_datetime(Excel['Data'])
        Excel.set_index('Date',inplace=True)
        stock_data=pd.DataFrame(index=Excel.index,columns=['Return'])
        stock_data['Return']=Excel['Zmiana']
        print("Using Infostrefa file for: ", Notoria_Stock_Name)
    except:
        
        try:
            FileName='D://Doktorat Marek//dane//notowania//quandl//'+Notoria_Stock_Name+'.csv'
            Quandl=pd.read_csv(FileName,header=0,index_col='Date',encoding ="UTF-8",parse_dates=True,dayfirst=True)
            stock_data=pd.DataFrame(index=Quandl.index,columns=['Return'])
            stock_data['Return']=Quandl['%Change']
            print("Using Quandl file for: ", Notoria_Stock_Name)
        except:
            print("No Quandl stock price data file for ",Notoria_Stock_Name)
            File='D://Doktorat Marek//dane//notowania//quandl//0EMPTY.csv'
            empty=pd.read_csv(File,header=0,index_col='Date',encoding ="UTF-8",parse_dates=True,dayfirst=True)
            stock_data=pd.DataFrame(index=empty.index,columns=['Return'])
    return stock_data

def Generating_stock_daily_return_table():
    """
    The function generates and returns a combined table with names of stocks
    in columns and dates in indexes. Profit tables for individual
    stocks are taken from stock_retrunrs function.
    """
    #Getting Names list
    Profitfile='pap//CombProfit.csv'
    path='D://Doktorat Marek//dane//'
    ProfitsFilePath=path+Profitfile
    quarterly_profit=pd.read_csv(ProfitsFilePath,index_col=0,header=0,parse_dates=True)
    Names_list=quarterly_profit.columns.tolist()
    
    Stock_returns=pd.DataFrame(index=pd.date_range('19980101','20180918',freq='D'),columns=Names_list)
    for name in Names_list:
        Stock_returns[name]=1+stock_returns(name)['Return']/100
        Stock_returns[name].fillna(1,inplace=True)
    
    WIG=pd.read_excel('D://Doktorat Marek//dane//notowania//Infostrefa//PL9999999995.xls')
    WIG['Date']=pd.to_datetime(WIG['Data'])
    WIG.set_index('Date',inplace=True)
    Stock_returns['WIG'] = 1+WIG['Zmiana']/100
    Stock_returns['WIG'].fillna(1,inplace=True)
    Stock_returns['Average']=Stock_returns.mean(1)
    
    FileReturns='D://Doktorat Marek//dane//Notowania//Stock_returns.csv'
    Stock_returns.to_csv(FileReturns,encoding='UTF-8')
    return 0