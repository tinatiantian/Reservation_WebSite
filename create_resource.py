import cgi
import os
import urllib
import datetime
import uuid

from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2

import login
import resources_datastore



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


    
class CreateresourcePageHandler(webapp2.RequestHandler):
  
  def get(self):
  	params = self.request.params
  	context = { }
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	contents = JINJA_ENVIRONMENT.get_template('create_resource.html').render(context)
  	self.response.write(contents)
  	
  	
  	
  def post(self):
  	params = self.request.params
  	context = { }
  	context = login.generateLogInOutContextInfo(self, context)
  	
  	"""Query all resources"""
  	resources_query = resources_datastore.resource.query(ancestor=resources_datastore.resources_key()).order(-resources_datastore.resource.resourceStartTime);
  	resources = resources_query.fetch(1000000);
  	context['resources'] = resources;
  	
  	"""Parse HTML date and time inputs into datetime object"""
  	rawStartTimeInput = params['resource_start_time'];
  	startDate = rawStartTimeInput.split("T")[0];
  	startTime = rawStartTimeInput.split("T")[1];
  	startDateTokens = startDate.split("-");
  	startTimeTokens = startTime.split(":");
  	parsedStartTimeInput = datetime.datetime(int(startDateTokens[0]), int(startDateTokens[1]), int(startDateTokens[2]), int(startTimeTokens[0]), int(startTimeTokens[1]));
  	
  	rawEndTimeInput = params['resource_end_time'];
  	endDate = rawEndTimeInput.split("T")[0];
  	endTime = rawEndTimeInput.split("T")[1];
  	endDateTokens = endDate.split("-");
  	endTimeTokens = endTime.split(":");
  	parsedEndTimeInput = datetime.datetime(int(endDateTokens[0]), int(endDateTokens[1]), int(endDateTokens[2]), int(endTimeTokens[0]), int(endTimeTokens[1]));
  	
  	resourceGUID = str(uuid.uuid4());
  	
  	"""Add template values"""
  	context['notification'] = 'resource Created!';
  	context['resourceResponse'] = True;
  	context['resourceGUID'] = resourceGUID;
  	context['resourceInstructor'] = users.get_current_user().nickname();
  	context['resourceOwner'] = users.get_current_user().user_id();
  	context['resourceEmail'] = users.get_current_user().email();
  	context['resourceName'] = params['resource_name'];
  	context['resourceStartTime'] = parsedStartTimeInput;
  	context['resourceEndTime'] = parsedEndTimeInput;
  	context['resourceTags'] = params['resource_tags'];
  	context['resourceRawStartTime'] = rawStartTimeInput;
  	context['resourceRawEndTime'] = rawEndTimeInput;
  	
  	"""Create resource for data store"""
  	resource = resources_datastore.resource(parent = resources_datastore.resources_key());
  	resource.resourceGUID = resourceGUID;
  	resource.resourceInstructor = users.get_current_user().nickname();
  	resource.resourceOwner = users.get_current_user().user_id();
  	resource.resourceEmail = users.get_current_user().email();
  	resource.resourceName = params['resource_name'];
  	resource.resourceStartTime = parsedStartTimeInput;
  	resource.resourceEndTime = parsedEndTimeInput;
  	resource.resourceTags = params['resource_tags'];
  	resource.resourceRawStartTime = rawStartTimeInput;
  	resource.resourceRawEndTime = rawEndTimeInput;
	  
	"""Determine if new resource is valid, handle appropriately"""
	present = datetime.datetime.now();
	if resource.resourceStartTime > present and resource.resourceStartTime < resource.resourceEndTime:
	  isValidNewresource = True;
	  for resourceClone in resources:
	    if resource.resourceOwner == resourceClone.resourceOwner and ((resource.resourceStartTime >= resourceClone.resourceStartTime and resource.resourceStartTime < resourceClone.resourceEndTime) or (resourceClone.resourceStartTime < resource.resourceEndTime and resource.resourceEndTime <= resourceClone.resourceEndTime)):
	      isValidNewresource = False;
	  if isValidNewresource:
	    resource.put();
	    context['notification'] = 'resource created!';
	  else:
	    context['notification'] = 'resource overlaps an existing resource!';
  	elif resource.resourceStartTime <= present:
  	  context['notification'] = 'Invalid start time specified!';
  	elif resource.resourceStartTime > resource.resourceEndTime:
  	  context['notification'] = 'Invalid end time specified!';
  	
  	contents = JINJA_ENVIRONMENT.get_template('create_resource.html').render(context)
  	self.response.write(contents)
  	
  	
  	
app = webapp2.WSGIApplication([
    ('/create_resource.*', CreateresourcePageHandler)
], debug = True)
