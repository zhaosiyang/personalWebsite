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
import os
import re
import jinja2
from google.appengine.ext import db
import random
import hashlib
import string
import urllib2
from xml.dom import minidom
import json
import logging
import time

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def openFile(documentSource):
	fr = open(documentSource, 'r')
	text = fr.read()
	fr.close()
	return text
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
class MainHandler(Handler):
	def get(self):
		self.response.write(openFile('index.html'))
class Education(Handler):
	def get(self):
		self.render("education.html")
class Work(Handler):
	def get(self):
		self.render("work.html")
class Project(Handler):
	def get(self):
		self.render("project.html")
class Contact(Handler):
	def get(self):
		self.render("contact.html")


class WebChatDB(db.Model):
	contents = db.TextProperty(required = True)
	date_time = db.DateTimeProperty(auto_now_add = True)

class WebChat(Handler):
	def get(self):
		entries = db.GqlQuery("SELECT * FROM WebChatDB ORDER BY date_time")
		if entries.count() != 0:
			for entry in entries:
				self.write( "<tr><td>" + entry.contents + "</td></tr>" )
	def post(self):
		action = self.request.get("action")
		if action == "enter":
			contents = self.request.get("contents")
			# self.write(contents)
			WebChatDB(contents = contents).put()
		else:   #action == "clear"
			entries = db.GqlQuery("SELECT * FROM WebChatDB ORDER BY date_time")
			for entry in entries:
				entry.delete()

app = webapp2.WSGIApplication([
	('/education', Education),
	('/work', Work),
	('/project', Project),
	('/contact', Contact),
	('/webchat',WebChat),
    ('/', MainHandler)
], debug=True)
