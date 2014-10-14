from urllib import urlopen
import urllib2
import utils
import json
from bs4 import BeautifulSoup
from collections import defaultdict
import random
import test
import pickle
import stripper
# helpful function for processing keywords, mostly    
def getMultiples(items, key):
    values_list = ""
    if len(items) > 0:
        num_keys = 0
        for item in items:
            if num_keys == 0:
                values_list = item[key]                
            else:
                values_list =  "; ".join([values_list,item[key]])
            num_keys += 1
    return values_list

def parse_nyt():
	url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=stock+market+crash+&begin_date=20070101&end_date=20090101&api-key=318a69b2af97848f66071cb4c1fdc831:15:69992102" 
	response = urlopen(url).read()
	response = json.loads(response)
	print "Got response from nytimes"
	articleContent = []
	i = 0
	page = 1
	hits = response["response"]["meta"]["hits"]
	while i<51 and page<(hits/10):
		print 'Getting response for page',page
		url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=stock+market+crash+&begin_date=20070101&end_date=20090101&page="+str(page)+"&api-key=318a69b2af97848f66071cb4c1fdc831:15:69992102" 
		try:
			response = urlopen(url).read()
			response = json.loads(response)
			for article in response["response"]["docs"]:
				if random.randint(0,3) == 3: 								#1/3 probability
					print article["web_url"]
					soup1 = BeautifulSoup(test.getData(article["web_url"]))
					soup = soup1.findAll("p",{"itemprop": "articleBody"})
					if soup == None or len(soup) == 0:
						soup = soup1.find("div", {"id": "articleBody"})
						if soup!=None:
							soup = soup.findAll("p")
					if soup == None or len(soup)==0:
						soup = soup1.find("div", {"class": "articleBody"}) 
						if soup!=None:
							soup = soup.findAll("p")
					if soup!=None and len(soup)>0:
						if article["word_count"]>200 and article["lead_paragraph"]!=None:
							articleContent.append({})
							articleContent[i]["abstract"] = article["abstract"]
							articleContent[i]["pub_date"] = article["pub_date"]
							articleContent[i]["headline"] = article["headline"]["main"]
							articleContent[i]["keywords"] = article["keywords"]
							articleContent[i]["lead_paragraph"] = article["lead_paragraph"]
							articleContent[i]["web_url"] = article["web_url"]
							articleContent[i]["id"] = article["_id"]
							articleContent[i]["word_count"] = article["word_count"]
							keywords = ""
							keywords = getMultiples(article["keywords"],"value")
							# should probably pull these if/else checks into a module
							#	variables = [article["pub_date"], keywords, str(article["headline"]["main"]) if "main" in article["headline"].keys() else "", str(article["source"]) if "source" in article.keys() else "", str(article["document_type"]) if "document_type" in article.keys() else "", article["web_url"] if "web_url" in article.keys() else "",str(article["news_desk"]) if "news_desk" in article.keys() else "",str(article["section_name"]) if "section_name" in article.keys() else "",str(article["lead_paragraph"]).replace("\n","") if "lead_paragraph" in article.keys() else ""]
							#	line = "\t".join(variables)
							#	articleContent[i]["text"] = line
							sent = ""
							if type(soup) is not str:
								sent = " ".join([str(word) for word in soup])
							else:
								sent = soup
							articleContent[i]["text"] = stripper.strip(sent)
							print articleContent[i]["headline"],article["keywords"],article["lead_paragraph"]
							i+=1
							print 'Extracted',i,article["pub_date"]
							if i>51:
								break
		except:
			print "Skipped"
		page+=1

	print "Articles Extracted",i	
	return articleContent

def writePickle(struct, filename):
	file1 = open(filename,"wb") 			
	pickle.dump(struct,file1)
	file1.close()

articleContent = parse_nyt()
writePickle(articleContent,"stockmarketarticleContent.txt")

