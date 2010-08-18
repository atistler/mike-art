#!/usr/bin/env python

import cgi
import datetime
from django.template import Context
from django.template import Template
import django.template.loader
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
from lib.models import ImageBlobModel
from lib.models import ImageModel
from lib.models import ImageModel2
from lib.models import LinkModel
from lib.models import SubscriberModel
import logging
import os
import wsgiref.handlers


template_base = "admin.tpl"
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
        self.redirect("/admin/gallery/?view=all")
        
class Image(BaseRequestHandler):
    def get(self):
        if (self.request.get("view")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("view")
            if (id == "all"):
                self.view_all()
            else:
                self.view(id)
        elif (self.request.get("migrate_all")):
            self.migrate_all()
        else:
            self.response.out.write("image action undef")

    def post(self):
        if (self.request.get("create")):
            self.create()
        elif (self.request.get("delete")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("delete")
            self.delete(id)
        elif (self.request.get("update")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("update")
            self.update(id)
        elif (self.request.get("migrate")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("migrate")
            self.migrate(id)
        else:
            self.response.out.write("gallery action undef")

    def view(self, id):
        img = ImageModel.get(id)
        if img:
            data = {
                "img": 		img,
                "template":	"admin/image_view.tpl"
            }
            self.generate(template_base, data)
        else:
            self.error(503)

    def view_all(self):
        imgs = ImageModel.all()
        imgs = sorted(imgs, priority_sort)
        result_imgs = []
        for img in imgs:
            contenttype, width, height = getImageInfo(img.image)
            img.contenttype = contenttype
            result_imgs.append(img)
            
        gallerys = GalleryModel.all()

        data = {
            "imgs":	result_imgs,
            "gals":	gallerys,
            "template":	"admin/image_view_all.tpl"
        }
        self.generate(template_base, data)

    def create(self):
        img = ImageModel()
        contenttype, width, height = getImageInfo(self.request.get("img"));
			
        img.name	= self.request.get("name")
        img.desc	= self.request.get("desc")
        img.priority	= int(self.request.get("priority"))
        img.image	= db.Blob(self.request.get("img"))
        img.gallery	= GalleryModel.get(self.request.get("gallery")).key()
        img.thumbnail	= db.Blob(images.resize(self.request.get("img"), 80, 60))
        img.put()
        referrer = self.request.headers['referer']
        self.redirect(referrer)

    def migrate_all(self):
        imgs = ImageModel.all()
        for img in imgs:
            result = ImageModel2.gql("WHERE orig_image = :img", img=img.key()).fetch(1)
            if not result:
                imgblob             = ImageBlobModel()
                imgblob.image       = img.image
                imgblob.thumbnail   = img.thumbnail
                imgblob.put()
            
                img2            = ImageModel2()
                img2.name       = img.name
                img2.desc       = img.desc
                img2.orig_image = img.key()
                img2.priority   = img.priority
                img2.gallery    = img.gallery
                img2.imageblob  = imgblob.key()
                img2.put()
            else:
                logging.info("Image %s has already been migrated" % img.key())

            
    def migrate(self, id):
        img = ImageModel.get(id)
        if (img):
            result = ImageModel2.gql("WHERE orig_image = :img", img=img.key()).fetch(1)
            if not result:
                imgblob             = ImageBlobModel()
                imgblob.image       = img.image
                imgblob.thumbnail   = img.thumbnail
                imgblob.put()
            
                img2            = ImageModel2()
                img2.name       = img.name
                img2.desc       = img.desc
                img2.priority   = img.priority
                img2.orig_image = img.key()
                img2.gallery    = img.gallery
                img2.imageblob  = imgblob.key()
                img2.put()
                referrer = self.request.headers['referer']
                self.redirect(referrer)
            else:
                logging.info("Image %s has already been migrated" % img.key())
                referrer = self.request.headers['referer']
                self.redirect(referrer)                
        else:
            self.error(503)
            
    def delete(self, id):
        img = ImageModel.get(id)
        if img:
            img.delete()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)

    def update(self, id):
        img = ImageModel.get(id)
        if img:
            img.name		= self.request.get("name")
            img.desc		= self.request.get("desc")
            img.priority	= int(self.request.get("priority"))
            img.gallery		= GalleryModel.get(self.request.get("gallery")).key()
            img.put()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)

class Subscriber(BaseRequestHandler):
    def get(self):
        if (self.request.get("export")):
            subscribers = SubscriberModel.all().fetch(_MAX_FETCH)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.headers['Content-Disposition'] = 'attachment;filename="MailingList.txt"'
            for s in subscribers:
                self.response.out.write('"' + s.fname + ' ' + s.lname + '"' + ' <' + s.email + '>')
                self.response.out.write("\n")
        else:
            subscribers = SubscriberModel.all().fetch(_MAX_FETCH)
            data = {
                "subscribers":	subscribers,
                "template":	 	"admin/subscriber_view_all.tpl"
            }
            self.generate(template_base, data)

    def post(self):
        if (self.request.get("delete")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("delete")
            self.delete(id)
        else:
            self.response.out.write("subscriber action undef")


    def delete(self, id):
        subscriber = SubscriberModel.get(id)
        if subscriber:
            subscriber.delete()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)

class Link(BaseRequestHandler):
    def get(self):
        links = LinkModel.all().fetch(_MAX_FETCH)
        data = {
            "links": 		links,
            "template":	 	"admin/link_view_all.tpl"
        }
        self.generate(template_base, data)

    def post(self):
        if (self.request.get("create")):
            self.create()
        elif (self.request.get("update")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("update")
            self.update(id)
        elif (self.request.get("delete")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("delete")
            self.delete(id)
        else:
            self.response.out.write("link action undef")

    def create(self):
        link = LinkModel(
                         name=self.request.get("name"),
                         link=self.request.get("link"),
                         priority=int(self.request.get("priority"))
                         )
        link.put()
        referrer = self.request.headers['referer']
        self.redirect(referrer)

    def delete(self, id):
        link = LinkModel.get(id)
        if link:
            link.delete()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)

    def update(self, id):
        link = LinkModel.get(id)
        if link:
            link.name		= self.request.get("name")
            link.link		= self.request.get("link")
            link.priority	= int(self.request.get("priority"))
            link.put()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)
			
class Event(BaseRequestHandler):
    def get(self):
        events = EventModel.all().fetch(_MAX_FETCH)
        data = {
            "events": 		events,
            "template":	 	"admin/event_view_all.tpl"
        }
        self.generate(template_base, data)

    def post(self):
        if (self.request.get("create")):
            self.create()
        elif (self.request.get("update")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("update")
            self.update(id)
        elif (self.request.get("delete")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("delete")
            self.delete(id)
        else:
            self.response.out.write("event action undef")

    def create(self):
        event = EventModel(
                           name=self.request.get("name"),
                           location=self.request.get("location"),
                           date=self.request.get("date"),
                           priority=int(self.request.get("priority"))
                           )
        event.put()
        referrer = self.request.headers['referer']
        self.redirect(referrer)

    def delete(self, id):
        event = EventModel.get(id)
        if event:
            event.delete()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)

    def update(self, id):
        event = EventModel.get(id)
        if event:
            event.name		= self.request.get("name")
            event.date		= self.request.get("date")
            event.location	= self.request.get("location")
            event.priority	= int(self.request.get("priority"))
            event.put()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)
			
class Gallery(BaseRequestHandler):
    def get(self):
        if (self.request.get("view")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("view")
            if (id == "all"):
                self.view_all()
            else:
                self.view(id)
        elif (self.request.get("migrate_all")):
            self.migrate_all(self.request.get("migrate_all"))
        else:
            self.response.out.write("gallery action undef")

    def post(self):
        if (self.request.get("create")):
            self.create()
        elif (self.request.get("delete")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("delete")
            self.delete(id)
        elif (self.request.get("update")):
            if (self.request.get("id")):
                id = self.request.get("id")
            else:
                id = self.request.get("update")
            self.update(id)
        else:
            self.response.out.write("gallery action undef")
            
    def migrate_all(self, id):
        gal = GalleryModel.get(id)
        if (gal):
            imgs = ImageModel.gql("WHERE gallery = :gallery", gallery=gal.key()).fetch(_MAX_FETCH)
            for img in imgs:
                result = ImageModel2.gql("WHERE orig_image = :img", img=img.key()).fetch(1)
                if not result:
                    imgblob             = ImageBlobModel()
                    imgblob.image       = img.image
                    imgblob.thumbnail   = img.thumbnail
                    imgblob.put()
            
                    img2            = ImageModel2()
                    img2.name       = img.name
                    img2.desc       = img.desc
                    img2.orig_image = img.key()
                    img2.priority   = img.priority
                    img2.gallery    = img.gallery
                    img2.imageblob  = imgblob.key()
                    img2.put()   
                else:
                    logging.info("Image %s has already been migrated" % img.key())
                    
        else:
            logging.info("Gallery %s not found" % id)
            self.error(503)
            

            

    def view(self, id):
        gal = GalleryModel.get(id)
        if (gal):
            result_imgs = []
            imgs = ImageModel.gql("WHERE gallery = :gallery", gallery=gal.key()).fetch(_MAX_FETCH)

            imgs = sorted(imgs, priority_sort)
        

            data = {
                "gal":			gal,
                "imgs_count":           len(imgs),
                "imgs":			imgs,
                "template":		"admin/gallery_view.tpl"
            }
            self.generate(template_base, data)
        else:
            self.error(503)

    def view_all(self):
        gals = GalleryModel.all().fetch(_MAX_FETCH)
        data = {
            "gals": 		gals,
            "template":	 	"admin/gallery_view_all.tpl"
        }
        self.generate(template_base, data)

    def create(self):
        gal = GalleryModel(
                           name=self.request.get("name"),
                           desc=self.request.get("desc")
                           )
        gal.put()
        referrer = self.request.headers['referer']
        self.redirect(referrer)

    def delete(self, id):
        gal = GalleryModel.get(id)
        if gal:
            gal.delete()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)

    def update(self, id):
        gal = GalleryModel.get(id)
        if gal:
            gal.desc		= self.request.get("desc")
            gal.put()
            referrer = self.request.headers['referer']
            self.redirect(referrer)
        else:
            self.error(503)

application = webapp.WSGIApplication([
                                     (r'/admin/event/.*', Event),
                                     (r'/admin/link/.*', Link),
                                     (r'/admin/subscriber/.*', Subscriber),
                                     (r'/admin/image/.*', Image),
                                     (r'/admin/gallery/.*', Gallery),
                                     (r'/admin.*', Home),
                                     (r'/.*', PageNotFound)
                                     ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

