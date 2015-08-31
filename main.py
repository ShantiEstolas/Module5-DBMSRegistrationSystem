import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
import os
import logging
import json
import urllib



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
    year = ndb.IntegerProperty()
    thesis_title = ndb.StringProperty(indexed = True)
    abstract = ndb.StringProperty(indexed = True)
    adviser = ndb.StringProperty(indexed = True)
    section = ndb.IntegerProperty()
    created_by = ndb.StringProperty(indexed = True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    phone_number = ndb.StringProperty(indexed=True)
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # login_url = users.create_login_url('/home')
        # template_values = {
        #     'login_url': login_url
        # }
        # template = JINJA_ENVIRONMENT.get_template('login.html')
        # self.response.write(template.render(template_values))
        if user:
            login_url = users.create_login_url('/home')
            template_values = {
                'login_url': login_url
            }
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
        else:
            url = users.create_login_url('/register')
            self.redirect(users.create_login_url(self.request.uri))
            template_values = {
                'url': url
            }
            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render(template_values))

class RegisterPageHandler(webapp2.RequestHandler):
    def get(self):

        loggedin_user = users.get_current_user()

        if loggedin_user:
            user_key = ndb.Key('User', loggedin_user.user_id())
            
            template = JINJA_ENVIRONMENT.get_template('register.html')
            loggedout_url = users.create_logout_url('/login')
            template_values = {
                'logout_url': loggedout_url
            }
            self.response.write(template.render(template_values))
        else:

            self.redirect(users.create_login_url('/register'))

    def post(self):
        registered_user = User()
        registered_user.first_name =self.request.get('first_name')
        registered_user.last_name = self.request.get('last_name')
        registered_user.email = self.request.get('email')
        registered_user.phone_number = self.request.get('phone_number')
        registered_user.put()
        self.redirect('/home')
        #loggedin_user = users.get_current_user()

        # current_user = User(id = loggedin_user.users_id(), email = loggedin_user.user.email(), first_name = loggedin_user.user.first_name(), last_name = loggedin_user.user.last_name(), phone_number=loggedin_user.phone_number())
        # current_user.put()
        # self.redirect('/home')

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + user.nickname())
            url = users.create_logout_url('/login')
            template = JINJA_ENVIRONMENT.get_template('main.html')
            template_values = {
                'user': user,
                'logout_url': url
            }
            self.response.write(template.render(template_values))
        else:
            url = users.create_login_url(self.request.uri)
            self.redirect(users.create_login_url(self.request.uri))
            template_values = {
                'url': url
            }
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
        
        
    def post(self):
        thesis = Thesis()
        thesis.year = self.request.get('year')
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = self.request.get('section')
        thesis.put()
        self.redirect('/home')


class APIThesisHandler(webapp2.RequestHandler):
    def get(self):
        thesises = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []
        for thesis in thesises:
            thesis_list.append({
                'id': thesis.key.urlsafe(),
                'year': thesis.year,
                'thesis_title': thesis.thesis_title,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section
                })
        response = {
            'result': 'OK',
            'data': thesis_list
            }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis = Thesis()
        thesis.year = int(self.request.get('year'))
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = int(self.request.get('section'))
        thesis.put()
        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result': 'OK',
            'data': {
                'id': thesis.key.urlsafe(),
                'year': thesis.year,
                'thesis_title': thesis.thesis_title,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section
            }
        }
        self.response.out.write(json.dumps(response));


class Success(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Success!')



app = webapp2.WSGIApplication([
    ('/api/thesis',APIThesisHandler),
    ('/home', MainPageHandler),
    ('/register', RegisterPageHandler),
    ('/login', LoginHandler),
    ('/', MainPageHandler),
    ('/success', Success)
   
], debug=True)
