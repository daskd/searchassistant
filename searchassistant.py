import cherrypy
import urllib2
from googleapiclient.discovery import build
import pickle
import unicodedata
import json
import re

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

        # extracting entities from conclusion
        #result = j['output'][-2].replace('>>> conclusion: ', '').replace('[', '').replace(']', '')

        # dbg: show conclusion line as is returned
        result = j['output'][-2]

        # dbg: the below is formatting just for debugging output
        result = result.replace(',', ', ')


        ''' 
        the result = j['output'][-2].replace(',', ', ') above, is of the form:

        conclusion: [eat, with(manolis), search(vegeterian), search(wine), is_a(manolis, vegeterian), 
        is_a(vegeterian, foodcategory), is_a(wine, food), likes(manolis, wine)]
        
        '''
        
        # dev: return json with Submisison status, final conclusion, intermediate conclusions
        # collecting them below:

        # Status: if succeeded then result should contain the word 'conclusion'
        status = 'SUCCESS' if bool(re.search('conclusion', result)) else 'FAIL'

        # final conclusion: We expect from Flash to respond by wrapping its onclusions 
        # into a search(<keyword>) predicate
        searchadditions = re.findall('search\((\w+)\)', result) # this returns e.g. ['vegetarian', 'wine']
        # and into a remove(<keyword>) predicate
        searchremovals = self.extractremovals(result) # this returns e.g. ['with(manolis)']

        # Intermediate conclusions: Any other thing contained in the result except the initial query and the additions
        initialquery = self.splitfirstlevel(urllib2.unquote(query).replace(' ', ''))
        cleanresult = result.replace('>>> conclusion:', '').replace('[', '').replace(']', '').replace(' ', '')
        allconclusions = self.splitfirstlevel(cleanresult)
        
        # The below are different from the above 'searchadditions' & 'searchremovals' variables
        # in that they look for the whole 'search(word)' string, while the above pick the 'word' inside the 'search(word)'
        # (Could this be done more elegantly ?)
        additions = re.findall('search\(\w+\)', result.replace(' ', ''))
        removals = ['remove(%s)' % x for x in searchremovals]

        intermediate = list(set(allconclusions) - set(initialquery) - set(additions) - set(removals))

        assistantsquery = list((set(initialquery) | set(searchadditions)) - set(searchremovals))

        completeoutput = {}
        completeoutput['status'] = status;
        completeoutput['initialquery'] = initialquery
        completeoutput['intermediateconclusions'] = intermediate
        completeoutput['searchadditions'] = searchadditions
        completeoutput['searchremovals'] = searchremovals
        completeoutput['assistantsquery'] = assistantsquery
        
        #import ipdb;ipdb.set_trace()

        outputstr = str(completeoutput)
        # replace pythons descriptor for unicode: it adds a u before the string quote
        outputstr = outputstr.replace('[u\'', '[\'').replace(', u\'', ', \'').replace(',u\'', ',\'')
        # replace all single quotes with double (the string comes from a dict so all strings are enclosed by single quotes
        outputstr = outputstr.replace('\'', '"')

        return str(outputstr)


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



    # Utility functions

    # unused
    def getpagecontent(self,url):
        response = urllib2.urlopen(url)
        html = response.read()
        return html


    # Unpickle
    def upkl(self, file):
        with open(file, 'rb') as input:
            res = pickle.load(input)
        return res

    # Parse predicates
    def splitfirstlevel(self, text, delimiter = ',', ignoreifinside = ['(', ')']):
        itemlist = []
        curitem = ''
        openparenthesis = 0
        for i in range(len(text)):
            if text[i] == ignoreifinside[0]:
                openparenthesis += 1
            if text[i] == ignoreifinside[1]:
                openparenthesis -= 1
            if text[i] != delimiter or (text[i] == delimiter and openparenthesis != 0):
                curitem += text[i]
            elif openparenthesis == 0:
                itemlist.append(curitem.strip())
                curitem = ''
        if curitem != '':
            itemlist.append(curitem.strip())
        return itemlist
        
    def extractremovals(self, text):
        pos = text.find('remove')
        result = []
        while pos > -1:
            result.append(self.extractcontentuntilendofparenthesis(text[pos:]))
            pos = text.find('remove', pos + 1)
        return result

    def extractcontentuntilendofparenthesis(self, text):
        extractedtext = ''
        openparenthesis = 0
        for i in range(len(text)):
            currletter = text[i]
            if currletter == ')':
                openparenthesis -= 1
            if openparenthesis >= 1:
                extractedtext += currletter
            if currletter == '(':
                openparenthesis += 1
            if extractedtext != '' and openparenthesis == 0:
              result = extractedtext
              break
        return result

