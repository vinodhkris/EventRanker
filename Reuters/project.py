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
from scipy.cluster.vq import *
import pylab
import datetime
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
import time
import pickle

def writePickle(struct, filename):
	file1 = open(filename,"wb") 			
	pickle.dump(struct,file1)
	file1.close()

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
print 'Extracting date and location for an article'
doctext = {}
docDate = {}
docLocation = {}

datePattern = re.compile("<date>(.*)</date>")
placesPattern = re.compile("<places><d>(.*)</d>*</places>")
places = []
mindate = 0
maxdate = 0
date1 = datetime.datetime(1985,1,1,0,0,0)
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
		date = datePattern.search(str(date)).groups()[0]
		doctime = date.split(' ')[1]
		date = date.split(' ')[0]
		month = monthtonum(date.split('-')[1])
		datenum = int(date.split('-')[0])
		year = int(date.split('-')[2])
		hour = int(doctime.split(":")[0])
		minute = int(doctime.split(":")[1])
		second = int(doctime.split(":")[2].split(".")[0])
		microsecond = int(doctime.split(":")[2].split(".")[1])
		c = datetime.datetime(year,month,datenum,hour,minute,second,microsecond) - date1
		doctext[doc]["date"] = int(c.total_seconds())
		if mindate == 0:
			mindate = doctext[doc]["date"]
		if doctext[doc]["date"]<mindate:
			mindate = doctext[doc]["date"]
		if doctext[doc]["date"]>maxdate:
			maxdate = doctext[doc]["date"]
		if placesPattern.search(str(word.findAll("places")[0]))!=None:
			doctext[doc]["places"] = placesPattern.search(str(word.findAll("places")[0])).groups()[0]
			if "</d>" in doctext[doc]["places"]:
				doctext[doc]["places"] = doctext[doc]["places"].split("</d>")[0]
		else:
			doctext[doc]["places"] = None

		if doctext[doc]["places"] not in places:
			places.append(doctext[doc]["places"])


print maxdate,mindate

#Part for extracting word tfidf vector for article

print 'Extracting tfidf vector for an article'
featureVector = np.zeros(shape=(max(docs)+1,18912))  					#Word vector, also added space for location and time and Person (if any)
csvfile = open('coffee_wc.csv','r')
read = csv.reader(csvfile, delimiter = ',')
for row in read:
	if int(row[0]) in docs:
		featureVector[int(row[0]),int(row[1])] += int(row[2]) 
'''
csvfile = open('coffee_tfidf.csv','r')
read = csv.reader(csvfile, delimiter = ',')
for row in read:
	featureVector[int(row[0]),int(row[1])] = float(row[2]) 
'''
'''
for doc in docs:
	featureVector[doc,18912] = places.index(doctext[doc]["places"])
	featureVector[doc,18913] = doctext[doc]["date"]
'''

#featureVector = featureVector.tocsr()
'''
for i in xrange(min(docs),max(docs)):
	print i,featureVector[i].data
raw_input()
'''
#Feature Vector extracted - Lets write the similarity formula

def similarity(featureVector,maxTimeDiff,doctext,doc1,doc2):
	location = 0
	featureVector1 = featureVector[doc1]
	featureVector2 = featureVector[doc2]
	print featureVector1
	jcSim = jaccard_similarity_score(featureVector1,featureVector2)
	if doctext[doc1]["places"] == doctext[doc2]["places"]:
		location+=1
	date = abs(int(doctext[doc1]["date"])- int(doctext[doc2]["date"]))
	w1 = 1 						#Weight for word vector
	w2 = 1 						#Weight for location
	w3 = 1 						#Weight for time distribution
	alpha = 1.0 				#Time decay
	sim = w1*jcSim+w2*location
	return sim*math.exp(-alpha*(date)/maxTimeDiff)

print 'Getting the similarity values between different articles'
startTime = time.time()
docssimilarity = np.ones(shape=(len(docs),len(docs)))  
mindoc = min(docs)
maxTimeDiff = maxdate - mindate
for docid1 in docs:
	for docid2 in docs:
		if docid1 == docid2:
			continue
		docssimilarity[docid1-mindoc][docid2-mindoc] = similarity(featureVector,maxTimeDiff,doctext,docid1,docid2)
		print docid1,docid2,docssimilarity[docid1-mindoc][docid2-mindoc]

writePickle(docssimilarity,'docSimilarityPickle.txt')

print docssimilarity

print 'Time elapsed',time.time()-startTime

#Kmeans with similarity
