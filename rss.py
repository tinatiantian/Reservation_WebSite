import cgi
import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

import login
import resources_datastore
import reservations_datastore



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
    
    
class XMLPageHandler(webapp2.RequestHandler):
  def get(self):
    params = self.request.params
    context = { }
    context = login.generateLogInOutContextInfo(self, context)

    """Get user information"""
    user = users.get_current_user();
    context['user'] = user;
    if user:
      context['userId'] = user.user_id();
      context['userEmail'] = user.email();

    """Query all resources"""
    resources_query = resources_datastore.resource.query(ancestor=resources_datastore.resources_key()).order(-resources_datastore.resource.resourceStartTime);
    resources = resources_query.fetch(1000000);
    context['resources'] = resources;
  	
    """Query all reservations"""
    reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(-reservations_datastore.Reservation.reservationStartTime);
    reservations = reservations_query.fetch(1000000);
    context['reservations'] = reservations;

    context['present'] = datetime.datetime.now();
    context['datetime'] = datetime;
    context['str'] = str;

    contents = JINJA_ENVIRONMENT.get_template('mainpage.html').render(context)
    self.response.write(contents)	



  def post(self):
  	params = self.request.params
  	context = { }
  	
  	"""Generate log in/out information"""
  	context = login.generateLogInOutContextInfo(self, context)

  	"""Query all resources"""
  	resources_query = resources_datastore.resource.query(ancestor=resources_datastore.resources_key()).order(-resources_datastore.resource.resourceStartTime);
  	resources = resources_query.fetch(1000000);
  	context['resources'] = resources;
  	
  	"""Query all reservations"""
  	reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(-reservations_datastore.Reservation.reservationTime);
  	reservations = reservations_query.fetch(1000000);
  	context['reservations'] = reservations;
  	
  	"""Get the selected resource"""
  	context['resourceGUID'] = params['resourceGUID'];
  	context['present'] = datetime.datetime.now();
  	context['datetime'] = datetime;  
  	
  	contents = JINJA_ENVIRONMENT.get_template('rss.html').render(context)
  	self.response.write(contents)
  	
  	
  	
app = webapp2.WSGIApplication([
    ('/rss.*', XMLPageHandler)
], debug = True)
