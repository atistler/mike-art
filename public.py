#!/usr/bin/env python

import cgi
import datetime
from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.base import BaseRequestHandler
from lib.base import PageNotFound
from lib.getimageinfo import getImageInfo
from lib.models import EventModel
from lib.models import GalleryModel
from lib.models import ImageModel2
from lib.models import LinkModel
from lib.models import SubscriberModel
import logging
import os
import wsgiref.handlers

base_template = "public.tpl"
_MAX_FETCH = 1000
PAGESIZE = 10

def priority_sort(x, y):
    if x.priority < y.priority:
        return 1
    elif x == y:
        return 0
    else:
        return -1

class Home(BaseRequestHandler):
    def get(self):
        paintings = GalleryModel.gql("WHERE name = :1", "Paintings").fetch(1)
        if paintings:
            paintings_gal = paintings[0]
        else:
            paintings_gal = None

        vinyl = GalleryModel.gql("WHERE name = :1", "Vinyl").fetch(1)
        if vinyl:
            vinyl_gal = vinyl[0]
        else:
            vinyl_gal = None

        illustrations = GalleryModel.gql("WHERE name = :1", "Illustrations").fetch(1)
        if illustrations:
            illustrations_gal = illustrations[0]
        else:
            illustrations_gal = None 

        photographs	= GalleryModel.gql("WHERE name = :1", "Photographs").fetch(1)
        if photographs:
            photographs_gal = photographs[0]
        else:
            photographs_gal = None
	

        data = {
            "paintings_gal":		paintings_gal,
            "vinyl_gal":			vinyl_gal,	
            "illustrations_gal":	illustrations_gal,
            "photographs_gal":		photographs_gal,
            "template":				"public/home.tpl"
        }
		
        self.generate(base_template, data)
		
class Gallery(BaseRequestHandler):
    def get(self):
        if (self.request.get("view")):
            id = self.request.get("view")
            self.view(id)
        else:
            self.error(503)

    def view(self, id):
        gal = GalleryModel.get(id)
        if (gal):
            imgs = ImageModel2.gql("WHERE gallery = :gallery", gallery=gal.key()).fetch(_MAX_FETCH)
            imgs = sorted(imgs, priority_sort)
                
            data = {
                "gal":		gal,
                "imgs":		imgs,
                "template":	"public/gallery_view.tpl"
            }
            self.generate(base_template, data)
        else:
            self.error(503)

class Events(BaseRequestHandler):
    def get(self):
        events = EventModel.gql("ORDER BY priority DESC").fetch(_MAX_FETCH);
        data = {
            "events": 	events,
            "template": "public/events.tpl"
        }
        self.generate(base_template, data)

class Links(BaseRequestHandler):
    def get(self):
        links = LinkModel.gql("ORDER BY priority DESC").fetch(_MAX_FETCH);
        data = {
            "links": 	links,
            "template": "public/links.tpl"
        }
        self.generate(base_template, data)


class Contacts(BaseRequestHandler):
    def get(self):
        data = {
            "template":	"public/contacts.tpl"
        }
        self.generate(base_template, data)
	
    def post(self):
        if (self.request.get("create")):
            self.create()
        else:
            self.error(503)

    def create(self):
        email_contact 		= SubscriberModel()
        email_contact.fname = self.request.get("fname")
        email_contact.lname = self.request.get("lname")
        email_contact.email = db.Email(self.request.get("email"))
        email_contact.put()
        data = {
            "submitted":	1,
            "fname":		email_contact.fname,
            "lname":		email_contact.lname,
            "email":		email_contact.email,
            "template":		"public/subscriber_confirm.tpl"
        }
        self.generate(base_template, data)
		
class Image(BaseRequestHandler):
    def get(self):
        if (self.request.get("view")):
            id = self.request.get("view")
            self.view(id)
        elif (self.request.get("render")):
            id = self.request.get("render")
            self.render(id)
        elif (self.request.get("render_thumb")):
            id = self.request.get("render_thumb")
            self.render_thumb(id)
        else:
            self.error(503)

    def view(self, id):
        img = ImageModel2.get(id)
        if (img):
            data = {
                "img":		img,
                "template":	"public/image_view.tpl"
            }
            self.generate(base_template, data)
        else:
            self.error(503)

    def render(self, id):
        img = ImageModel2.get(id)
        img_name = img.name.replace(' ', '');
        img_name 
        if (img):
            content_type, width, height = getImageInfo(img.imageblob.image)
            self.response.headers['Content-Type'] = content_type 
            self.response.headers['Content-Disposition'] = 'filename=' + img_name
            self.response.out.write(img.imageblob.image)
        else:
            self.error(404)
	
    def render_thumb(self, id):
        img = ImageModel2.get(id)
        if img:
            content_type, width, height = getImageInfo(img.imageblob.thumbnail)
            self.response.headers['Content-Type'] = content_type
            self.response.headers['Content-Disposition'] = img.name
            self.response.out.write(img.imageblob.thumbnail)
        else:
            self.error(404)
	
class Bio(BaseRequestHandler):
    def get(self):
        data = {
            "template":	"public/bio.tpl"
        }
        self.generate(base_template, data)


application = webapp.WSGIApplication([
                                     ('/home', Home),
                                     ('/bio', Bio),
                                     (r'/contacts.*', Contacts),
                                     ('/links', Links),
                                     ('/events', Events),
                                     (r'/gallery/.*', Gallery),
                                     (r'/image/.*', Image),
                                     (r'.*', Home)
                                     ], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

