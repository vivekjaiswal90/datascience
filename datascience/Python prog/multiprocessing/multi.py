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
from mmap import mmap,ACCESS_READ
from xlrd import open_workbook

"""def GeneralInfo(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email):
		try:
					con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='findthedta', use_unicode=True, charset="utf8")
					ciur = con.cursor()
					cur.execute('INSERT INTO generalinfo(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)) 
					con.commit()
					con.close()
		except Exception, e:
					print ("DB Connection error")"""


def foo(ID,URL):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		url = URL
		response = opener.open(url)
		page = response.read()
		#from bs4 import BeautifulSoup
		soup = Soup(page)
		#print soup

		#Head = soup.find('head')

		"""Id = (Head.find('link'))#.encode('utf8', 'ignore').strip()
		id=(Id.get('href')).strip().split('/')[4]
		id=str(id)"""
		
		id=ID
		#print id

		Data=soup.findAll('td',{'class' :'fdata'})
		name=Data[0].text
		#print name

		Website_link=Data[1].find('a')
		website_link=(Website_link.get('href')).strip()
		#print website_link

		category=Data[2].text
		#print category

		active=Data[3].text
		#print active

		founders=Data[4].text
		#print founders

		current_director=Data[5].text
		#print current_director
	
		try:
			Board_of_directors_link=Data[6].find('a')
			board_of_directors_link=(Board_of_directors_link.get('href')).encode('utf8', 'ignore').strip()
			#print board_of_directors_link
		except	Exception,e:
			print "Board of directorerror"+str(e)
		
		politicalaffiliation=Data[7].text
		#print politicalaffiliation

		research=Data[8].text
		#print research

		mission=Data[9].text
		#print mission

		non_profit=Data[10].text
		#print non_profit

		funding=Data[11].text
		#print funding


		address=Data[25].text
		#print address

		phonenumber=Data[27].text
		#print phonenumber

		posturl=soup.find('div',{'class' :'content'})
		post_url=posturl.find('form')
		pourl=(post_url.get('action')).strip()
		#print pourl
		#pre_url="http://think-tanks.findthedata.org"
		#site_url=pre_url+pourl
		#print site_url
		
	except	Exception,e:
		print "Connection error"+str(e)
		id='void'
		name='void'
		board_of_directors_link='void'
		website_link='void'
		category='void'
		active='void'
		founders='void'
		current_director='void'
		board_of_directors_link='void'
		politicalaffiliation='void'
		research='void'
		mission='void'
		non_profit='void'
		funding='void'
		address='void'
		phonenumber='void'
		faxnumber='void'
		email='void'
	
	
	
	
		#GeneralInfo(id,name,website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)
	
	
	
def foo1 (y):
	print len(y)
	for t in y:
		try:
			Id = t[1]
			url = t[0]
			foo(Id,url)
			print "Done Id: "+ str(Id)
		except Exception, e:
			print "foo "+str(e)
			

			
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
        print (start_index)
        end_index = start_index + int(each_slot)
        print (end_index)
        #pre_url = "http://think-tanks.findthedata.org"
        before_url = "http://think-tanks.findthedata.org/l/"
        #after_cik = "&type=8-k&dateb=&owner=exclude&count=100"
        #book = xlrd.open_workbook('CIKs.xlsx')
        #sheet = book.sheet_by_index(0)
		
		
        for h in range(start_index, end_index):
			param = []
			#CIK = sheet.cell_value(h,0)
			code = int(h+1)
			code = str(code)
			#CIK='1059142'
			#while len(CIK)<10:
				#CIK="0"+CIK
			#print CIK
			site_url = before_url + code #+ after_cik
			print "running index: "+str(h+1)+" & id: "+str(code)
			print site_url
			param.append(site_url)
			param.append(code)
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
	