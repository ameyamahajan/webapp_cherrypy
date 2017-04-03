import os, os.path
import random
import string

import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')


class StringGeneratorWebService(object):
    expose=True
    @cherrypy.tools.accept(media='text/plain')
    
    @cherrypy.expose
    def GET(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    @cherrypy.expose
    def PUT(self, another_string):
        cherrypy.session['mystring'] = another_string

    @cherrypy.expose
    def DELETE(self):
        cherrypy.session.pop('mystring', None)

class BannerRunner(object):
    expose=True
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.expose 
    def GET(self):
        return "Shit happends :("


if __name__ == '__main__':
    cherrypy.log("Here in Main")
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        },
        '/banner':{
	    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]	
	},
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    webapp.banner = BannerRunner() 
    cherrypy.quickstart(webapp, '/', conf)
