# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 08:15:03 2017

@author: marek
"""
# %%
import os
import json
import datetime
import pandas as pd
import numpy as np
from pandas.tseries.offsets import QuarterBegin

os.chdir('D:\\Quant\\CS50\\Project\\Project')
#%%

#filename='D://Doktorat Marek//dane//pap//Reports2.csv'
#dtypes={'report_period1':np.float64,'report_period2':np.float64,'Profit':np.float64,'NoShares':np.float64,'consolidated':np.bool}
#pap_data=pd.read_csv(filename,parse_dates=['Datetime','start_date','end_date'],sep=',',index_col=0,header=0,dtype=dtypes)
#pap_data['Datetime']=pd.to_datetime(pap_data['Datetime'], format='%Y-%m-%d %H:%M:%S')

#Quant Research File
#quantrfile='D://Doktorat Marek//dane//caig_company (GPW).csv'
#quant_data=pd.read_csv(quantrfile,parse_dates=True,sep=',',names=['Name','Profit','Date'])

#%%

def creating_year_csv_file(start_year=2004,end_year=2020):
    '''
    Reading json year files
    Extracting information from files to find Profit and No of Shares
    Copying known fields
    Saving in csv file format
    '''
    current_dir = os.getcwd()
    years=range(start_year,end_year)
    for year in years:
        
        filename = current_dir + '\\data\\PAP\\Reports'+str(year)+'.json'
        with open(filename, 'r') as pf:
            papfile=json.load(pf)
        pap_df=pd.DataFrame(papfile)
        
    
        pap_df['Datetime'] = pd.to_datetime(pap_df['report_date'] + ' ' +
              pap_df['report_time'], format='%Y.%m.%d %H:%M')    
        # Extacting information found in many columns to Profit column and NoShares column
        profit_list = []
        share_list = []
        sales_list = []
        for column in pap_df.columns:
            if ('zysk' in column.lower() or 'wynik' in column.lower() or
                'strata' in column.lower() or 'dochody' in column.lower() or
                'profit' in column.lower()) and \
                ('netto' in column.lower() or 'po opodatkow' in column.lower() or 
                'okres' in column.lower() or 'ogółem' in column.lower() or 
                'za rok' in column.lower() or ' roku obrotowego' in column.lower() or
                'net' in column.lower()) and \
                 ('mniejsz' not in column.lower() and
                  'zanualiz' not in column.lower() and 'działalno' not in column.lower() and
                  '-' not in column.lower() and '*' not in column.lower() and
                  '[' not in column.lower() and 'sprawozdan' not in column.lower() and
                  'z inwestycji' not in column.lower() and 'ze sprzedaży' not in column.lower() and
                  'operacyjny' not in column.lower() and 'przed' not in column.lower() and 
                  'udział' not in column.lower() and 'kontroli' not in column.lower() and
                  'akcję' not in column.lower() and 'akcje' not in column.lower() and 
                  'jedną' not in column.lower() and 'pozosta' not in column.lower() and
                  'from' not in column.lower() and 'per' not in column.lower()):
                profit_list.append(column)
            elif ('netto z działalności kontynuowanej' in column.lower() and
                  'zysk' in column.lower()) and 'akcję' not in column.lower():
                profit_list.append(column)
            elif ('netto na działalności kontynuowanej' in column.lower() and
                  'zysk' in column.lower()) and 'akcję' not in column.lower():
                profit_list.append(column)
            elif 'Całkowite dochody ogółem' in column.lower():
                profit_list.append(column)
            elif 'Zysk/ strata z działalności kontynuowanej' in column.lower():
                profit_list.append(column)
            elif 'Net profit for the period reported' in column.lower():
                profit_list.append(column)
            elif (('liczba' in column.lower() or 'number' in column.lower()) and
                ('akcji' in column.lower() or 'shares' in column.lower())):
                share_list.append(column)
            elif ('przych' in column.lower() or 'sales' in column.lower()):
                sales_list.append(column)

        pap_df['Profit'] = pap_df[profit_list[0]]
        for column in profit_list[1:]:
            pap_df['Profit'].fillna(pap_df[column], inplace=True)
#        for column in pap_df.columns:
#            if ('liczba' in column.lower() or 'number' in column.lower()) and \
#                ('akcji' in column.lower() or 'shares' in column.lower()):
#                share_list.append(column)
        pap_df['NoShares'] = pap_df[share_list[0]]
        for column in share_list[1:]:
            pap_df['NoShares'].fillna(pap_df[column],inplace=True)
        pap_df['Sales'] = pap_df[sales_list[0]]
        for column in sales_list[1:]:
            pap_df['Sales'].fillna(pap_df[column],inplace=True)
        
        fields_list = ['Datetime', 'report_stock_name', 'Profit', 'Sales',
                       'units', 'NoShares', 'report_type', 'accounting_period',
                       'report_period1', 'report_period2', 'period','report_url']     
        financial_data = pap_df[fields_list]
        csvname = current_dir + '\\data\\PAP\\Reports'+str(year)+'.csv'
        financial_data.to_csv(csvname,sep=',',encoding ='UTF-8')
    return 0
    
def merging_year_csv_files():
    '''
    loads files Reports2004.csv for every year and using pandas.append 
    links them to a single list
    '''
    current_dir = os.getcwd()
    firstcsvname = current_dir + '\\data\\PAP\\Reports2004.csv'
    pap_reports = pd.read_csv(firstcsvname, parse_dates=True, sep=',',
                              encoding ='UTF-8', index_col=0, header=0)
    years = range(2005,datetime.datetime.now().year+1)
    for year in years:
        csvname = current_dir + '\\data\\PAP\\Reports' + str(year) + '.csv'
        pap_report = pd.read_csv(csvname, parse_dates=True, sep=',',
                                 encoding ='UTF-8', index_col=0, header=0)
        pap_reports = pap_reports.append(pap_report,ignore_index=True, sort=False)
    csvname = current_dir + '\\data\\PAP\\Reports.csv'
    pap_reports.to_csv(csvname, sep=',', encoding ='UTF-8')
    return 0
    
def Reports_csv_cleaning():
    """
    Reading Reports.csv
    Cleaning names list
    Adding Names column with name based on notoria names list
    """
    current_dir = os.getcwd()
    filename = current_dir + '\\data\\pap\\Reports.csv'
    pap_data = pd.read_csv(filename, parse_dates=True, sep=',', index_col=0, header=0)
    #change name from XXStara spolka to Getin Noble Bank
    Xs = pap_data.index[pap_data['report_stock_name'] == 'XXStara spółka - Getin Noble Bank SA']
    pap_data.loc[Xs, 'report_stock_name'] = 'Getin Noble Bank SA'
    #finding names of stocks in pap database sorting alphabetically
    names_list = list(pap_data['report_stock_name'].unique())
    names_list.sort()
    #creating dictionary to translate pap name to notoria name
    names_dict = {key:None for key in names_list}
    #reading Notoria names data
    Notoriafile = current_dir + '\\data\\Notoria Names data.csv'
    Notoriadata = pd.read_csv(Notoriafile, parse_dates=True, sep=',',
                              index_col=0, header=0)
    #Creating dict key=pap name and value= notoria name
    for key in names_list:
        if key.lower() in list(Notoriadata['Stock Name'].str.lower()):
            names_dict[key] = Notoriadata.index[Notoriadata['Stock Name'].str.lower() == key.lower()][0]
    # Checking for stock names found in pap not in Notoria database
    notinnotoria = []
    for key in names_dict.keys():
        if names_dict[key] == None:
            notinnotoria.append(key)
    # only company not in notoria worth looking at
    # notinnotoria.remove('Multimedia Polska SA')
    

    # creating new column Name with notoria name first droping rows with names
    # that are not in notoria database
    pap_data = pap_data[~pap_data['report_stock_name'].isin(notinnotoria)]
    for stock in names_dict.keys():
            IndList = list(pap_data.index[pap_data['report_stock_name'] == stock])
            pap_data.loc[IndList,'Name'] = names_dict[stock]
    
    #Flagging consolidated reports
    annual_reports = ['SA-R','SA-RS','SAB-RS','SAB-R','SAF-R','SAU-R','RS','SAU-RS','R','SAF-RS']
    annualS_reports = ['SA-RS','SAB-RS','RS','SAU-RS','SAF-RS']
    semi_reports = ['SA-P','SA-PS','PSr','P','PS', 'SA-PSr', 'SAU-P', 'SAB-P', 'SAU-PSr', 'SAF-P', 'SAF-PS','SAF-PSr']
    semiS_reports = ['SA-PS','PSr','PS','SA-PSr','SAU-PSr','SAF-PS','SAF-PSr']
    q_reports = ['SAB-QSr','SA-QSr','SA-Q','SA-QS','SAF-Q','SAB-Q','SAB-QS','SAU-Q','SAU-QSr','SAU-QS','SAF-QSr','SAF-QS','QSr','Q','QS']
    qS_reports = ['SAB-QSr','SA-QSr','SA-QS','SAB-QS','SAU-QSr','SAU-QS','SAF-QSr','SAF-QS','QSr','QS']
    consolidated = annualS_reports + semiS_reports + qS_reports
    unit = annual_reports + semi_reports + q_reports
    for x in consolidated:
        unit.remove(x)
    pap_data['consolidated'] = False
    pap_data.loc[pap_data['report_type'].isin(consolidated),'consolidated'] = True
    # Based on field accounging_period creating starting and ending reports date
    pap_data['start_date'] = pap_data['accounting_period'].str.strip().str.split().str.get(1)
    pap_data.loc[~pap_data['start_date'].str.split('-').
                 str.get(0).str.startswith("2", na=False), 'start_date'] = None
    pap_data['end_date'] = pap_data['accounting_period'].str.strip().str.split().str.get(3)
    pap_data.loc[~pap_data['end_date'].str.split('-').str.get(0).str.startswith("2", na=False), 'end_date'] = None
    #pap_data.drop('accounting_period',axis=1,inplace=True)  
    # correcting mistyped values
    pap_data.loc[pap_data['start_date'] == '20010-01-01',['start_date']] = '2010-01-01'
    pap_data.loc[pap_data['start_date'] == '20011-01-01',['start_date']] = '2011-01-01'
    pap_data.loc[pap_data['end_date'] == '20010-06-30',['end_date']] = '2010-06-30'
    pap_data.loc[pap_data['end_date'] == '20011-06-30',['end_date']] = '2011-06-30'
    pap_data.loc[pap_data['end_date'] == '20015-03-31',['end_date']] = '2015-03-31'
    # Getting start period and end period drom period column
    pap_data['period_start'] = pap_data['period'].str.strip().str.split().str.get(7)
    pap_data['period_end'] = pap_data['period'].str.strip().str.split().str.get(9)
    #pap_data.drop('period',axis=1,inplace=True)
    # Filling missing data with None, cleaning rubish from columns
    pap_data.loc[~pap_data['period_start'].str.startswith("20").fillna(False),['period_start']] = None
    pap_data.loc[~pap_data['period_end'].str.startswith("20").fillna(False),['period_end']] = None
    #filling empty values in start_date and end_date with values from period_start and period_end
    pap_data.loc[pap_data['start_date'].isnull(),['start_date']]=pap_data['period_start']
    pap_data.loc[pap_data['end_date'].isnull(),['end_date']]=pap_data['period_end']
    # chaning dtype to datetime
    pap_data['start_date']=pd.to_datetime(pap_data['start_date'], format='%Y-%m-%d')
    pap_data['end_date']=pd.to_datetime(pap_data['end_date'], format='%Y-%m-%d')    
    # Fields report_period1 contains quarter number for q reports and year for R and P reports
    # Copyting year from report_period1 to report_period2 and 
    # deleting values which are not q from report_period1 and not year from report_period2
    pap_data.loc[pap_data['report_period2'].isnull(),['report_period2']]=pap_data['report_period1']
    pap_data.loc[pap_data['report_period1']>4,['report_period1']]=None
    pap_data.loc[pap_data['report_period2']<2000,['report_period2']]=None
    pap_data.loc[pap_data['report_period2']>2100,['report_period2']]=None
    # Filling report_period1 based on report_type 4 for annual reports and 2 for semiannual reports
    pap_data.loc[pap_data['report_type'].isin(annual_reports),'report_period_interim_based_on_report_type']=4
    pap_data.loc[pap_data['report_type'].isin(semi_reports),'report_period_interim_based_on_report_type']=2
    pap_data['report_period1'].fillna(pap_data['report_period_interim_based_on_report_type'],inplace=True)
    pap_data.drop('report_period_interim_based_on_report_type',axis=1,inplace=True)
    # Filling missing data in report_period2 with year from period column
    pap_data.loc[pap_data['report_type'].isin(annual_reports),'report_period_interim_year']=pap_data['period'].str.strip().str.split().str.get(0)
    pap_data.loc[pap_data['report_type'].isin(semi_reports),'report_period_interim_year']=pap_data['period'].str.strip().str.split().str.get(2)  
    pap_data['report_period2'].fillna(pap_data['start_date'].dt.year,inplace=True)
    pap_data.drop('report_period_interim_year',axis=1,inplace=True)
    #Filling report_period1 for missing quarterly reports based on period column
    pap_data['rp1']=pap_data['period'].str.strip().str.split().str.get(0)
    pap_data.loc[~pap_data['rp1'].isin([1,2,3,4,5,6,'1','2','3','4','5','6']),'rp1']=None
    pap_data['report_period1'].fillna(pd.to_numeric(pap_data['rp1']),inplace=True)
    pap_data.drop('rp1',axis=1,inplace=True)
    # Filling missing start_date and end_date with value from report_period 1 and 2 columns
    pap_data['month_helper']=((pap_data['report_period1']*3)%13)
    pap_data['start_helper']=pd.to_datetime(pap_data['report_period2'].astype('str').str.split('.').str.get(0)+'01'+'01',errors='coerce',yearfirst=True,format='%Y%m%d')
    pap_data['end_helper']=pd.to_datetime(pap_data['report_period2'].astype('str').str.split('.').str.get(0)+pap_data['month_helper'].astype('str').str.split('.').str.get(0)+'30',errors='coerce',yearfirst=True,format='%Y%m%d')
    pap_data['start_date'].fillna(pap_data['start_helper'],inplace=True)
    pap_data['end_date'].fillna(pap_data['end_helper'],inplace=True)
    pap_data.drop(['month_helper','start_helper','end_helper'],axis=1,inplace=True)
    # changing units to int number based on units column
    pap_data['units2']=1
    #Blad w PZU i ASSECO
    pap_data.loc[[28854,29380,29852,17067,20357,22215],'units']='w mln.'
    #Blad w PGNIG
    pap_data.loc[[29754,20897,20898,27594,26460],'units']='w mln.'
    #Blad w PKNORLEN
    pap_data.loc[[23013,23767,25372,26093,26094,26143,26774],'units']='w mln.'
    #Blad w KGHM
    pap_data.loc[[21361,21362,21720,22710,23288,23290,23995,25060,25676,
                  25679,26515,26863,27374,27943,27945,28638,29186,29632,29689,
                  29785],'units']='w mln.'
    #Blad w PGE
    pap_data.loc[[22235,22744,23057,23058,23968,24741,24996,25406,25408,27348,
                  27855,27856,29154,29655],'units']='w mld.'
    #Blad w 11BIT,BSK
    pap_data.loc[[29871,25513,29138,29647],'units']='w zl'             
    #Preparing units2
    pap_data.loc[pap_data['units']=='w zl','units2']=1
    pap_data.loc[pap_data['units']=='w tys.','units2']=1000
    pap_data.loc[pap_data['units']==' w tys. zł','units2']=1000
    pap_data.loc[pap_data['units']=='  w tys. zł','units2']=1000
    pap_data.loc[pap_data['units']=='w 10 tys.','units2']=10000
    pap_data.loc[pap_data['units']=='w mln.','units2']=1000000
    pap_data.loc[pap_data['units']=='w mld.','units2']=1000000000
    # Resampling Profit field by column units2
    pap_data['Profit_t']=pap_data['Profit']*pap_data['units2']/1000
    # Flagging quarter period of the report
    
    #saving cleaned file to Reports2
    repots_clean_filename = current_dir + '\\data\\pap\\Reports2.csv'
    pap_data.to_csv(repots_clean_filename, sep=',', encoding ='UTF-8')
    return 0


#List of stock's names in DataFrane created using merging_csv_files
#stocks_names_list=list(pap_reports['report_stock_name'].unique())



def Selecting_reports():
    """
    From reports in pap_data select reports
    so that consolidated are left where both conso and unit are available
    only first report for period is left where multiple announcements found
    """
    current_dir = os.getcwd()
    file2 = current_dir + '\\data\\pap\\Reports2.csv'
    dtypes = {'report_period1':np.float64, 'report_period2':np.float64,
              'Profit':np.float64, 'NoShares':np.float64, 'consolidated':np.bool}
    pap_data = pd.read_csv(file2, parse_dates=['Datetime','start_date','end_date'],
                           sep=',', index_col=0, header=0, dtype=dtypes)
    # Reports definitions
    annual_reports=['SA-R','SA-RS','SAB-RS','SAB-R','SAF-R','SAU-R','RS','SAU-RS','R','SAF-RS']
    annualS_reports=['SA-RS','SAB-RS','RS','SAU-RS','SAF-RS']
    semi_reports=['SA-P','SA-PS','PSr','P','PS', 'SA-PSr', 'SAU-P',
                  'SAB-P', 'SAU-PSr', 'SAF-P', 'SAF-PS','SAF-PSr']
    semiS_reports=['SA-PS','PSr','PS','SA-PSr','SAU-PSr','SAF-PS','SAF-PSr']
    q_reports=['SAB-QSr','SA-QSr','SA-Q','SA-QS','SAF-Q','SAB-Q','SAB-QS',
               'SAU-Q','SAU-QSr','SAU-QS','SAF-QSr','SAF-QS','QSr','Q','QS']
    qS_reports=['SAB-QSr','SA-QSr','SA-QS','SAB-QS','SAU-QSr','SAU-QS',
                'SAF-QSr','SAF-QS','QSr','QS']
    consolidated = annualS_reports + semiS_reports + qS_reports
    unit = annual_reports + semi_reports + q_reports
    for x in consolidated:
        unit.remove(x)
    # Removing R and P reports for years 2005-2008, they were late and only copied info from previously announced Q reports
    annual_reports_index_list = list(pap_data[(pap_data['report_period2'].isin([2004,2005,2006,2007,2008]))&
                                     (pap_data['report_type'].isin(annual_reports))].index)
    semi_reports_index_list = list(pap_data[(pap_data['report_period2'].isin([2004,2005,2006,2007,2008]))&
                                            (pap_data['report_type'].isin(semi_reports))].index)
    pap_data.drop(annual_reports_index_list,axis=0,inplace=True)
    pap_data.drop(semi_reports_index_list,axis=0,inplace=True)
    # Drop unit reports where consolidated available
    for stock in list(pap_data['Name'].unique()):
        stocks_reports=pap_data[pap_data['Name']==stock]
        for year in list(stocks_reports['report_period2'].unique()):
            years_reports=pap_data.loc[(pap_data['Name']==stock)&(pap_data['report_period2']==year)]
            if len(years_reports) > 4:
                if len(years_reports.consolidated.unique()) > 1:
                    list_of_unit_reports_index = list(years_reports[years_reports['consolidated'] == False].index)
                    pap_data.drop(list_of_unit_reports_index,axis=0,inplace=True)
                    years_reports = pap_data.loc[(pap_data['Name'] == stock) & (
                                    pap_data['report_period2'] == year)]
            #Drop reports where more then two in a quarter available, leave the earliest announced        
            for quarter in pap_data.loc[(pap_data['Name'] == stock) & (
                            pap_data['report_period2'] == year), 'report_period1'].unique():
                quarter_reports = pap_data.loc[(pap_data['Name'] == stock) & (
                                    pap_data['report_period2'] == year) & (
                                    pap_data['report_period1'] == quarter)]
                if len(quarter_reports) > 1:
                    list_of_report_index = list(quarter_reports.index)
                    first_announced_index = int(quarter_reports[
                            quarter_reports.Datetime == quarter_reports.Datetime.min()].index[0])
                    list_of_report_index.remove(first_announced_index)
                    pap_data.drop(list_of_report_index, axis=0, inplace=True)
        # Droping reports with less then 5 reports in the data set
        stocks_reports = pap_data[pap_data['Name'] == stock]
        if len(stocks_reports) < 6:
            stocks_reports_index = list(stocks_reports.index)
            pap_data.drop(stocks_reports_index, axis=0, inplace=True)

    """
    Unrolling_profit
    All announced earnings are rolling quarter
    To unroll earnings subtract previous quarterly profit from current profit
    apart from first quarter
    """    
    pap_data.loc[pap_data['report_period1'] == 1, 'Profit_Q'] = pap_data['Profit_t']
    for stock in list(pap_data.Name.unique()):
        stocks_reports = pap_data[pap_data['Name'] == stock]
        pap_data.loc[pap_data['Name'] == stock, 'Profit_helper'] = stocks_reports[
                'Profit_t'] - stocks_reports['Profit_t'].shift(1)
        pap_data.loc[(pap_data['Name'] == stock) &
                     (pap_data['report_period1'].isin([2,3,4,5,6])),
                     'Profit_Q'] = pap_data['Profit_helper']
    pap_data.drop('Profit_helper', axis=1, inplace=True)
    pap_data['Q_start_date'] = [date-QuarterBegin(startingMonth=1) for date in pap_data['end_date']]
    pap_data.loc[pap_data['Q_start_date'] < '20000101','Q_start_date'] = None
    pap_data.loc[pap_data['Q_start_date'] > '20190401','Q_start_date'] = None
    pap_data['aprox_date'] = pap_data['Datetime'].dt.date-QuarterBegin(n=2, startingMonth=1)
    pap_data['Q_start_date'].fillna(pap_data['aprox_date'], inplace=True)


    """
    Creating_profits_DataFrame(pap_data):
    Based on data in pap_data creating DataFrames with quarter start date and stock name as indexes
    Seperate Df is created for every value: Profit, Publication date, NoShares
    """
    RowIndex = pd.date_range(start='19971231',end='20190401', freq='Q') + pd.Timedelta(1,unit='d')
    ColumnIndex = list(pap_data.Name.sort_values().unique())
    Profit_df = pd.DataFrame(columns=ColumnIndex, index=RowIndex)
    Dates_df = pd.DataFrame(columns=ColumnIndex, index=RowIndex)
    Noshares_df = pd.DataFrame(columns=ColumnIndex, index=RowIndex)
    for stock in list(pap_data.Name.unique()):
        stocks_reports_index = pap_data.loc[pap_data['Name'] == stock].index
        for index in stocks_reports_index:
            Name = pap_data.loc[index, 'Name']
            Date_pub = pap_data.loc[index, 'Datetime']
            Profit = pap_data.loc[index, 'Profit_Q']
            NoShares = pap_data.loc[index, 'NoShares']
            QDate = pap_data.loc[index, 'Q_start_date']
            Profit_df.loc[QDate, Name] = Profit
            Dates_df.loc[QDate, Name] = Date_pub
            Noshares_df.loc[QDate, Name] = NoShares
    filep = current_dir + '\\data\\pap\\PAPProfit.csv'
    Profit_df.to_csv(filep, sep=',', encoding ='UTF-8')
    filed = current_dir + '\\data\\pap\\PAPDates.csv'
    Dates_df.to_csv(filed, sep=',', encoding ='UTF-8')
    files = current_dir + '\\data\\pap\\PAPNoshares.csv'
    Noshares_df.to_csv(files, sep=',', encoding ='UTF-8')
    return 0
            
def Filling_from_Notoria():
    """
    Filling missing data in file Profits.csv sourced from PAP with data
    from Notoria where suitable data available
    
    """
    current_dir = os.getcwd()
    #Loading Notoria files
    Notoria_Profit = pd.read_csv(current_dir + '\\data\\pap\\Profits.csv',
                                 index_col=0, header=0, parse_dates=True)
    Notoria_Dates = pd.read_csv(current_dir + '\\data\\pap\\ProfitDates.csv',
                                index_col=0, header=0, parse_dates=True)
    Notoria_NoShares = pd.read_csv(current_dir + '\\data\\pap\\NoShares.csv',
                                   index_col=0, header=0, parse_dates=True)
    #loading PAP data files
    filep = current_dir + '\\data\\pap\\PAPProfit.csv'
    filed = current_dir + '\\data\\pap\\PAPDates.csv'
    files = current_dir + '\\data\\pap\\PAPNoshares.csv'
    PAP_Profit = pd.read_csv(filep, index_col=0, header=0, parse_dates=True)
    PAP_Dates = pd.read_csv(filed, index_col=0, header=0, parse_dates=True)
    PAP_Noshares = pd.read_csv(files, index_col=0, header=0, parse_dates=True)
    # Combining data in files
    # Looking for stock names in PAP not in Notoria_names
    PAP_names = list(PAP_Profit.columns)
    Notoria_names = list(Notoria_Profit.columns)
    for name in PAP_names:
        if name not in Notoria_names:
            PAP_names.remove(name)
    New_stocks = Notoria_Profit.drop(PAP_names, axis=1)
    New_dates = Notoria_Dates.drop(PAP_names, axis=1)
    New_noshares = Notoria_NoShares.drop(PAP_names, axis=1)
    # Filling missing values in PAP data with data from Notoria files
    PAP_Profit.fillna(value=Notoria_Profit, inplace=True)
    PAP_Dates.fillna(value=Notoria_Dates, inplace=True)
    PAP_Noshares.fillna(method='bfill', inplace=True)
    PAP_Noshares.fillna(value=Notoria_NoShares, inplace=True)
    # Adding columns from Notoria to PAP
    Combined_Profit = PAP_Profit.join(New_stocks)
    Combined_Dates = PAP_Dates.join(New_dates)
    Combined_Noshares = PAP_Noshares.join(New_noshares)
    #Saving new files
    filep = current_dir + '\\data\\pap\\CombProfit.csv'
    Combined_Profit.to_csv(filep,sep=',',encoding ='UTF-8')
    filed = current_dir + '\\data\\pap\\CombDates.csv'
    Combined_Dates.to_csv(filed,sep=',',encoding ='UTF-8')
    files = current_dir + '\\data\\pap\\CombNoshares.csv'
    Combined_Noshares.to_csv(files,sep=',',encoding ='UTF-8')
    return 0
    
    
#%%
def Combined():
    current_dir = os.getcwd()
    filep = current_dir + '\\data\\pap\\CombProfit.csv'
    filed = current_dir + '\\data\\pap\\CombDates.csv'
    files = current_dir + '\\data\\pap\\CombNoshares.csv'
    Comb_Profit=pd.read_csv(filep,index_col=0,header=0,parse_dates=True)
    Comb_Dates=pd.read_csv(filed,index_col=0,header=0,parse_dates=True)
    Comb_Noshares=pd.read_csv(files,index_col=0,header=0,parse_dates=True)
    
#%%
def finding_net_profit_in_json_report(report):
    '''
    
    '''
    for title in report.keys():
        if 'zysk' in title.lower() and 'netto' in title.lower():
            print(report['report_stock_name'] + ' ' + title + ' ' + str(report[title]) + '\n')
            break
    return report[title]
    
