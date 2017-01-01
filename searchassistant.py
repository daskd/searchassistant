import cherrypy
import urllib2
from googleapiclient.discovery import build
import pickle
import unicodedata

class Test(object):
    
    @cherrypy.expose
    def index(self):
        return '<h1>Test!</h1>'
    
    @cherrypy.expose
    def testmethod(self, parameter):
        return '<h1>Parameter: {0}</h1>'.format(parameter)

    def gettestsearch(self):
        testquery = 'test something bro'
        return self.getsearch(testquery)

    @cherrypy.expose
    def getsearchresultsashtml(self, query):
        results = self.getgoogleresults(query)
        resultview = [(x['title'], x['link'], x['htmlSnippet']) for x in results['items']]

        with open('template.html') as templatefile:
            template = templatefile.read()

        # now format as html
        html = 'Keywords used for querying: <br/>{0}<br/><br/>'.format(query)
        for (title, url, description) in resultview:
            title       = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
            url         = unicodedata.normalize('NFKD', url).encode('ascii','ignore')
            description = unicodedata.normalize('NFKD', description).encode('ascii','ignore')
            html += template.format(url=url, title=title, description=description)

        return html


    def getgoogleresultsmocked(self, query):
        '''
        The Mock function .
        Just to avoid hittimg the limit of 100 queries on google's free search.
        '''
        return self.upkl('result.pkl')


    def getgoogleresults(self, query):
        ''' 
        The Real Function.
        Returns dictionary of Google results, 
        by calling Google's Custom Search Engine API.
        This API is a new thing, as Google's now controlling calls to google.com
        and you can't now just call its url and get results.
        By using the API you can have up to 100 free search requests per day.
        
        '''
        apikey = 'AIzaSyDMKhd-jsTLFlII7bjfxpRMDSn8_VHkRmE'
        searchengineid = '017618634140051690802:9hr8vphns8k'
        service = build('customsearch', 'v1', developerKey=apikey)
        res = service.cse().list( q=query, cx=searchengineid ).execute()
        return res

    # unused
    def getpagecontent(self,url):
        response = urllib2.urlopen(url)
        html = response.read()
        return html



    def upkl(self, file):
        with open(file, 'rb') as input:
            res = pickle.load(input)
        return res
