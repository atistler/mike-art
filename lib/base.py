#!/usr/bin/env python

import cgi
import datetime
import logging
import os
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import images
from google.appengine.api import users

_DEBUG=False

class BaseRequestHandler(webapp.RequestHandler):
	def generate(self,template_name,template_values={}):
		values = {
			"request":	self.request,
			"app_name":	"michaelferrari.net"
		}

		values.update(template_values)
		directory = os.path.dirname(__file__)
		path = os.path.join(directory,os.path.join("templates",template_name))
		self.response.out.write(template.render(path,values,debug=_DEBUG))

class PageNotFound(webapp.RequestHandler):
    def get(self):
        self.request.error(503)

