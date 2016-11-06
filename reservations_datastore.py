from google.appengine.ext import ndb



"""Get key for datastore"""
def reservations_key():
  return ndb.Key('Reservations', 'default_reservations')

"""Representation of a reservation for datastore"""
class Reservation(ndb.Model):
  """Model for representing an individual reservations entry."""
  reservationTime = ndb.DateTimeProperty(indexed = True);
  reservationGUID = ndb.StringProperty(indexed = True);
  reservationOwnerName = ndb.StringProperty(indexed = True);
  reservationOwner = ndb.StringProperty(indexed = True);
  reservationEmail = ndb.StringProperty(indexed = True);
  reservationStartTime = ndb.DateTimeProperty(indexed = True);
  reservationDuration = ndb.IntegerProperty(indexed = False);
  resourceGUID = ndb.StringProperty(indexed = False);
  resourceInstructor = ndb.StringProperty(indexed = False);
  resourceOwner = ndb.StringProperty(indexed = False);
  resourceName = ndb.StringProperty(indexed = False);
