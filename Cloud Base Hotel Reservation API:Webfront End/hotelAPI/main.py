#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
	('/customer', 'customer.Customer'),
  ('/hotel', 'hotel.Hotel')
], debug=True)

app.router.add(webapp2.Route(r'/customer/<id:[0-9]+><:/?>','customer.Customer'))
app.router.add(webapp2.Route(r'/customer/<did:[0-9]+><:/?>/delete','customer.CustomerDelete'))
app.router.add(webapp2.Route(r'/customer/search', 'customer.CustomerSearch'))
app.router.add(webapp2.Route(r'/hotel/<hoid:[0-9]+><:/?>','hotel.Hotel'))
app.router.add(webapp2.Route(r'/hotel', 'hotel.Hotel'))
app.router.add(webapp2.Route(r'/hotel/<hid:[0-9]+>/customer/<cid:[0-9]+><:/?>', 'hotel.HotelCustomers'))
app.router.add(webapp2.Route(r'/hotel/search', 'hotel.HotelSearch'))
app.router.add(webapp2.Route(r'/hotel/<dhid:[0-9]+><:/?>/delete','hotel.HotelDelete'))