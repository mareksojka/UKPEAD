# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 21:39:35 2018

@author: marek
"""
import pandas as pd


QStock_prices_close=pd.read_csv('D://Doktorat Marek//dane//Notowania//QStock_price_close.csv',parse_dates=True,encoding='UTF-8',index_col=0,header=0,dtype='float')
QStock_prices_close.drop(QStock_prices_close.iloc[79].name,inplace=True)
files='D://Doktorat Marek//dane//pap//CombNoshares.csv'
Comb_Noshares=pd.read_csv(files,index_col=0,header=0,parse_dates=True)


MCap=Comb_Noshares*QStock_prices_close
MCapA=MCap.resample('AS').first()
Mask=MCapA[MCapA.rank(axis=1,ascending=False)<=100]
Mask[MCapA.rank(axis=1,ascending=False)<=100]=1
Mask=Mask.resample('QS-JAN').ffill()
Mask.loc[pd.Timestamp('20170401')]=Mask.iloc[76]
Mask.loc[pd.Timestamp('20170701')]=Mask.iloc[76]
