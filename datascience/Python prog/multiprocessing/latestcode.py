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
import time


def GeneralInfo(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email):
		try:
					con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='findthedta', use_unicode=True, charset="utf8")
					cur = con.cursor()
					cur.execute('INSERT INTO generalinfo(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)) 
					con.commit()
					con.close()
		except Exception, e:
					print ("DB Connection error"+str(e))


def foo(ID,URL):
	
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mediapartners-Google')]
		#url = URL
		response = opener.open(URL)
		page = response.read()
		#from bs4 import BeautifulSoup
		soup = Soup(page)
		"""r= requests.get(URL, proxies=proxies)
		site = r.text.encode('utf-8')
		soup=Soup(site)"""
		"""proxy = urllib2.ProxyHandler({'http': '190.145.26.6'})
		opener = urllib2.build_opener(proxy)
		urllib2.install_opener(opener)
		url = URL
		urllib2.urlopen(url)
		#opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		
		response = opener.open(url)
		page = response.read()"""
		
		
		#from bs4 import BeautifulSoup
		#soup = Soup(page)
		#print soup

		#Head = soup.find('head')
	except Exception,e:
		print "Cannont find the page"+str(e)
		
		"""Id = (Head.find('link'))#.encode('utf8', 'ignore').strip()
		id=(Id.get('href')).strip().split('/')[4]
		id=str(id)"""
			
	id=ID
	#print id
		
	#Data=soup.findAll('td',{'class' :'fdata'})
	#Fname=soup.findAll('td',{'class' :'fname'})
	#print len(Fname)
	#count=1
	try:
		NAME=soup.find('tr',{'class' :'component two-column first fieldedit even'})
		#print NAME
		namea=NAME.findAll('td')
		name=(namea[1].text).encode('utf8','ignore').strip()
		#print name
	except Exception,e:
		print "Name Error"+str(e)
		name='void'
		
	try:
		WEB=soup.find('tr',{'class' :'component two-column fieldediturlmain odd'})
		web=WEB.find('a')#{'class' :'outbound_lnk'})
		website_link=(web.get('href')).encode('utf8','ignore').strip()
		#print weba
		#website=(web[1].get('href')).encode('utf8','ignore').strip()
		#print website_link
	except Exception,e:
		print "Website Error"+str(e)
		website_link='void'
		
	try:
		CATEGORY=soup.find('tr',{'class' :'component two-column fieldlist even'})
		#print CATEGORY
		cat=(CATEGORY.findAll('td'))
		#print cat
		#Category=cat[2].text
		category=(cat[1].text).encode('utf8','ignore').strip()
		#print category
	except Exception,e:
		print "category Error"+str(e)
		category='void'
		
	try:
		ACTIVE=soup.find('tr',{'class' :'component two-column fieldcombo odd'})
		#print NAME
		act=ACTIVE.findAll('td')
		active=(act[1].text).encode('utf8','ignore').strip()
		#print active
	except Exception,e:
		print "Active Error"+str(e)
		active='void'
		
	try:
		FOUNDER=soup.find('tr',{'class' :'component two-column fieldedit even'})
		#print NAME
		found=FOUNDER.findAll('td')
		founders=(found[1].text).encode('utf8','ignore').strip()
		#print founders
	except Exception,e:
		print "Founder Error"+str(e)
		founders='void'	
		
	try:
		DIRECTOR=soup.find('tr',{'class' :'component two-column fieldedit odd'})
		#print NAME
		Director=DIRECTOR.findAll('td')
		current_director=(Director[1].text).encode('utf8','ignore').strip()
		#print current_director
	except Exception,e:
		print "Director Error"+str(e)
		current_director='void'	
		
	try:
		BOD_LINK=soup.find('tr',{'class' :'component two-column fieldediturl even'})
		Bod_link=BOD_LINK.find('a')#{'class' :'outbound_lnk'})
		board_of_directors_link=(web.get('href')).encode('utf8','ignore').strip()
		#print board_of_directors_link
		#website=(web[1].get('href')).encode('utf8','ignore').strip()
		#print website
	except Exception,e:
		print "BOD_link Error"+str(e)
		board_of_directors_link='void'
		
	try:
		POLITICAL=soup.find('tr',{'class' :'component two-column first fieldlist odd'})
		#print NAME
		Political=POLITICAL.findAll('td')
		politicalaffiliation=(Political[1].text).encode('utf8','ignore').strip()
		#print politicalaffiliation
	except Exception,e:
		print "Political Error"+str(e)	
		politicalaffiliation='void'
		
	try:
		RESEARCH=soup.find('tr',{'class' :'component two-column fieldmledit even'})
		#print NAME
		Research=RESEARCH.findAll('td')
		research=(Research[1].text).encode('utf8','ignore').strip()
		#print research
	except Exception,e:
		print "Research Error"+str(e)
		research='void'

	try:
		MISSION=soup.find('tr',{'class' :'component two-column fieldmledit odd'})
		#print NAME
		Mission=MISSION.findAll('td')
		mission=(Mission[1].text).encode('utf8','ignore').strip()
		#print mission
	except Exception,e:
		print "Mission Error"+str(e)
		mission='void'
	try:
		NONPROFIT=soup.find('tr',{'class' :'component two-column first fieldcombo odd'})
		#print NAME
		Nonprofit=NONPROFIT.findAll('td')
		non_profit=(Nonprofit[1].text).encode('utf8','ignore').strip()
		#print non_profit
	except Exception,e:
		print "Non profit Error"+str(e)
		non_profit='void'

	try:
		FUNDING=soup.find('tr',{'class' :'component two-column fieldlist even'})
		#print NAME
		Funding=FUNDING.findAll('td')
		funding=(Funding[1].text).encode('utf8','ignore').strip()
		#print funding
	except Exception,e:
		print "Funding Error"+str(e)	
		funding='void'
		
	try:
		ADDRESS=soup.find('tr',{'class' :'component two-column first address odd'})
		#print NAME
		Address=ADDRESS.findAll('td')
		address=(Address[1].text).encode('utf8','ignore').strip()
		#print address
	except Exception,e:
		print "Address Error"+str(e)
		address='void'
		
	try:
		PHONE=soup.find('tr',{'class' :'component two-column fieldeditphone even'})
		#print NAME
		Phone=PHONE.findAll('td')
		phonenumber=(Phone[1].text).encode('utf8','ignore').strip()
		#print phonenumber
	except Exception,e:
		print "Phone Error"+str(e)	
		phonenumber='void'
		
	try:
		FAX=soup.find('tr',{'class' :'component two-column fieldeditphone odd'})
		#print NAME
		Fax=FAX.findAll('td')
		faxnumber=(Fax[1].text).encode('utf8','ignore').strip()
		#print faxnumber
	except Exception,e:
		print "Fax Error"+str(e)
		faxnumber='void'
		
	try:
		EMAIL=soup.find('tr',{'class' :'component two-column fieldeditemail even'})
		#print NAME
		Email=EMAIL.findAll('td')
		email=(Email[1].text).encode('utf8','ignore').strip()
		#print email
	except Exception,e:
		print "Email Error"+str(e)
		email='void'	


	GeneralInfo(id,name,website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)
		
	
def foo1 (y):
	print len(y)
	for t in y:
		try:
			Id = t[1]
			url = t[0]
			print Id
			print url
			foo(Id,url)
			#print "Done Id: "+ str(Id)
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
			#print "running index: "+str(h+1)+" & id: "+str(code)
			print site_url
			param.append(site_url)
			param.append(code)
			#print param
			params.append(param)
			#print params
        #print len(urls)
       	final_params.append(params)
		#print final_params
    i= 0
    for y in final_params:
        i = i + 1
        pool.apply_async(foo1, args=(y, ))
       # print ("process: "+ str(i))
         

    pool.close()
    pool.join()