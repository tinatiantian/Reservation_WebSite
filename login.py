from google.appengine.api import users

def generateLogInOutContextInfo(self, context):
  user = users.get_current_user()
  if user:
    context['userLogInOutLink'] = users.create_logout_url(self.request.uri)
    context['userLogInOutText'] = 'Sign Out'
  else:
  	context['userLogInOutLink'] = users.create_login_url(self.request.uri)
  	context['userLogInOutText'] = 'Sign In'
  return context
