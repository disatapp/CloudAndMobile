import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb

from webapp2_extras import security

# http://eecs.oregonstate.edu/ecampus-video/player/player.php?id=99
class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Update(Model):
	name = ndb.StringProperty(required=True)
	rooms = ndb.StringProperty(required=True)
	room_count = ndb.IntegerProperty(required=True)		

class Hotel(Model):
	username = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	rooms = ndb.StringProperty(repeated=True)
	customers = ndb.KeyProperty(repeated=True)
	updates = ndb.StructuredProperty(Update, repeated=True)

	def to_dict(self):
		d = super(Hotel, self).to_dict()
		d['customers'] = [m.id() for m in d['customers']]
		return d

class Customer(Model):
	name = ndb.StringProperty(required=True)
	email = ndb.StringProperty()
	phone = ndb.StringProperty()