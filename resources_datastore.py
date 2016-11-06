from google.appengine.ext import ndb



"""Get key for datastore"""
def resources_key():
  return ndb.Key('resources', 'default_resources')

"""Representation of a resource for datastore"""
class resource(ndb.Model):
  """Model for representing an individual resources entry."""
  resourceGUID = ndb.StringProperty(indexed = False);
  resourceInstructor = ndb.StringProperty(indexed = True);
  resourceOwner = ndb.StringProperty(indexed = False);
  resourceEmail = ndb.StringProperty(indexed = False);
  resourceName = ndb.StringProperty(indexed = True);
  resourceStartTime = ndb.DateTimeProperty(indexed = True);
  resourceEndTime = ndb.DateTimeProperty(indexed = True);
  resourceTags = ndb.StringProperty(indexed = False);
  resourceRawStartTime = ndb.StringProperty(indexed = False);
  resourceRawEndTime = ndb.StringProperty(indexed = False);
