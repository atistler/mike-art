#!/usr/bin/env python

import logging
import datetime
from google.appengine.api import images
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from lib.base import BaseRequestHandler
from lib.getimageinfo import getImageInfo
from lib.models import EventModel, GalleryModel, ImageModel2, LinkModel, SubscriberModel
from xml.sax.saxutils import quoteattr


base_template = "public.tpl"
empty_template = "empty.tpl"
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
        data = {
            "template":				"public/home.tpl"
        }	
        self.generate(base_template, data)
		
class Gallery(BaseRequestHandler):
    def get(self):
        logging.debug(self.request.path)
        gal_id = -1
        gal_name = ""
        if (self.request.get("view")):
            gal_id = self.request.get("view")
        elif (self.request.path.startswith('/illustrations')):
            gal_name = 'illustrations'
            gal_id = GalleryModel.gql("WHERE name = :name", name='Illustrations').fetch(1)[0].key()
        elif (self.request.path.startswith('/vinyl')):
            gal_name = 'vinyl'
            gal_id = GalleryModel.gql("WHERE name = :name", name='Vinyl').fetch(1)[0].key()
        elif (self.request.path.startswith('/photographs')):
            gal_name = 'photographs'
            gal_id = GalleryModel.gql("WHERE name = :name", name='Photographs').fetch(1)[0].key()
        elif (self.request.path.startswith('/paintings')):
            gal_name = 'paintings'
            gal_id = GalleryModel.gql("WHERE name = :name", name='Paintings').fetch(1)[0].key()
        else:
            self.error(503)

        if ( self.request.path.endswith('list') ):
            self.view_xml(gal_id)
        elif ( self.request.path.endswith('flash') ):
            self.view_flash(gal_name)
        else:
            self.view(gal_id, gal_name)

    def view_flash(self,gal_name):
        data = {
            'gal_name': gal_name,
            'template': 'public/gallery.tpl'
        }
        self.generate(empty_template,data)


    def view_xml(self, id):
        gal = GalleryModel.get(id)
        if (gal):
            imgs = ImageModel2.gql("WHERE gallery = :gallery", gallery=gal.key()).fetch(_MAX_FETCH)
            imgs = sorted(imgs, priority_sort)
            xml = '<?xml version="1.0" encoding="utf-8"?>'
            xml += '<pics>'
            for img in imgs:
                src = '/image/?render=%s' % img.key()
                xml += '<pic src=%s title=%s/>' % (quoteattr(src), quoteattr(img.name))
            xml += '</pics>'
            self.response.headers['Content-Type'] = 'application/xml'
            self.response.out.write(xml)
        else:
            self.error(503)

    def view(self, id, gal_name):
        gal = GalleryModel.get(id)
        if (gal):
            imgs = ImageModel2.gql("WHERE gallery = :gallery", gallery=gal.key()).fetch(_MAX_FETCH)
            imgs = sorted(imgs, priority_sort)
                
            data = {
                "gal_name":     gal_name,
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
        image_model = ImageModel2.get(id)
        img_name = image_model.name.replace(' ', '');
        if (image_model):
            img = images.Image(image_model.imageblob.image)
            img.resize(1024, 768)
            image_output = img.execute_transforms(output_encoding=images.JPEG)
            self.response.headers['Content-Type'] = 'image/jpeg' 
            self.response.headers['Content-Disposition'] = 'filename=' + img_name
            expires = datetime.datetime.now() + datetime.timedelta(days=7)
            self.response.headers.add_header("Expires", expires.strftime("%a, %d %b %Y %H:%M:%S %Z") + "GMT")
            self.response.headers['Cache-Control'] = 'public,max-age=%d' % int(7*24*60)            
            self.response.out.write(image_output)
        else:
            self.error(404)
	
    def render_thumb(self, id):
        img = ImageModel2.get(id)
        if img:
            content_type, width, height = getImageInfo(img.imageblob.thumbnail)
            self.response.headers['Content-Type'] = content_type
            self.response.headers['Content-Disposition'] = img.name
            expires = datetime.datetime.now() + datetime.timedelta(days=7)
            self.response.headers.add_header("Expires", expires.strftime("%a, %d %b %Y %H:%M:%S %Z") + "GMT")
            self.response.headers['Cache-Control'] = 'public,max-age=%d' % int(7*24*60) 
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
                                     (r'/(?:paintings|illustrations|vinyl|photographs).*', Gallery),
                                     (r'/.*', Home)
                                     ], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

