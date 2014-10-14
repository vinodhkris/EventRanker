import cookielib
import urllib2
from bs4 import BeautifulSoup
'''
response = urllib2.urlopen('http://python.org/')
html = response.read()
'''
url = "http://www.nytimes.com/2008/12/28/books/review/Gross-t.html"
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
request = urllib2.Request(url)
response = opener.open(request)
print response.read()