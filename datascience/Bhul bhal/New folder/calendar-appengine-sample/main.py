#!/usr/bin/env python
#
# Copyright 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Starting template for Google App Engine applications.

Use this project as a starting point if you are just beginning to build a Google
App Engine project. Remember to download the OAuth 2.0 client secrets which can
be obtained from the Developer Console <https://code.google.com/apis/console/>
and save them as 'client_secrets.json' in the project directory.
"""
import cloudDbHandler as dbhelper
import urllib
import urllib2
import httplib2
import json
import logging
import os
import gdata
from apiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache
from apiclient.discovery import build

import webapp2
import jinja2

from gdata.calendar.service import CalendarService

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
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

http = httplib2.Http(memcache)
service = discovery.build('calendar', 'v3', http=http)
decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=MISSING_CLIENT_SECRETS_MESSAGE)

class MainHandler(webapp2.RequestHandler):

  @decorator.oauth_required
  def get(self):
    variables = {
        'url': decorator.authorize_url(),
        'has_credentials': decorator.has_credentials()
        }
    template = JINJA_ENVIRONMENT.get_template('main.html')
    self.response.write(template.render(variables))

    if decorator.has_credentials():
      service = build('calendar', 'v3', http=decorator.http())
      http = decorator.http()
    
    # Build a service object for interacting with the API. Visit
    # the Google Cloud Console
    # to get a developerKey for your own application.
    #service = build(serviceName='calendar', version='v3', http=http,developerKey='YOUR_DEVELOPER_KEY')

    module_name='Tasks'
    authtoken='7b64e8f8c6a3039b0e8199e02cdcca6b'
    params = {'authtoken':authtoken,'scope':'crmapi'}
    final_URL = "https://crm.zoho.com/crm/private/json/Tasks/getRecords"
    data = urllib.urlencode(params)
    request = urllib2.Request(final_URL,data)
    response = urllib2.urlopen(request)
    xml_response = response.read()
    data  = json.loads(xml_response)

    tasks_list  = data['response']['result']['Tasks']['row']
    tasks = []
    for task in tasks_list:
      taskl = {}
      ts =  task['FL']
      for point in ts:
        if point['val'] == 'Subject':
          self.response.write(point['content'])
        """taskl['title'] = str(point['content'])
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
                taskl['modifiedtime'] = str(point['content'])"""    

    #dbhelper.AddData().addZohoLogs(task['id'],'task',str(datetime.datetime.now()),username,gid,task['modifiedtime'])  
    #rule = service.acl().get(calendarId='primary', ruleId='ruleId').execute()
    #print '%s: %s' % (rule['id'], rule['role'])
    calendar_service =CalendarService()
    calendar_service.email ='vivekjwl@gmail.com'
    calendar_service.password ='ybntkamshkviwibz'
    calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
    calendar_service.ProgrammaticLogin()
    feed = calendar_service.GetCalendarListFeed()
    event = service.events().get(calendarId='primary', eventId='5nhvgdb7s2uiagopo07p141jug').execute()
    self.response.write(event['status'])
    self.response.write(event['htmlLink'])
    self.response.write(event['created'])
    self.response.write(event['updated'])
    self.response.write(event['description'])
    self.response.write(event['status'])
    self.response.write(event['creator']['displayName'])
    self.response.write(event['id'])
    #self.response.write(event['etag'])
    #self.response.write(event['id'])

    dbhelper.AddData().addcalendarlogs(event['id'],event['summary'],event['created'],event['updated'],event['description'])


    calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
    #self.response.write(calendar_list_entry)
    """rule = {
        'scope': {
            'type': 'default',
            'value': '',
        },
        'role': 'read'
    }"""

    calendar_list_entry = service.calendarList().get(calendarId='primary').execute()

    #self.response.write(calendar_list_entry)


    """page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        self.response.write(calendar_list_entry)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
          break
    #etag=calendar['etag']
    #print etag
    for i, a_calendar in enumerate(feed.entry):
      self.response.write('\t%s. %s' % (i, a_calendar.title.text))"""


    #event = service.events().get(calendarId='primary', eventId='5nhvgdb7s2uiagopo07p141jug').execute()
    #print event['summary']
  
app = webapp2.WSGIApplication(
    [
     ('/', MainHandler)
    ],
    debug=True)
