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


def GeneralInfo(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email):
		try:
					con = MySQLdb.connect(host='200.52.182.236', user='root', passwd='', db='findthedta', use_unicode=True, charset="utf8")
					ciur = con.cursor()
					cur.execute('INSERT INTO generalinfo(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(id,name, website_link, category, active,founders, current_director, board_of_directors_link,politicalaffiliation,research,mission,non_profit,funding,address,phonenumber,faxnumber,email)) 
					con.commit()
					con.close()
		except Exception, e:
					print ("DB Connection error")


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#url = URL
response = opener.open("http://think-tanks.findthedata.org/l/100")
page = response.read()
#from bs4 import BeautifulSoup
soup = Soup(page)
		#print soup

		#Head = soup.find('head')
		
		
#id=ID
#print id
"""		
Data=soup.findAll('td',{'class' :'fdata'})
Fname=soup.findAll('td',{'class' :'fname'})
print len(Fname)

#for i in range(0,len(Fname)-1):
TIP=Fname[2].find('div',{'class' : 'has-help-text'})
qwerty=(TIP.text).encode('utf8', 'ignore').strip().split(' ')[1]
print qwerty"""

try:
	NAME=soup.find('tr',{'class' :'component two-column first fieldedit even'})
	#print NAME
	name=NAME.findAll('td')
	namea=(name[1].text).encode('utf8','ignore').strip()
	print namea
except Exception,e:
	print "Error"+str(e)

try:
	WEB=soup.find('tr',{'class' :'component two-column fieldediturlmain odd'})
	web=WEB.find('a')#{'class' :'outbound_lnk'})
	weba=(web.get('href')).encode('utf8','ignore').strip()
	#print weba
	#website=(web[1].get('href')).encode('utf8','ignore').strip()
	print weba
except Exception,e:
	print "Error"+str(e)

try:
	CATEGORY=soup.find('tr',{'class' :'component two-column fieldlist even'})
	#print CATEGORY
	cat=(CATEGORY.findAll('td'))
	#print cat
	#Category=cat[2].text
	category=(cat[1].text).encode('utf8','ignore').strip()
	print category
except Exception,e:
	print "Error"+str(e)

try:
	ACTIVE=soup.find('tr',{'class' :'component two-column fieldcombo odd'})
	#print NAME
	act=ACTIVE.findAll('td')
	active=(act[1].text).encode('utf8','ignore').strip()
	print active
except Exception,e:
	print "Error"+str(e)	

try:
	FOUNDER=soup.find('tr',{'class' :'component two-column fieldedit even'})
	#print NAME
	found=FOUNDER.findAll('td')
	founder=(found[1].text).encode('utf8','ignore').strip()
	print founder
except Exception,e:
	print "Error"+str(e)	

try:
	DIRECTOR=soup.find('tr',{'class' :'component two-column fieldedit odd'})
	#print NAME
	Director=DIRECTOR.findAll('td')
	director=(Director[1].text).encode('utf8','ignore').strip()
	print director
except Exception,e:
	print "Error"+str(e)	

try:
	BOD_LINK=soup.find('tr',{'class' :'component two-column fieldediturl even'})
	Bod_link=BOD_LINK.find('a')#{'class' :'outbound_lnk'})
	board_of_directors_link=(web.get('href')).encode('utf8','ignore').strip()
	print board_of_directors_link
	#website=(web[1].get('href')).encode('utf8','ignore').strip()
	#print website
except Exception,e:
	print " "+str(e)
	board_of_directors_link='void'

try:
	POLITICAL=soup.find('tr',{'class' :'component two-column first fieldlist even'})
	#print NAME
	Political=POLITICAL.findAll('td')
	politicalaffiliation=(Political[1].text).encode('utf8','ignore').strip()
	print politicalaffiliation
except Exception,e:
	print " "+str(e)	
	
try:
	RESEARCH=soup.find('tr',{'class' :'component two-column fieldmledit even'})
	#print NAME
	Research=RESEARCH.findAll('td')
	research=(Research[1].text).encode('utf8','ignore').strip()
	print research
except Exception,e:
	print " "+str(e)
	
try:
	MISSION=soup.find('tr',{'class' :'component two-column fieldmledit odd'})
	#print NAME
	Mission=MISSION.findAll('td')
	mission=(Mission[1].text).encode('utf8','ignore').strip()
	print mission
except Exception,e:
	print " "+str(e)
	
try:
	NONPROFIT=soup.find('tr',{'class' :'component two-column first fieldcombo even'})
	#print NAME
	Nonprofit=NONPROFIT.findAll('td')
	non_profit=(Nonprofit[1].text).encode('utf8','ignore').strip()
	print non_profit
except Exception,e:
	print " "+str(e)	
	
try:
	FUNDING=soup.find('tr',{'class' :'component two-column fieldlist odd'})
	#print NAME
	Funding=FUNDING.findAll('td')
	funding=(Funding[1].text).encode('utf8','ignore').strip()
	print funding
except Exception,e:
	print " "+str(e)	

try:
	ADDRESS=soup.find('tr',{'class' :'component two-column address odd'})
	#print NAME
	Address=ADDRESS.findAll('td')
	address=(Address[1].text).encode('utf8','ignore').strip()
	print address
except Exception,e:
	print " "+str(e)

try:
	PHONE=soup.find('tr',{'class' :'component two-column fieldeditphone odd'})
	#print NAME
	Phone=PHONE.findAll('td')
	phonenumber=(Phone[1].text).encode('utf8','ignore').strip()
	print phonenumber
except Exception,e:
	print " "+str(e)	
	
try:
	FAX=soup.find('tr',{'class' :'component two-column fieldeditphone odd'})
	#print NAME
	Fax=FAX.findAll('td')
	faxnumber=(Fax[1].text).encode('utf8','ignore').strip()
	print faxnumber
except Exception,e:
	print " "+str(e)

try:
	EMAIL=soup.find('tr',{'class' :'component two-column fieldeditemail odd'})
	#print NAME
	Email=EMAIL.findAll('td')
	email=(Email[1].text).encode('utf8','ignore').strip()
	print email
except Exception,e:
	print " "+str(e)	
	
	