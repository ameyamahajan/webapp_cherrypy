import os, os.path
import random
import string
import shutil
import cherrypy


class StringGenerator(object):
    expose = True
    @cherrypy.expose
    def index(self):
        return open('upload.html')


@cherrypy.expose
class StringGeneratorWebService(object):
    expose = True
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
class Uploader():
    def POST(self, input_file=None):
        print("--"*5 +input_file + "--"*5)
	print(type(input_file))
        f = open('XYZZ','wb')
        with open(input_file) as inf:
            f.write(inf)
	return input_file 


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
        '/upload': {
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
    webapp.upload = Uploader()
    cherrypy.quickstart(webapp, '/', conf)
