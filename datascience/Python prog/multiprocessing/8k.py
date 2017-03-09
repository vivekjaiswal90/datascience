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
def add8kDetails(CIK, filing_date, period_report, items, items_count, accepted_date, accepted_time, CIK_check, fiscal_year_end, link_to_8k, type_file, press_release_found, link_press_release, press_release_date):
        try:
                    con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='8k_data', use_unicode=True, charset="utf8")
                    cur = con.cursor()
                    cur.execute('INSERT INTO 8k(CIK, filing_date, period_report, items, items_count, accepted_date, accepted_time, CIK_check, fiscal_year_end, link_to_8k, type_file, press_release_found, link_press_release, press_release_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(CIK, filing_date, period_report, items, items_count, accepted_date, accepted_time, CIK_check, fiscal_year_end, link_to_8k, type_file, press_release_found, link_press_release, press_release_date)) 
                    con.commit()
                    con.close()
        except Exception, e:
                    print ("DB Connection error")

#The CIK Page DB 
def cikPage(CIK, url, execution):
	try:
		con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='8k_data', use_unicode=True, charset="utf8")
		cur = con.cursor()

		cur.execute('INSERT INTO cikPage(CIK, url, execution) values (%s,%s,%s)',(CIK, url, execution)) 
		con.commit()

		con.close()
	except Exception, e:
		print ("DB Connection error")

#The Next Page DB
def nextPage(CIK, url, execution):
	try:
		con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='8k_data', use_unicode=True, charset="utf8")
		cur = con.cursor()

		cur.execute('INSERT INTO nextPage(CIK, url, execution) values (%s,%s,%s)',(CIK, url, execution)) 
		con.commit()

		con.close()
	except Exception, e:
		print ("DB Connection error")

#The Document Page DB
def docPage(CIK, url, execution):
	try:
		con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='8k_data', use_unicode=True, charset="utf8")
		cur = con.cursor()

		cur.execute('INSERT INTO docPage(CIK, url, execution) values (%s,%s,%s)',(CIK, url, execution)) 
		con.commit()

		con.close()
	except Exception, e:
		print ("DB Connection error")

#The Press Release Page DB
def prPage(CIK, url, execution):
	try:
		con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='8k_data', use_unicode=True, charset="utf8")
		cur = con.cursor()

		cur.execute('INSERT INTO prPage(CIK, url, execution) values (%s,%s,%s)',(CIK, url, execution)) 
		con.commit()

		con.close()
	except Exception, e:
		print ("DB Connection error")

def addItemDetails(CIK, url, item):
	try:
		con = MySQLdb.connect(host='192.168.1.14', user='root', passwd='', db='8k_data', use_unicode=True, charset="utf8")
		cur = con.cursor()

		cur.execute('INSERT INTO list_items(CIK, 8k_link, item) values (%s,%s,%s)',(CIK, url, item)) 
		con.commit()

		con.close()
	except Exception, e:
		print ("DB Connection error")




