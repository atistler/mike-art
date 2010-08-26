#!/usr/bin/env python

import os
from google.appengine.ext.webapp import template, RequestHandler


_DEBUG=False

class BaseRequestHandler(RequestHandler):
	def generate(self,template_name,template_values={}):
		values = {
			"request":	self.request,
			"app_name":	"michaelferrari.net"
		}

		values.update(template_values)
		directory = os.path.dirname(__file__)
		path = os.path.join(directory,os.path.join("templates",template_name))
		self.response.out.write(template.render(path,values,debug=_DEBUG))

class PageNotFound(RequestHandler):
    def get(self):
        self.request.error(503)

