import cookielib
import urllib2
from bs4 import BeautifulSoup
import pickle
'''
response = urllib2.urlopen('http://python.org/')
html = response.read()
'''
def getData(url):
	html = ""
	try:
		response = urllib2.urlopen(url)
		html = response.read()
	except:
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		request = urllib2.Request(url)
		response = opener.open(request)
		html = response.read()

	return html

def unpickle(filename):
	f = open(filename,"rb") 
	heroes = pickle.load(f)
	return heroes