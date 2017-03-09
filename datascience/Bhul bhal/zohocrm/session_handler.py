'''
Created on 18-Nov-2012

@author: Ankit Maheshwari 
'''
import webapp2
from webapp2_extras import sessions
#from google.appengine.ext import ndb


#This is needed to configure the session secret key
#Runs first in the whole application
myconfig_dict = {}
myconfig_dict['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
    'debug': True,
    'datastore': 'DatastoreSessionFactory'
}

#Session Handling class, gets the store, dispatches the request
class BaseSessionHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(backend='datastore')
#End of BaseSessionHandler Class