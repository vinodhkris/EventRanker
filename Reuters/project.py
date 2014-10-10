from __future__ import division
from bs4 import BeautifulSoup
import csv
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
from sklearn.metrics import jaccard_similarity_score
from sklearn.metrics.pairwise import cosine_similarity
import math
import re


def monthtonum(month):
	if month.lower() == "jan":
		return 1
	elif month.lower() == "feb":
		return 2
	elif month.lower() == "mar":
		return 3
	elif month.lower() == "apr":
		return 4
	elif month.lower() == "may":
		return 5
	elif month.lower() == "jun":
		return 6
	elif month.lower() == "jul":
		return 7
	elif month.lower() == "aug":
		return 8
	elif month.lower() == "sep":
		return 9
	elif month.lower() == "oct":
		return 10
	elif month.lower() == "nov":
		return 11

	elif month.lower() == "dec":
		return 12

topics = open('Topics.txt','r')

inputTopic = 9
for line in topics:
	if int(line.split('\t')[0]) == inputTopic:
		filename = line.split('\t')[1]

listOfDocs = open(filename+'.txt','r')
docs = []

for doc in listOfDocs:
	docs.append(int(doc))
	print doc

#Part for extracting date and location for an article
doctext = {}
docDate = {}
docLocation = {}

datePattern = re.compile("<date>(.*)</date>")
placesPattern = re.compile("<places><d>(.*)</d>*</places>")
for doc in docs:
	num = int(doc/1000)
	if num<10:
		filename = 'reut2-00'+str(num)+'.sgm'
	else:
		filename = 'reut2-0'+str(num)+'.sgm'

	soup = BeautifulSoup(open('reuters21578original/'+filename))
	doctext[doc] = {}
	for word in soup.findAll("reuters",{"newid":str(doc)}):
		doctext[doc]["text"] = word.findAll("text")
		date = word.findAll("date")
		print 'date',date
		date = datePattern.search(str(date)).groups()[0]
		date = date.split(' ')[0]
		month = monthtonum(date.split('-')[1])
		datenum = int(date.split('-')[0])
		year = int(date.split('-')[2])
		months = year*12+month-1 	
		date = months*30 + datenum 							#For days
		doctext[doc]["date"] = date
		if placesPattern.search(str(word.findAll("places")[0]))!=None:
			doctext[doc]["places"] = placesPattern.search(str(word.findAll("places")[0])).groups()[0]
			if "</d>" in doctext[doc]["places"]:
				doctext[doc]["places"] = doctext[doc]["places"].split("</d>")[0]
		else:
			doctext[doc]["places"] = None


#Part for extracting word tfidf vector for article

featureVector = lil_matrix((max(docs)+1,18914))  					#Word vector, also added space for location and time and Person (if any)
csvfile = open('coffee_tfidf.csv','r')
read = csv.reader(csvfile, delimiter = ',')
for row in read:
	featureVector[int(row[0]),int(row[1])] = float(row[2]) 

for doc in docs:
	featureVector[doc,18912] = doctext[doc]["places"]
	featureVector[doc,18913] = doctext[doc]["date"]


featureVector = featureVector.tocsr()
for i in xrange(min(docs),max(docs)):
	print i,featureVector[i].data

#Feature Vector extracted - Lets write the similarity formula

def similarity(featureVector1,featureVector2,maxTimeDiff):
	jcSim = jaccard_similarity_score(featureVector1[:-2],featureVector2[:-2])
	if featureVector1[-2] == featureVector2[-2]:
		location+=1
	date = abs(featureVector1[-1] - featureVector2[-1])
	w1 = 1 						#Weight for word vector
	w2 = 1 						#Weight for location
	w3 = 1 						#Weight for time distribution
	alpha = 1.0 				#Time decay
	sim = w1*jcSim+w2*location
	return sim*math.exp(-alpha*(date)/maxTimeDiff)


#K means with similarity vector
