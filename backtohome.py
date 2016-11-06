import datetime

from google.appengine.api import users

import login
import resources_datastore
import reservations_datastore



def redirectToIndexPage(self, context):
  params = self.request.params
  context = { }

  """Generate log in/out information"""
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
  reservations_query = reservations_datastore.Reservation.query(ancestor=reservations_datastore.reservations_key()).order(-reservations_datastore.Reservation.reservationTime);
  reservations = reservations_query.fetch(1000000);
  context['reservations'] = reservations;
  
  resourcesGUIDByLastReservation = [];
  resourcesByLastReservation = [];
  allTags = [];
  
  for reservation in reservations:
    if not (reservation.resourceGUID in resourcesGUIDByLastReservation):
      resourcesGUIDByLastReservation.append(reservation.resourceGUID);
      for resource in resources:
        if resource.resourceGUID == reservation.resourceGUID:
          resourcesByLastReservation.append(resource);
          break;
  for resource in resources:
    if not (resource in resourcesByLastReservation):
      resourcesByLastReservation.append(resource);
  context['resourcesByLastReservation'] = resourcesByLastReservation;

  for resource in resources:
    for tag in str(resource.resourceTags).split(","):
      if tag not in allTags:
        allTags.append(tag);
  context['allTags'] = allTags;

  context['present'] = datetime.datetime.now();
  context['datetime'] = datetime;
  context['str'] = str;
  
  return context;
