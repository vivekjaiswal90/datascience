import xlrd
import MySQLdb
from bs4 import BeautifulSoup as Soup
import requests
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
#import excelHelper
import time
#import dbHandler
import csv
import re
import random
from multiprocessing import Pool
from selenium.webdriver.common.action_chains import ActionChains
import urllib2

#The main Function
def GeneralInfo(name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email):
		try:
					con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='findthedta', use_unicode=True, charset="utf8")
					cur = con.cursor()
					cur.execute('INSERT INTO generalinfo(name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)) 
					con.commit()
					con.close()
		except Exception, e:
					print ("DB Connection error")


#The jack of all Calculations 
def foo(id,site_url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		url = "http://think-tanks.findthedata.org/l/112"
		response = opener.open(url)
		page = response.read()
		#from bs4 import BeautifulSoup
		soup = Soup(page)
		print soup
	except Exception,e:
		print("Connection Error")

i=0
if(i==0)
		site_url=http://think-tanks.findthedata.org/l/1
		i=i+1
else
	posturl=soup.find('div',{'class' :'content'})
	post_url=posturl.find('form')
	pourl=(post_url.get('action')).strip()		
	pre_url="http://think-tanks.findthedata.org"
	site_url=pre_url+post_url

foo(id,site_url)
GeneralInfo(name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)


if __name__ == '__main__':


    start_page = raw_input("Enter start index:")
    end_page = raw_input("Enter end index:")
    if int(end_page) < int(start_page):
    	end_page = raw_input("end page can't be less  that start index Enter again:")
    total_process = raw_input("total no. of parallel process you want:")
    total_page =  int(end_page) - int(start_page)
    each_slot =  int(float(total_page)/float(total_process))
    print "each slot:"+str(each_slot)

    counter  = 0
       
    pool = Pool(processes=int(total_process))
    #pool.map(crawl_page,(proxy,))
    #proc = []
    #sub_param = []
    param, params, final_params = [], [], []
    for i in range(int(total_process)):
    	params = []
        print "process no." + str(counter +1) + " started"
        #proxy['http'] = proxies[counter]
        start_index = int(start_page) + (int(each_slot)*i)
        #print (start_index)
        end_index = start_index + int(each_slot)
        #print (end_index)
        pre_url = "http://www.sec.gov"
        before_cik = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
        after_cik = "&type=8-k&dateb=&owner=exclude&count=100"
        book = xlrd.open_workbook('CIKs.xlsx')
        sheet = book.sheet_by_index(0)
        for h in range(start_index, end_index):
			param = []
			CIK = sheet.cell_value(h,0)
			CIK = int(CIK)
			CIK = str(CIK)
			#CIK='1059142'
			while len(CIK)<10:
				CIK="0"+CIK
			print CIK
			site_url = before_cik + CIK + after_cik
			print "running index: "+str(h+1)+" & CIK: "+str(CIK)
			#print site_url
			param.append(site_url)
			param.append(CIK)
			params.append(param)
        #print len(urls)
       	final_params.append(params)
    i= 0
    for y in final_params:
        i = i + 1
        pool.apply_async(foo1, args=(y, ))
        print ("process: "+ str(i))
         

    pool.close()
    pool.join()

