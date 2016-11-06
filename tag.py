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
import backtohome



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
    
    
class TagPageHandler(webapp2.RequestHandler):
	
  def get(self):
    params = self.request.params
    context = { }

    context = backtohome.redirectToIndexPage(self, context);

    contents = JINJA_ENVIRONMENT.get_template('mainpage.html').render(context)
    self.response.write(contents)
	
		
	
  def post(self):
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
  	
  	"""Find matching resource"""
  	matchingresources = [];
  	for resource in resources:
  	  resourceTags = str(resource.resourceTags).split(",");
  	  for tag in resourceTags:
  	  	if tag.strip() == params['tagName'].strip():
  	  	  matchingresources.append(resource);
  	
  	context['str'] = str;
  	context['present'] = datetime.datetime.now();
  	context['datetime'] = datetime; 
  	context['resources'] = matchingresources;
	context['tagName'] = params['tagName'];
  	
  	contents = JINJA_ENVIRONMENT.get_template('tag.html').render(context)
  	self.response.write(contents)
  	
  	
  	
app = webapp2.WSGIApplication([
    ('/tag.*', TagPageHandler)
], debug = True)
