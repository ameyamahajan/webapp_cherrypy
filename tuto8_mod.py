import os, os.path
import random
import string

import cherrypy
import time 

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index_mod.html')


@cherrypy.expose
class StringGeneratorWebService(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        if not cherrypy.session.get('mystring'):
            return "GET response needs a parameter my_string"
        return cherrypy.session['mystring']

    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    def DELETE(self):
        cherrypy.session.pop('mystring', None)

@cherrypy.expose
class Check():
   @cherrypy.tools.accept(media='text/plain')
   def GET(self):
       return open('foo.html')

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/check': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    webapp.check = Check()
    cherrypy.quickstart(webapp, '/', conf)
