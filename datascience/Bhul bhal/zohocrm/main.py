#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import webapp2
import urllib
import urllib2
import json
import session_handler
import gdata
import oauth2client
import cloudDbHandler as dbhelper
import os
import sys
import datetime
from apiclient.discovery import build
#from oauth2client.appengine import OAuth2Decorator
from oauth2client import appengine
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from gdata.calendar.service import CalendarService
import apiclient
import time

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS

decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope=[
      'https://www.googleapis.com/auth/calendar'
    ],
    message=MISSING_CLIENT_SECRETS_MESSAGE)

"""decorator = OAuth2Decorator(
      client_id='669177946307@developer.gserviceaccount.com',
      client_secret='pbg2Xex8QjZDbmSTSgMaUKng',
      scope='https://www.googleapis.com/auth/calendar')"""

class zoho_integrate(session_handler.BaseSessionHandler):

    def getTaskList(self):
        module_name='Tasks'
        authtoken='7b64e8f8c6a3039b0e8199e02cdcca6b'
        params = {'authtoken':authtoken,'scope':'crmapi'}
        final_URL = 'https://crm.zoho.com/crm/private/json/'+[module_name]+'/getRecords'
        data = urllib.urlencode(params)
        request = urllib2.Request(final_URL,data)
        response = urllib2.urlopen(request)
        xml_response = response.read()
        data  = json.loads(xml_response)
    
        tasks_list  = data['response']['result'][module_name]['row']
        tasks = []
        for task in tasks_list:
            taskl = {}
            ts =  task['FL']
    
            for point in ts:
                if point['val'] == 'Subject':
                    #print "subject:",str(point['content'])
                    taskl['title'] = str(point['content'])
                elif point['val'] == 'ACTIVITYID':
                    #print "id:",str(point['content'])
                    taskl['id'] = str(point['content'])
                elif point['val'] == 'Due Date':
                    #print "subject:",str(point['content'])
                    taskl['due'] = str(point['content'])+'T12:00:00.000Z'
                elif point['val'] == 'Priority':
                    #print "subject:",str(point['content'])
                    taskl['priority'] = str(point['content'])
                elif point['val'] == 'status':
                    #print "subject:",str(point['content'])
                    taskl['status'] = str(point['content'])
                elif point['val'] == 'Related To':
                    #print "subject:",str(point['content'])
                    taskl['related_to'] = str(point['content'])
                elif point['val'] == 'Modified Time':
                    #print "subject:",str(point['content'])
                    taskl['modifiedtime'] = str(point['content'])

    @ decorator.oauth_required
    def get(self):
        if decorator.has_credentials():
            service = build('tasks', 'v1', http=decorator.http())
            http = decorator.http()
            tasks = service.tasks().list(tasklist='@default').execute(http=decorator.http())
            
        task_det = self.getTaskList()
        #tasklist = {
        #            'title': 'Zoho Tasks'
        #}
        #result = service.tasklists().insert(body=tasklist).execute(http=decorator.http())
        #listID = result['id']
        for task in task_det:
            taskd = {
                    'title':task['title'],
                    'due':task['due'],
                    'priority':task['priority'],
                    'related_to': task['related_to'],
                    'modifiedtime': task['modifiedtime']
                     }
            try:
                #print decorator
                #dbhelper.AddData().addGoogleAuthTokens(username, decorator.http(), str(datetime.datetime.now()))
                user_details =decorator.http().request("https://www.googleapis.com/oauth2/v3/userinfo?alt=json",method="POST")
                #print user_details[0]
                det = json.loads(user_details[1])
                
                #print det
                #print "lalal:",det['email']
                
                #user_det = user_details[1][1]
                #print str(user_det[1]['email'])
                username = det['email']
                dbhelper.AddData().addGoogleAuthTokens(username, decorator.http(), str(datetime.datetime.now()))
                gid=det['id']
                #gmodifiedtime=det['modifiedtime']
                tmodifiedtime=task['modifiedtime']
                print task['id']
                print str(datetime.datetime.now())
                print username
                print gid
                print task['modifiedtime']
                #print gmodifiedtime
                #while(zid==task['id'] || gid==)
                #if(gmodifiedtime!=gmodifiedtime && )
                dbhelper.AddData().addZohoLogs(task['id'],'task',str(datetime.datetime.now()),username,gid,task['modifiedtime'])
                newTask = service.tasks().insert(tasklist='@default', body=taskd).execute(http=decorator.http())
                
                 
                
            except Exception,e:
                print str(e),"Entry already thr !! "
            
        calendar_service =CalendarService()
        calendar_service.email ='sajagbahadur@gmail.com'
        calendar_service.password ='bihargaya'
        calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
        calendar_service.ProgrammaticLogin()
        feed = calendar_service.GetCalendarListFeed()
        for i, a_calendar in enumerate(feed.entry):
            print '\t%s. %s' % (i, a_calendar.title.text,)
          
        module_name = 'Events'
        authtoken = '7b64e8f8c6a3039b0e8199e02cdcca6b'
        params = {'authtoken':authtoken,'scope':'crmapi'}
        final_URL = "https://crm.zoho.com/crm/private/json/"+module_name+"/getRecords"
        data = urllib.urlencode(params)
        request = urllib2.Request(final_URL,data)
        response = urllib2.urlopen(request)
        xml_response = response.read()
        data  = json.loads(xml_response)
        
        tasks_list  = data['response']['result']['Events']['row']
        for task in tasks_list:
            ts =  task['FL']
            for point in ts:
                if point['val'] == 'Subject':
                    #print "subject:",str(point['content'])
                    subject = str(point['content'])
                elif point['val'] == 'Start DateTime':
                    #print "subject:",str(point['content'])
                    start_time = str(point['content'])
                elif point['val'] == 'ACTIVITYID':
                    print "subject:",str(point['content'])
                    zoho_id = str(point['content'])
                elif point['val'] == 'Contact Name':
                    #print "subject:",str(point['content'])
                    contact_name = str(point['content'])
                elif point['val'] == 'Related To':
                    #print "subject:",str(point['content'])
                    related_to = str(point['content'])
                elif point['val'] == 'End DateTime':
                    #print "subject:",str(point['content'])
                    end_time = str(point['content'])
                    
                
                    #event = gdata.calendar.CalendarEventEntry()
                    #event.title = atom.Title(text=subject)
                    #event.content = atom.Content(text=contact_name+" related to "+related_to)
                    #event.where.append(gdata.calendar.Where(value_string="Call"))
                    
                    #start_time = time.strptime( start_time,'%Y-%m-%d %H:%M:%S')
                    #end_time = time.strptime(end_time,'%Y-%m-%d %H:%M:%S')
                    #start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                    start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S' ).strftime('%Y-%m-%dT%H:%M:%S.000')
                    end_time = datetime.datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S' ).strftime('%Y-%m-%dT%H:%M:%S.000')
                    #end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                    
                    #print start_time,end_time
                
                    if start_time is None:
                        # Use current time for the start_time and have the event last 1 hour
                        start_time = time.strftime('%Y-%m-%d %H:%M:%S.000Z', time.gmtime())
                        end_time = time.strftime('%Y-%m-%d %H:%M:%S.000Z', time.gmtime(time.time() + 3600))
                    #event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
                    print start_time ,end_time
                    event = {
                              'summary': subject,
                              'location': 'On Call',
                              'start': {
                                'dateTime': str(start_time) + '+05:30'
                              },
                              'end': {
                                'dateTime': str(end_time)+'+05:30'
                              }
                            }
                    try:
                        
                        print zoho_id
                        print username
                        print str(datetime.datetime.now())
                        #dbhelper.AddData().addZohoLogs(zoho_id,'event',str(datetime.datetime.now()),username)
                
                        #new_event = cal_service.events().insert(calendarId='primary', body=event).execute(http=decorator.http())

                    
                        #print 'New single event inserted: %s' % (new_event.id.text,)
                        #print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
                        #print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)
                    except Exception,e:
                        print "Error:",str(e),"The calender entry is already entered."

app = webapp2.WSGIApplication([
('/', zoho_integrate)
], debug=True,
config = session_handler.myconfig_dict)