#The jack of all Calculations 
def foo (CIK, site_url):

	#print (site_url)
	pre_url = "http://www.sec.gov"
	#Navigating to the link
	#extracting the html source
	#print site_url
	cik_id = CIK

	try:
		r = requests.get(site_url)
		#print r.status_code
		soup = Soup(r.text)
		#print soup
		cikPage(CIK, site_url, 'Yes')

	except Exception, e:
		print("Internet Connection lost or page not found")
		cikPage(CIK, site_url, 'No')
	#print r.status_code

	#Finding the link to the next page
	try:
		Next_page = soup.find('input',{'value': 'Next 100'})
		next_page = (Next_page.get('onclick')).encode('utf8', 'ignore').strip()
		#print (next_page)
		url_next_page = next_page.split('\'')
		#print url_next_pageython
		url_next = pre_url + url_next_page[1]
		#print url_next
		#print ("I, found the lik to the next page")
		nextPage(CIK, url_next, 'Yes')

	except Exception,e:
		url_next = "False"
		#print ("Something went wrong, couldnt find the link tp the next page")
		nextPage(CIK, url_next, 'No')
		print ('Page Navigation ends: '+CIK)

	#print (url_next)

	#Extracting values for filings, description, filing_date, document url
	try:
		Table = soup.find('table', {'class':'tableFile2'})
		Rows = Table.findAll('tr')
	except Exception, e:
		Rows = 'void'
		print ('unable to find document table')

	document_url = []

	for i in range(1, len(Rows)):
		
		try:
			Col = Rows[i].findAll('td')
			if Col <> None:
				filings = (Col[0].text).encode('utf8', 'ignore').strip()
				description = (Col[2].text).encode('utf8', 'ignore').strip()
				filing_date = (Col[3].text).encode('utf8', 'ignore').strip()
				Doc = Col[1].find('a')
				Doc_url = (Doc.get('href')).encode('utf8', 'ignore').strip()
				doc_url = pre_url + Doc_url
				document_url.append(doc_url)

		except Exception,e:
			filings = 'void'
			description = 'void'
			filing_date = 'void'
			doc_url = 'void'

		#print (filings)
		#print (description)
		#print (filing_date)
		#print (doc_url)

	#Navigating to each and every document page
	for i in range(len(document_url)): 
		#print i
		try:
			#document_url[i]='http://www.sec.gov/Archives/edgar/data/4904/000000490411000059/0000004904-11-000059-index.htm'
			req = requests.get(document_url[i])
			soup = Soup(req.text)
			docPage(CIK, document_url[i], 'Yes')

		except Exception, e:
			print ('Couldnt open the document page')
			docPage(CIK, document_url[i], 'No')


		#Extracting Values for filing_date_check, period_report, items, items_count, accepted_date, accepted_time, cik, fiscal_year_end
		try: 
			Form1= soup.findAll('div', {'class': 'formGrouping'})
			#print (Form1)

			for j in range(len(Form1)):
				Info = Form1[j].findAll('div', {'class':'info'})
				#print (Info)
				if Info <> None:
					if j == 0:
						filing_date_check = (Info[0].text).encode('utf8', 'ignore').strip()
						Accepted = (Info[1].text).encode('utf8', 'ignore').strip()
						accepted_date = Accepted.split(' ')[0]
						accepted_time = Accepted.split(' ')[1]
						#print (filing_date_check)
						#print (Accepted)
					if j == 1:
						period_report = (Info[0].text).encode('utf8', 'ignore').strip()
						#print (period_report)
					if j == 2:
						items = (Info[0].text).encode('utf8', 'ignore').strip()
						#Item_count = soup.findAll('div',{'class': 'formGrouping'})
						Count_item = Info[0].findAll('br')
						count_item = len(Count_item)
						

						#print (items)
						#Item_count = Info.findAll('br')
						#item_count = len(Item_count)
						#print (item_count)

		except Exception,e:
			filing_date_check = 'void'
			period_report = 'void'
			Accepted = 'void'
			items = 'void'
			count_item = 'void'
			accepted_date = 'void'
			accepted_time = 'void'

		try:

			CIK_check = soup.find('span', {'class': 'companyName'})
			cik_check = CIK_check.find('a')
			#print (cik_check)
			cik = (cik_check.text).encode('utf8', 'ignore').strip().split(' ')[0]
			#print (cik)

			Fiscal_year = soup.find('p', {'class': 'identInfo'})
			#print (Fiscal_year)
			fiscal_year = Fiscal_year.findAll('strong')
			#print (fiscal_year)
			fiscal_year_end = (fiscal_year[2].text).encode('utf8', 'ignore').strip()
			#print (fiscal_year_end)

		except Exception,e:
			cik = 'void'
			fiscal_year_end = 'void'
			

		#print (filing_date_check)
		#print (period_report)
		#print (Accepted)
		#print (items)
		#print (count_item)
		#print (cik)
		#print (fiscal_year_end)

		#Extracting the link and value for 8k and type respectively
		#type_check = ''
		#link = ''
		try:
			table1 = soup.find('table', {'class':'tableFile'})
			#print (table1)
			table1_row = table1.findAll('tr')
			#print (table1_row)
			lets_count = 0
			for k in range(1, len(table1_row)):
				table1_col = table1_row[k].findAll('td')
				#print (table1_col)
				Type_check = ((table1_col[3].text).encode('utf8', 'ignore').strip()).lower()
				Description = ((table1_col[1].text).encode('utf8', 'ignore').strip()).lower()
				#print (Description)
				#print (Type_check)
				if (Type_check == '8-k' or Type_check == '8-k/a'):
					#print (Type_check)
					Link_8k = table1_col[2].find('a')
					link8k = (Link_8k.get('href')).encode('utf8', 'ignore').strip()
					link_8k = pre_url + link8k
					#print (link_8k)
					type_check =Type_check
					#print (type_check)
					#print (link_8k)
					#print (k)

				if (Description == 'press release'):
					press_release_found = 'Yes'
					Link_press_release = table1_col[2].find('a')
					linkPressRelease = (Link_press_release.get('href')).encode('utf8', 'ignore').strip()
					link_press_release = pre_url + linkPressRelease
					lets_count = 1

			if (lets_count == 0):
				press_release_found = 'No'
				link_press_release = 'void'
				
					


		except Exception,e:
			print (str(e))
			type_check = 'void'
			link_8k = 'void'
			press_release_found ='void'
			link_press_release = 'void'

		try:
			Text = soup.findAll('div', {'class' : 'info'})
			Cont = (Text[5]).contents
			for e in range(len(Cont)):
				cont = str(Cont[e]).encode('utf8', 'ignore').strip()
				if(cont != '<br/>'):
					addItemDetails(CIK, link_8k, cont)
		except Exception, e:
			print("Item Details could not be found")
			addItemDetails(CIK, link_8k, 'void')
		#print (type_check)
		#print (link_8k)
		#print (press_release_found)
		#print (link_press_release)

		#Model 4
		# Extracting press release date
		if (press_release_found == 'Yes'):
			try:
				#req1='http://www.sec.gov/Archives/edgar/data/11544/000001154413000028/wrb33113ex991.htm'
				req1 = requests.get(link_press_release)
				soup = Soup(req1.text)
				prPage(CIK, link_press_release, 'Yes')

			except Exception, e:
				prPage(CIK, link_press_release, 'No')


			try:
				txt = soup.find('text').text
				m = re.search('(Jan.|Feb.|Mar.|Apr.|Jun.|Jul.|Aug.|Sep.|Sept.|Oct.|Nov.|Dec.|January|February|March|April|May|June|July|August|September|October|November|December).{1}\d{2}\,\s\d{4}', txt) 
				press_release_date = m.group(0)
				#print m.group(0)
			except Exception,e:
				press_release_date = 'Not Found'

		else:
			#print ("No Press release")
			press_release_date = 'void'

		add8kDetails(CIK, filing_date_check, period_report, items, count_item, accepted_date, accepted_time, cik, fiscal_year_end, link_8k, type_check, press_release_found, link_press_release, press_release_date)
	
	if(url_next != "False"):
		foo(CIK, url_next)
	


def foo1 (y):
	print len(y)
	for t in y:
		try:
			CIK = t[1]
			site_url = t[0]
			foo(CIK, site_url)
			print "Done CIK: "+ str(CIK)
		except Exception, e:
			print "foo "+str(e)



if __name__ == '__main__':


    start_page = raw_input("Enter start index:")
    end_page = raw_input("Enter end index:")
    if int(end_page) < int(start_page):
    	end_page = raw_input("end page can't be less  that start indes Enter again:")
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



