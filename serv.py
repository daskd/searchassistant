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




conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 8084)),
        },
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },

        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
        }

    }
cherrypy.quickstart(HelloWorld(), '/', config=conf)


