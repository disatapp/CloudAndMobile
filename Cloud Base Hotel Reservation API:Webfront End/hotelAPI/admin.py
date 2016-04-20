import webapp2
from google.appengine.api import oauth
# http://eecs.oregonstate.edu/ecampus-video/player/player.php?id=99
app = webapp2.WSGIApplication([
	('/customer', 'customer.Customer'),
	('/', 'customer.Customer')
], debug=True)

app.router.add(webapp2.Route(r'/customer/<id:[0-9]+><:/?>','customer.Customer'))
app.router.add(webapp2.Route(r'/customer/<did:[0-9]+><:/?>/delete','customer.CustomerDelete'))
app.router.add(webapp2.Route(r'/customer/search', 'customer.CustomerSearch'))
app.router.add(webapp2.Route(r'/hotel/<hoid:[0-9]+><:/?>', 'hotel.Hotel'))
app.router.add(webapp2.Route(r'/hotel/search', 'hotel.HotelSearch'))
app.router.add(webapp2.Route(r'/hotel/<hid:[0-9]+>/customer/<cid:[0-9]+><:/?>', 'hotel.HotelCustomers'))
