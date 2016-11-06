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
import reservations_datastore
import backtohome



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
    
    
class resourcePageHandler(webapp2.RequestHandler):

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
  	resources_query = resources_datastore.resource.query(ancestor=resources_datastore.resources_key()).order(-resources_datastore.resource.resourceStartTime)
  	resources = resources_query.fetch(1000000);
  	context['resources'] = resources;
  	
  	"""Get the clicked resource"""
  	for resource in resources:
  	  if resource.resourceGUID == params['resourceGUID']:
		context['resource'] = resource;
		thisresource = resource;
		
	"""Query all reservations"""
  	reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(-reservations_datastore.Reservation.reservationTime);
  	reservations = reservations_query.fetch(1000000);
  	context['reservations'] = reservations;
  	    
  	"""Check if modify resource form had been submitted"""
  	if 'edit_resource_submit' in params:	
  	  thisresource.resourceName = params['resource_name'];
  	  
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
  	  
  	  thisresource.resourceStartTime = parsedStartTimeInput;
  	  thisresource.resourceEndTime = parsedEndTimeInput;
  	  thisresource.resourceRawStartTime = params['resource_start_time'];
  	  thisresource.resourceRawEndTime = params['resource_end_time'];
  	  thisresource.resourceTags = params['resource_tags'];
  	  
  	  present = datetime.datetime.now();
  	  if thisresource.resourceStartTime > present and thisresource.resourceStartTime < thisresource.resourceEndTime:
  	  	thisresource.put();
		context['notification'] = 'resource modifications submitted!';
  	  elif thisresource.resourceStartTime <= present:
  	  	context['notification'] = 'Invalid start time specified!';
	  elif thisresource.resourceStartTime > resource.resourceEndTime:
  	  	context['notification'] = 'Invalid end time specified!';
  	  context['resource'] = thisresource;  	  



  	"""Check if a reservation form had been submitted"""
  	if user and 'reserve_resource_submit' in params:
  	  rawStartTimeInput = params['reservation_start_time'];
  	  startDate = rawStartTimeInput.split("T")[0];
  	  startTime = rawStartTimeInput.split("T")[1];
  	  startDateTokens = startDate.split("-");
  	  startTimeTokens = startTime.split(":");
  	  parsedStartTimeInput = datetime.datetime(int(startDateTokens[0]), int(startDateTokens[1]), int(startDateTokens[2]), int(startTimeTokens[0]), int(startTimeTokens[1]));
  	
	  reservationGUID = str(uuid.uuid4());
	  reservation = reservations_datastore.Reservation(parent = reservations_datastore.reservations_key()); 
	  reservation.reservationTime = datetime.datetime.now();
	  reservation.reservationGUID = reservationGUID;
	  reservation.reservationOwnerName = user.nickname();
	  reservation.reservationOwner = user.user_id();
	  reservation.reservationEmail = user.email();
	  reservation.reservationStartTime = parsedStartTimeInput;
	  reservation.reservationDuration = int(params['reservation_duration']);
	  reservation.resourceGUID = params['resourceGUID'];
	  reservation.resourceInstructor = params['resourceInstructor'];
	  reservation.resourceOwner = params['resourceOwner'];
	  reservation.resourceName = params['resourceName'];
	  
	  """Check if reservation valid before storing"""
	  alreadyReserved = False;
	  for reservationClone in reservations:
	  	if reservationClone.reservationOwner == user.user_id() and reservationClone.resourceGUID == params['resourceGUID']:
	  	  alreadyReserved = True;
	  
	  present = datetime.datetime.now();
	  durationInSeconds = reservation.reservationDuration * 60;
	  if alreadyReserved:
	  	context['notification'] = 'You have already reserved the resource!';
	  elif parsedStartTimeInput > present and parsedStartTimeInput >= thisresource.resourceStartTime and durationInSeconds > 0:
	    potentialEndTime = parsedStartTimeInput + datetime.timedelta(seconds = durationInSeconds);
	    if potentialEndTime <= thisresource.resourceEndTime:
	      reservation.put();
	      context['notification'] = 'Reservation made!';
	    else:
	      context['notification'] = 'Duration specified is too long!';
	  elif durationInSeconds <= 0:
	  	context['notification'] = 'Invalid duration specified!';
	  elif parsedStartTimeInput < thisresource.resourceStartTime:
	  	context['notification'] = 'Invalid start time specified!';
	  elif parsedStartTimeInput <= present:
	  	context['notification'] = 'Invalid start time specified!';
	  
	  context['reservationGUID'] = reservation.reservationGUID;
	  context['reservationOwnerName'] = reservation.reservationOwnerName;
	  context['reservationOwner'] = reservation.reservationOwner;
	  context['reservationEmail'] = reservation.reservationEmail;
	  context['reservationStartTime'] = reservation.reservationStartTime;
	  context['reservationDuration'] = reservation.reservationDuration;
	  context['resourceGUID'] = reservation.resourceGUID;
	  context['resourceInstructor'] = reservation.resourceInstructor;
	  context['resourceOwner'] = reservation.resourceOwner;
	  context['resourceName'] = reservation.resourceName;
	elif 'reserve_resource_submit' in params:
	  context['notification'] = 'You must be signed in to make a reservation!';
  	
  	context['present'] = datetime.datetime.now();
  	context['datetime'] = datetime;  	
  	
  	context['tags'] = str(context['resource'].resourceTags).split(",");
  	  	
  	contents = JINJA_ENVIRONMENT.get_template('resource.html').render(context)
  	self.response.write(contents)
  	
  	
  	
app = webapp2.WSGIApplication([
    ('/resource.*', resourcePageHandler)
], debug = True)
