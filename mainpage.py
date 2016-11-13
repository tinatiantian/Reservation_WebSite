import cgi
import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.db import Query
import jinja2
import webapp2

import login
import resources_datastore
import reservations_datastore
import backtohome

＃Ting's Copy'



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


    
class MainPageHandler(webapp2.RequestHandler):

  def get(self):
  	params = self.request.params
  	context = { }
  	context = backtohome.redirectToIndexPage(self, context);
    
  	contents = JINJA_ENVIRONMENT.get_template('mainpage.html').render(context)
  	self.response.write(contents)
  	
  	
  	
  def post(self):
  	params = self.request.params;
	  
	"""Query all reservations"""
  	reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(reservations_datastore.Reservation.reservationStartTime);
  	reservations = reservations_query.fetch(1000000);
	  
	"""Delete the reservation specified"""
	for reservation in reservations:
	  if reservation.reservationGUID == params['reservationGUID']:
	    reservation.key.delete();
	  
	self.get();


app = webapp2.WSGIApplication([
    ('/', MainPageHandler)
], debug = True)
