import cherrypy
import urllib2


class Test(object):
    
    @cherrypy.expose
    def index(self):
        return '<h1>Test!</h1>'

    def gettestsearch(self):
        testquery = 'test something bro'
        return self.getsearch(testquery)

    def getsearch(self, query):
        basesearchurl = 'http://www.google.com/?q='
        searchurl = basesearchurl + urllib2.quote(query)
        return self.getpagecontent(searchurl)

    def getpagecontent(self,url):
        response = urllib2.urlopen(url)
        html = response.read()
        return html


