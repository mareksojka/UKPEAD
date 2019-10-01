# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 09:38:39 2017

@author: marek
"""
import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import json
import re
os.chdir('D:\\Quant\\CS50\\Project\\Project')

def ReportsScraping(start_year=2004,end_year=2020):
    '''
    Reads list of url to scrap from file termReports2004.json or termReports2004corected.json
    Takes basic info from list of lists (list of dicts in corected file) 
    loads site tries two times
    makes soup
    loopup for tr nTekst
    takes all rows from 2 to lenght-1 and appends to list
    saves to disk as file Reports2004corected.json
    '''
    current_dir = os.getcwd()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
    years=range(start_year,end_year)
    for year in years:
        pap_data = []
        json_name = current_dir + '\\data\\PAP\\termReports' + str(year) + '.json'
        #json_name='D://Doktorat Marek//dane//pap//termReports'+str(year)+'corected.json'
        with open(json_name, 'r') as fp:
            links_list=json.load(fp)
    
        for counter,link in enumerate(links_list):
            pap_data.append({})
            #link=list(link.values()) #only for corrected json file
            pap_data[counter]['report_date'] = link['date']
            pap_data[counter]['report_time'] = link['time']
            pap_data[counter]['report_stock_name'] = link['name']
            pap_data[counter]['report_type'] = link['report_type']
            pap_data[counter]['report_name'] = link['report_name']
            pap_data[counter]['report_url'] = link['report_url']
            url=link['report_url']
            print('\nscrapping ',url)
            try:
                try:
                    req = urllib.request.Request(url, headers={'User-Agent':user_agent})
                    html = urllib.request.urlopen(req).read().decode('utf-8')
                except (urllib.error.URLError, urllib.error.HTTPError) as e:
                    print('error scraping:' + url +' stopped for 2 seconds')
                    time.sleep(2)
                    req = urllib.request.Request(url, headers={'User-Agent':user_agent})
                    html = urllib.request.urlopen(req).read().decode('utf-8')
            # giving html to Beautifulsoup constructor
                soup = BeautifulSoup(html, 'html.parser')
                print('found '+ str(soup.title) + ' in ' + link['name'] + ' ' + link['report_type'] + ' at ' + link['date'])
                #scraping data from page soup
                #scraping frame with report title data
                table = soup.find_all("a",string=("STRONA TYTUŁOWA"))[-1].find_parent().next_sibling.next_sibling
                nTekst=table.find_all('tr','nTekst')
                if year>2004:
                    line_title = 'report_period1'
                    try:
                        line_data=int(nTekst[2].find_all('td')[4].string)
                    except: 
                        try:
                            line_data=int(nTekst[3].find_all('td')[4].string)
                        except:
                            line_data=None
                    pap_data[counter][line_title]=line_data
                    line_title='report_period2'
                    try:
                        line_data=int(nTekst[2].find_all(string=re.compile("\d\d\d\d"))[0].strip())
                    except:
                        try:
                            line_data=int(nTekst[3].find_all(string=re.compile("\d\d\d\d"))[0].strip())
                        except:
                            line_data=None
                    pap_data[counter][line_title]=line_data
                else:
                    line_title='report_period1'
                    try:
                        line_data=int(nTekst[2].find_all('td')[2].string)
                    except:
                        line_data=None
                    pap_data[counter][line_title]=line_data
                    line_title='report_period2'
                    try:
                        line_data=int(nTekst[2].find_all('td')[4].string)
                    except:
                        line_data=None
                    pap_data[counter][line_title]=line_data
            
                line_title='accounting_period'
                try:
                    line_data=table.find_all(string=re.compile("od.*\d\d\d\d-\d\d-\d\d.*do.*"))[0]
                except:
                    line_data=None
                pap_data[counter][line_title]=line_data
    
                
                # Scrapping financial report contents
                try:
                    table=soup.find_all("a",string=("WYBRANE DANE FINANSOWE"))[-1].find_parent().next_sibling.next_sibling
                    nTekst=table.find_all('tr','nTekst')
                    line_title='units'
                    try:
                        line_data0=nTekst[0].find_all('td')[2].string.strip()
                        if line_data0=='\n' or line_data0=='':
                            line_data0=nTekst[1].find_all('td')[2].string.strip()   
                    except:
                        line_data0=None
                    pap_data[counter][line_title]=line_data0   
                    line_title='period'
                    try:
                        line_data=nTekst[1].find_all('td')[1].string.strip()
                        if line_data0=='\n' or line_data0=='':
                           line_data=nTekst[2].find_all('td')[1].string.strip()
                    except:
                        line_data=None
                    pap_data[counter][line_title]=line_data                
                    for r in range(2,len(nTekst)-1):
                        line_title=None
                        try:
                            line_title=nTekst[r].find_all('td')[1].string.strip()
                        except:
                            line_title=None            
                        try:
                            line_string=nTekst[r].find_all('td')[2].string.replace(' ','')
                        except:
                            line_string=None
                        line_data=''
                        try:
                            for number in line_string:
                                if number in'0123456789-':
                                    line_data=line_data+number
                                elif number==',':
                                    line_data=line_data+'.'
                            line_data=float(line_data)
                            pap_data[counter][line_title]=line_data
                        except:
                            try:
                                line_string=nTekst[r].find_all('td')[4].string.replace(' ','')
                                line_data=''
                                for number in line_string:
                                    if number in'0123456789-':
                                        line_data=line_data+number
                                    elif number==',':
                                        line_data=line_data+'.'
                                line_data=float(line_data)
                                pap_data[counter][line_title]=line_data
                            except:
                                line_data=None
                        if line_title!=None and line_data!=None:
                            pap_data[counter][line_title]=line_data
                except:
                    pass
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                pass
        
        
        
        # delays for 0.2 second
        #    time.sleep(0.2)
        
        links_json_file = current_dir + '\\data\\PAP\\Reports'+str(year)+'.json'
        with open(links_json_file, 'w') as fp:
            json.dump(pap_data,fp)
    return 0

def emptyrecords():
    '''
    Function finds empty records in file Reports2004.json
    that is dict that are shorter then 7, which is the length of the header
    List of dicts is saved to termReports2004corected.json
    '''
    links_list=[]
    years=range(2004,2018)
    for year in years:
        links_list=[]
        filename='D://Doktorat Marek//dane//pap//Reports'+str(year)+'.json'
        with open(filename,'r') as papfile:
            papfile=json.load(papfile)
    
    
        for r in range(len(papfile)):
            if len(papfile[r])<7:
                links_list.append(papfile[r])
        json_file='D://Doktorat Marek//dane//pap//termReports'+str(year)+'corected.json'
        with open(json_file, 'w') as fp:
            json.dump(links_list,fp)
    return links_list

def filesmerging():
    '''
    Function read files Reports2004.json and Reports2004corected.json
    and merges them based on key 'url'
    saves to file Reports2004merged.json
    Runs a loop for years 2004 to 2017
    '''
    years=range(2004,2018)
    for year in years:
        
        filename='D://Doktorat Marek//dane//pap//Reports'+str(year)+'.json'
        with open(filename,'r') as pf:
            papfile=json.load(pf)
       
        
        filenamecorected='D://Doktorat Marek//dane//pap//Reports'+str(year)+'corected.json'
        with open(filenamecorected,'r') as cpf:
            papfile_corected=json.load(cpf)
    
        for papdict in papfile:
            for papcor in papfile_corected:
                if papdict['url']==papcor['url']:
                    papdict.update(papcor)
        
        json_file='D://Doktorat Marek//dane//pap//Reports'+str(year)+'merged.json'
        with open(json_file, 'w') as fp:
            json.dump(papfile,fp)

#    with open('D://Doktorat Marek//dane//termReports.txt', 'r') as fp:
#        link1_list=fp.read().splitlines()
#for link in link1_list:
#    link2_list.append(link.replace('[','').replace(']','').replace("'","").split(','))