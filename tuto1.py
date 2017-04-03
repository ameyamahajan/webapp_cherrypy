import cherrypy


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def multiple(self):
        return '<title> Hello </title> <h1> Ameya first Cherry Pie Web App</h1>' 

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
