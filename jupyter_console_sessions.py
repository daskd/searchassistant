# coding: utf-8
import cherrypy
import cherrypy
from google import google
num_page = 3
search_results = google.search("This is my query", num_page)
search_results
import json
import pprint as pp
get_ipython().magic(u'cd c:\\projects\\APKY\\PES601\\Project\\SearchAssistant\\resources\\GoogleSearchAPI\\google-api-python-client-master\\google-api-python-client-master\\samples\\customsearch')
get_ipython().magic(u'pwd ')
with open('out.json') as datfile:
    data = json.load(datfile)
    
get_ipython().magic(u'cd c:\\projects\\APKY\\PES601\\Project\\SearchAssistant\\searchassistant')
with open('out.json') as datfile:
    data = json.load(datfile)
with open('out2.json') as datfile:
    data = json.load(datfile)
with open('out3.json') as datfile:
    data = json.load(datfile)
with open('out2.json') as datfile:
    data = json.load(datfile)
with open('out4.json') as datfile:
    data = json.load(datfile)
with open('out4.json') as datfile:
    data = json.load(datfile)
with open('out4.json') as datfile:
    data = json.load(datfile)
get_ipython().magic(u'pwd ')
execfile('gsearchtest.py')
r = main()
r
r[0]
r.keys
r.keys()
r.items
r.items()
r.items.keys()
r['items']
r['items'].keys()
r['items'][0]
r['items'][1]
r['items'][0]
r['items'][1]
[x['title'] for x in r['items']]
get_ipython().magic(u'pinfo2 main')
execfile('gsearchtest.py')
execfile('gsearchtest.py')
r
[x['title'] for x in r['items']]
execfile('gsearchtest.py')
r = main()
r = main()
import pickle
output = open('result.pkl','wb')
pickle.dump(r, output)
output.close()
def pkl(o):
    with open('result.pkl','wb') as out:
        pickle.dump(o, out, -1)
        
pkl(r)
def upkl(file):
    with open(file, 'rb') as input:
        res = pickle.load(input)
    return res
rback = upkl('result.pkl')
rback
[x['title'] for x in rback['items']]
get_ipython().magic(u'hist -n')
