import StringIO
import webapp2
import jinja2
import cgi
import json
import ast
import datetime
import os
from google.appengine.api import rdbms


_INSTANCE_NAME = 'vivek-jwl-api:zohogoogle' 
dbname = 'zohogoogle'

class AddData():
    def addZohoLogs(self,zid,zoho_category,sync_time,username,gid,tmodifiedtime):
        try:
            
            conn = rdbms.connect(instance=_INSTANCE_NAME, database=dbname)
            cursor = conn.cursor()
            cursor.execute('insert into zoho_logs (id,zoho_category,sync_time,username,gid,tmodifiedtime) values (%s,%s,%s,%s,%s,%s)',(zid,zoho_category,sync_time,username,gid,tmodifiedtime))
            conn.commit()
            testid = cursor.lastrowid
            conn.close()
            return testid
        except Exception,e:
            print str(e)
            return False
    def addGoogleAuthTokens(self,username,decoratorhttpobj,timenow):
        try:
            conn = rdbms.connect(instance=_INSTANCE_NAME, database=dbname)
            cursor = conn.cursor()
            cursor.execute('insert into googletokens (username,decoratorhttpobj,timenow) values (%s,%s,%s)',(username,decoratorhttpobj,timenow))
            conn.commit()
            testid1 = cursor.lastrowid
            conn.close()
            return testid1
        except Exception,e:
            print str(e)
            return False