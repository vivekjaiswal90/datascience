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


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
url ="http://think-tanks.findthedata.org/l/100"
response = opener.open(url)
page = response.read()
#from bs4 import BeautifulSoup
soup = Soup(page)
#print soup

#Head = soup.find('head')

"""Id = (Head.find('link'))#.encode('utf8', 'ignore').strip()
id=(Id.get('href')).strip().split('/')[4]
id=str(id)"""
		
#id=ID
#print id
		
Data=soup.findAll('td',{'class' :'fdata'})
Fname=soup.findAll('td',{'class' :'fname'})
a=len(Fname)

#Fname=soup.findAll('td',{'class' :'fname'})
		#count=1
for i in range(0,a-1):
#FNAME=Fname[i]
#FNAME=(FNAME.find('div')).text
				
				#print FNAME
	TIP=((Fname[i].findAll('div',{'class' : 'tip'}))[0].text).encode('utf8', 'ignore').strip()
	print TIP
#count=1
#print len(Data)
#print len(Fname)
#print Fna
#name=Fname[14].text
#name=Fname[0]..text
#web=((Fname[1].findAll('div',{'class' : 'tip'}))[0].text).encode('utf8', 'ignore').strip()

#w=(web[0].text).encode('utf8', 'ignore').strip()
#print name
#for i in range(0,len(Data)-1):
	#FNAME=Fname[i].find('div')
	#FNAME=Fname[i].text
	#abc=FNAME.split(' ')[1]
	
	#abc=FNAME.find('div')
	#print FNAME
	"""for i in range(0,len(Fname)-1):
				#FNAME=Fname[i]
				#FNAME=(FNAME.find('div')).text
				#print FNAME
				
				TIP=((Fname[i].find('div',{'class' : 'tip'}))[0].text).encode('utf8', 'ignore').strip()
				print TIP
				if Fname[i].text==' Think Tank':
					try:
						name=Data[i].text
						#print name
					except Exception,e:
						name='void'
						print"NAME"+str(e)
						
				elif TIP=='Think tank website.':
					try:
						Website_link=Data[i].find('a')
						website_link=(Website_link.get('href')).strip()
						#print website_link
					except Exception,e:
						website_link='void'
						print "WEBSITE LINK"+str(e)
						
				elif TIP=='What type of category does the think tank fall in? Is it educational, public policy, etc?':
					try:
						category=Data[i].text
						#print category
					except Exception,e:
						category='void'
						print"CATEGORY"+str(e)
						
				elif TIP=='Is the think tank still active?':
					try:
						active=Data[i].text
						#print active
					except Exception,e:
						active='void'
						print "ACTIVE"+str(e)
						
				elif TIP=='Who founded the think tank?':
					try:
						founders=Data[i].text
						#print founders
					except Exception,e:
						founders='void'
						print"FOUNDERS"+str(e)
						
				elif Fname[i].text==' Current Director':
					try:
						current_director=Data[i].text
						#print current_director
					except Exception,e:
						current_director='void'
						print "CURRENT DIRECTOR"+str(e)
						
				elif FNAME=='Link to Board of Directors':
					try:
						Board_of_directors_link=Data[i].find('a')
						board_of_directors_link=(Board_of_directors_link.get('href')).encode('utf8', 'ignore').strip()
						#print board_of_directors_link
					except Exception,e:
						board_of_directors_link='void'
						print"B_O_DLINK"+str(e)
						
				elif Fname[i].text==' Political Affiliation':
					try:
						politicalaffiliation=Data[i].text
						#print politicalaffiliation
					except Exception,e:
						politicalaffiliation='void'
						print"POLITICALAFFILIATION"+str(e)
						
				elif TIP=='Type of research the think tank focuses on.':
					try:
						research=Data[i].text
						#print research
					except Exception,e:
						research='void'
						
				elif TIP=='The mission or goal of the think tank.  ':
					try:
						mission=Data[i].text
						#print mission
					except Exception,e:
						mission='void'
						print "MISSION"+str(e)
						
				elif TIP=='Does the think tank work for a non-profit organization?':
					try:
						non_profit=Data[i].text
						#print non_profit
					except Exception,e:
						non_profit='void'
						print"NONPROFIT"+str(e)
						
				elif TIP=='Where does the think tank receive funding?':
					try:
						funding=Data[i].text
						#print funding
					except Exception,e:
						funding='void'
						print"FUNDING"+str(e)
						
				elif Fname[i].text=='Address':
					try:
						address=Data[i].text
						#print address
					except Exception,e:
						address='void'
						print "ADDRESS"+str(e)
						
				elif Fname[i].text==' Phone Number':
					try:
						phonenumber=Data[i].text
						#print phonenumber
					except Exception,e:
						phonenumber='void'
						print"PHONE NUMBER"+str(e)
						
				elif Fname[i].text==' Fax Number':
					try:
						faxnumber=Data[i].text
						#print faxnumber
					except Exception,e:
						faxnumber='void'
						print"FAXNUMBER"+str(e)
						
				elif Fname[i].text==' Email Address':
					try:
						email=Data[i].text
						#print email
					except Exception,e:
						email='void'
						print"EMAIL"+str(e)

		

		

		

		

		


		

		

		#posturl=soup.find('div',{'class' :'content'})
		#post_url=posturl.find('form')
		#pourl=(post_url.get('action')).strip()
		#print pourl
		#pre_url="http://think-tanks.findthedata.org"
		#site_url=pre_url+pourl
		#print site_url
		
	except	Exception,e:
		print "Connection"+str(e)
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
		email='void'"""