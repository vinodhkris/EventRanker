import json
import urllib2
import random

def get_json_response (url):
    response = urllib2.urlopen (url)
    response_string = response.read()
    js_object =  json.loads (response_string)
    return js_object

def get_nyt_article_search_url(params):
	url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?api-key="
	ARTICLE_SEARCH_API_KEY = ["318a69b2af97848f66071cb4c1fdc831:15:69992102", "353424482f2911b68847901e257ce797:18:69992139"]
	url += random.choice(ARTICLE_SEARCH_API_KEY)
	url += "&q="+params
	return url