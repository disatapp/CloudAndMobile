import webapp2
from google.appengine.ext import ndb
import db_models
import json
# http://eecs.oregonstate.edu/ecampus-video/player/player.php?id=99
class Customer(webapp2.RequestHandler):
	def post(self):
		# """Creates a Customer entity
		# POST body Variables:
		# name - required
		# email - email
		# phone - Real name
		# """
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return
		new_customer = db_models.Customer()
		name = self.request.get('name', default_value=None)
		email = self.request.get('email', default_value=None)
		phone = self.request.get('phone', default_value=None)
		if	phone:
			new_customer.phone = phone
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
		if email:
			new_customer.email = email
		if name:
			new_customer.name = name
		key = new_customer.put()
		put = new_customer.to_dict()
		self.response.write(json.dumps(put))
		return

	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return
		if 'id' in kwargs:
			out = ndb.Key(db_models.Customer, int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_models.Customer.query()
			keys = q.fetch(keys_only=True)
			results = {'key' : [x.id() for x in keys]}
			self.response.write(json.dumps(results))

class CustomerSearch(webapp2.RequestHandler):
	def get(self):
		# Search a Customer entity
		# 	Return value:
		# 	phone
		# 	email

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return
		test = {'data': [p.to_dict() for p in db_models.Customer.query().fetch()]}
		self.response.write(json.dumps(test))

class CustomerDelete(webapp2.RequestHandler):
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return
		if 'did' in kwargs:
			entity = ndb.Key(db_models.Customer, int(kwargs['did'])).delete()
			self.response.write('Success: Entity deleted\n')
		