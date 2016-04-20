import webapp2
from google.appengine.ext import ndb
import db_models
import json
# http://eecs.oregonstate.edu/ecampus-video/player/player.php?id=99
class Hotel(webapp2.RequestHandler):
	def post(self):
		# Creates a Hotel entity

		# POST Body Variables:
		# name - Required. Hotel name
		# customers[] - Array of customer ids
		# rooms[] - Array of Hotel rooms
		
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return

		new_hotel = db_models.Hotel()
		username = self.request.get('username', default_value=None)
		name = self.request.get('name', default_value=None)
		customers = self.request.get_all('customers[]', default_value=None)
		rooms = self.request.get_all('rooms[]', default_value=None)
		if name:
			new_hotel.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"

		if customers:
			for customer in customers:
				new_hotel.customers.append(ndb.Key(db_models.Customer, int(customer)))
		if rooms:
			new_hotel.rooms = rooms
		if rooms:
			new_hotel.username = username
		for room in new_hotel.rooms:
			print room
		key = new_hotel.put()
		out = new_hotel.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return
		if 'hoid' in kwargs:
			out = ndb.Key(db_models.Hotel, int(kwargs['hoid'])).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_models.Hotel.query()
			key = q.fetch(keys_only=True)
			results = {'key' : [x.id() for x in key]}
			self.response.write(json.dumps(results))

class HotelSearch(webapp2.RequestHandler):
	def get(self):
		# Search a Customer entity
		# 	Return value:
		# 	phone
		# 	email

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return
		user = self.request.get('username', None)
		if user:
			test = {'data': [p.to_dict() for p in db_models.Hotel.query(db_models.Hotel.username == user).fetch()]}
			self.response.write(json.dumps(test))
		# q = db_models.Hotel.query()
		# if self.request.get('username', None):
		# 	q = q.filter(db_models.Hotel.name != self.request.get('username'))
		# if self.request.get('rooms', None):
		# 	q = q.filter(db_models.Hotel.rooms != self.request.get('rooms'))
		# key = q.fetch()

		# json.dumps()
		# results = {'key' : [x.id() for x in key]}

		# self.response.write(json.dumps(key))



class HotelCustomers(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status_message = 406
			self.response.status_message = "Not Acceptable"
			return

		if not ndb.Key(db_models.Hotel, self.request.get('username')):
			self.response.status_message = 401
			self.response.status_message = "Not Authorized"
			return

		hotel = None
		customer = None
		if 'hid' in kwargs:
			hotel = ndb.Key(db_models.Hotel, int(kwargs['hid'])).get()
			if not hotel:
				self.response.status = 404
				self.response.status_message = "Hotel Not Found"
				return
		if 'cid' in kwargs:
			customer = ndb.Key(db_models.Customer, int(kwargs['cid']))
			if not customer: 
				# Does this need to be in Hotel??
				self.response.status = 404
				self.response.status_message = "Customer Not Found"
				return
			if customer not in hotel.customers:
				hotel.customers.append(customer)
				hotel.put()
		self.response.write(json.dumps(hotel.to_dict()))
		return

class HotelDelete(webapp2.RequestHandler):
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable"
			return
		if 'dhid' in kwargs:
			entity = ndb.Key(db_models.Hotel, int(kwargs['dhid'])).delete()
			self.response.write('Success: Entity deleted\n')