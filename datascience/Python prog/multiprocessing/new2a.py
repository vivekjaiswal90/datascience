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

#Functions to add vales into the DB

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
					


					
#Now the calculation begins
def foo(id,site_url):
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		url = "http://think-tanks.findthedata.org/l/112"
		response = opener.open(url)
		page = response.read()
		#from bs4 import BeautifulSoup
		soup = Soup(page)
		#print soup

		Head = soup.find('head')
		Id = (Head.find('link'))#.encode('utf8', 'ignore').strip()
		id=(Id.get('href')).strip().split('/')[4]
		print id
		
		Name=soup.find('td')#,{'class' :'fname'})
		#print Name
		
	except Exception, e:
		print("Internet Connection lost or page not found")
	
	#try:
		#Name=soup.find('td',{'class' :'fdata'})
		#print Name