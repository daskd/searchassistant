import cherrypy
import urllib2
from googleapiclient.discovery import build
import pickle
import unicodedata
import json

# Globals
APIKEY = '54606e96f52a19e5d2f2258c637d8e98'
BASEURL = 'http://cognition-srv1.ouc.ac.cy/smart_corpus_builder/ws2/api.php'

class Test(object):
    
    @cherrypy.expose
    def index(self):
        return '<h1>Test!</h1>'
    
    @cherrypy.expose
    def testmethod(self, parameter):
        return '<h1>Parameter: {0}</h1>'.format(parameter)

    @cherrypy.expose
    def setdomaintest(self, rules):
        method = 'flash_set_rules'
        url = '{base}?api={apikey}&method={method}&flash_rules={rules}'.format(base = BASEURL, apikey = APIKEY, method = method, rules = rules) 

        return urllib2.quote(rules)


    @cherrypy.expose
    def querydomain(self, query, domainid):
        method = 'flash_run_query'
        urlcomposition = '{base}?api={apikey}&method={method}&flash_query={query}&domain_id={domainid}'
        query = urllib2.quote(query)
        url = urlcomposition.format(
            base = BASEURL, apikey = APIKEY, method = method, query = query, domainid = domainid) 
        response = urllib2.urlopen(url).read()
        print 'URL for querying domain: {0}'.format(url)
        print 'Response: {0}'.format(response)
        j = json.loads(response)
        result = j['output'][-2].replace('>>> conclusion: ', '').replace('[', '').replace(']', '')
        return result


    @cherrypy.expose
    def setdomain(self, rules):
        method = 'flash_set_rules'
        urlcomposition = '{base}?api={apikey}&method={method}&flash_rules={rules}'
        rules = urllib2.quote(rules)
        url = urlcomposition.format(
            base = BASEURL, apikey = APIKEY, method = method, rules = rules) 
        print 'URL for setting domain: ' + url
        id = urllib2.urlopen(url).read()
        return id


    @cherrypy.expose
    def getsearchresultsashtml(self, query):
        results = self.getgoogleresultsmocked(query)
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
