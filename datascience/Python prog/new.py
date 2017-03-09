from bs4 import BeautifulSoup as Soup
import MySQLdb
import requests
import mysql.connector
import glob
import json
import re
#import excelHelper
#import dbHandler
import random
import urllib
import csv
import traceback
#import psutil
import os

files_list=glob.glob("C:\Users\Vivek\Desktop\Python prog//*.html")
file_num=0
for files in files_list:
	try:
		file_num=file_num+1
		q = files.split("\\")
		z = q[5].strip('.html')
		z=str(z)
		print str(file_num)+","+str(z)
		filename = "C:\Users\Vivek\Desktop\Python prog\\"+z+".html"
		f = open(filename , 'r').read()
		name_index = f.find('<td colspan="4"><br /><b>') + len('<td colspan="4"><br /><b>')
		colg_index = [m.start() for m in re.finditer('<td width="80%" align="left">', f)]
		for i in range(len(colg_index)):
			colg_index[i] = colg_index[i] + len('<td width="80%" align="left">')
		email_index = [m.start() for m in re.finditer('<td align="left"><a href="mailto:', f)]
		for j in range(len(email_index)):
			email_index[j] = email_index[j] + len('<td align="left"><a href="mailto:')
		name = ""
		if name_index:
			while (f[name_index] != '<' and f[name_index+1] != '/' and f[name_index+2] != 'b' and f[name_index+3] != '>'):
				name += f[name_index]
				name_index += 1 
		print name

		colg_names = []
		colg_name = ""
		if colg_index:
			for i in range(len(colg_index)):
				colg_name = ""
				while (f[colg_index[i]] != '<'):
					colg_name += f[colg_index[i]]
					colg_index[i] += 1
				print colg_name
				colg_names.append(colg_name)
		print colg_names


		email_ids = []
		email_id = ""
		if email_index:
			for j in range(len(email_index)):
				email_id = ""
				while (f[email_index[j]] != '"'):
					email_id += f[email_index[j]]
					email_index[j] += 1 
				print email_id
				email_ids.append(email_id)
		print email_ids
		if colg_index:
			for i in range(len(colg_index)):
				try:
					dbHandler.addColgProfs(i+1,z,name,colg_names[i],email_ids[i])
					print "Saved in DB"

				except Exception, e:
					print str(z)+":"+str(e)
	except Exception, e:
		print str(e)
		con = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='ssrn_contacts', use_unicode=True, charset="utf8")
		cur = con.cursor()
		cur.execute('INSERT INTO error_email (author_id) values (%s)',(z)) 
		mid = cur.lastrowid
		con.commit()
		con.close()