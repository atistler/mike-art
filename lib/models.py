#!/usr/bin/env python

from google.appengine.ext import db

class GalleryModel(db.Model):
    name        = db.StringProperty()
    desc	= db.StringProperty(multiline=True)
    created     = db.DateTimeProperty(auto_now_add=True)

class ImageModel(db.Model):
    name        = db.StringProperty()
    desc        = db.StringProperty(multiline=True)
    priority	= db.IntegerProperty(default=0)
    image       = db.BlobProperty()
    thumbnail	= db.BlobProperty()
    gallery    	= db.ReferenceProperty(GalleryModel)
    created     = db.DateTimeProperty(auto_now_add=True)

class ImageBlobModel(db.Model):
    image       = db.BlobProperty()
    thumbnail   = db.BlobProperty()
    
class ImageModel2(db.Model):
    name        = db.StringProperty()
    desc        = db.StringProperty(multiline=True)
    priority	= db.IntegerProperty(default=0)
    gallery    	= db.ReferenceProperty(GalleryModel)
    orig_image  = db.ReferenceProperty(ImageModel)
    created     = db.DateTimeProperty(auto_now_add=True)
    imageblob   = db.ReferenceProperty(ImageBlobModel)

class SubscriberModel(db.Model):
    fname	= db.StringProperty()
    lname	= db.StringProperty()
    email	= db.EmailProperty()

class EventModel(db.Model):
    name	= db.StringProperty()
    location	= db.StringProperty(multiline=True)
    date	= db.StringProperty()	
    priority	= db.IntegerProperty(default=0)

class LinkModel(db.Model):
    name	= db.StringProperty()
    link	= db.LinkProperty()
    priority	= db.IntegerProperty(default=0)
