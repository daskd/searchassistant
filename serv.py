import cherrypy
import os
import searchassistant


class HelloWorld(object):

    # Method
    test = searchassistant.Test()

    # Method
    @cherrypy.expose
    def index(self):
        return "Hello world!"




cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', 8084))})
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


