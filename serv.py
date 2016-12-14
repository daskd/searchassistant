import cherrypy
import os


class HelloWorld(object):

    @cherrypy.expose
    def index(self):
        return "Hello world!"


cherrypy.config.update({'server.socket_port': 8084})
conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },

        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }

    }
cherrypy.quickstart(HelloWorld(), '/', conf)


