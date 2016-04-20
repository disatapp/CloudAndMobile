#!/usr/bin/env python

import logging
import os.path
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError


######################################
#        Authenicate Handler         #
######################################

def user_required(handler):
  def check_login(self, *args, **kwargs):
    auth = self.auth
    if not auth.get_user_by_session():
      self.redirect(self.uri_for('login'), abort=True)
    else:
      return handler(self, *args, **kwargs)

  return check_login

######################################
#            Base Handler            #
######################################

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def auth(self):
    return auth.get_auth()

  @webapp2.cached_property
  def user_info(self):
    return self.auth.get_user_by_session()

  @webapp2.cached_property
  def user(self):
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None

  @webapp2.cached_property
  def session(self):
      return self.session_store.get_session(backend="datastore")

  @webapp2.cached_property
  def user_model(self):   
    return self.auth.store.user_model

#http://forums.udacity.com/questions/100006286/posting-data-using-ajax-in-gae-405-method-not-allowed
  def render_template(self, view_filename, argu=None):
    if not argu:
      argu = {}
    user = self.user_info
    argu['user'] = user
    path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
    self.response.out.write(template.render(path, argu))


  def display_message(self, message):
    argu = {
      'message': message
    }
    self.render_template('message.html', argu)

  # this is needed for webapp2 sessions to work
  def dispatch(self):
      self.session_store = sessions.get_store(request=self.request)

      try:
          webapp2.RequestHandler.dispatch(self)
      finally:
          self.session_store.save_sessions(self.response)

######################################
#             Main Handler           #
######################################

class MainHandler(BaseHandler):
  def get(self):
    self.render_template('home.html')


######################################
#           Signup Handler           #
######################################

class SignupHandler(BaseHandler):
  def get(self):
    self.render_template('signup.html')

  def post(self):
    name = self.request.get('username')
    email = self.request.get('email')
    fname = self.request.get('name')
    lname = self.request.get('lastname')
    password = self.request.get('password')

    up = ['email_address']
    usermod = self.user_model.create_user(name, up, email_address=email, name=fname, password_raw=password, last_name=lname, verified=False)
    if not usermod[0]: #user_data is a tuple
      self.display_message('Fail to create account with %s duplicate keys %s' % (name, usermod[1]))
      return
    
    user = usermod[1]
    user_id = user.get_id()
    signup_token = self.user_model.create_signup_token(user_id)

    loginurl = self.uri_for('verification', type='v', user_id=user_id, signup_token=signup_token, _full=True)

    msg = '<a href="{url}">{url}</a>'

    self.display_message(msg.format(url=loginurl))

######################################
#           Verifi Handler           #
######################################

class VerificationHandler(BaseHandler):
  def get(self, *args, **kwargs):
    ver = kwargs['type']
    user_id = kwargs['user_id']
    token = kwargs['signup_token']
   
    user = None
    user, ts = self.user_model.get_by_auth_token(int(user_id), token,'signup')

    if not user:
      logging.info('User ID not found "%s"',
        user_id, token)
      self.abort(404)

    self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

    if ver == 'v':
      self.user_model.delete_signup_token(user.get_id(), token)

      if not user.verified:
        user.verified = True
        user.put()

      self.display_message('Success: Email verified.')
      return
    else:
      logging.info('Invalid Action')
      self.abort(404)

######################################
#            Login Handler           #
######################################

class LoginHandler(BaseHandler):
  def get(self):
    self._render()

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')
    try:
      u = self.auth.get_user_by_password(username, password, remember=True, save_session=True)
      self.redirect(self.uri_for('home'))
    except (InvalidAuthIdError, InvalidPasswordError) as e:
      logging.info('Login failed for user %s because of %s', username, type(e))
      self._render(True)

  def _render(self, failed=False):
    username = self.request.get('username')
    argu = {
      'username': username,
      'failed': failed
    }
    self.render_template('login.html', argu)

######################################
#           Logout Handler           #
######################################

class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect(self.uri_for('home'))

######################################
#            Edit Handler            #
######################################

class DeleteHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('delete.html')

######################################
#          Create Handler            #
######################################

class CreateHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('createcustomer.html')


######################################
#            display Handler         #
######################################
class DisplayHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('display.html')

######################################
#            HEdit Handler           #
######################################

class HotelEditHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('edithotel.html')

######################################
#          HCreate Handler           #
######################################

class HotelCreateHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('createhotel.html')


######################################
#            Hview Handler           #
######################################

class HotelDisplayHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('displayhotel.html')


######################################
#            User Handler            #
######################################

class UserHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('user.html')

######################################
#              config                #
######################################

config = {
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

# http://stackoverflow.com/questions/18167504/adding-a-username-property-to-webapp2-user-model-after-entity-has-been-created

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/signup', SignupHandler),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<token:.+>', handler=VerificationHandler, name='verification'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/delete', DeleteHandler, name='delete'),
    webapp2.Route('/display', DisplayHandler, name='display'),
    webapp2.Route('/user', UserHandler, name='user'),
    webapp2.Route('/create', CreateHandler, name='create'),
    webapp2.Route('/viewhotel', HotelDisplayHandler, name='hoteldisplay'),
    webapp2.Route('/hotelcustomer', HotelEditHandler, name='edithotel'),
    webapp2.Route('/createhotel', HotelCreateHandler, name='createhotel')
], debug=True, config=config)

app.router.add(webapp2.Route(r'/customer/search', 'customer.CustomerSearch'))
app.router.add(webapp2.Route(r'/hotel/search', 'hotel.HotelSearch'))

logging.getLogger().setLevel(logging.DEBUG)
