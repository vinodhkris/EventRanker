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
import stripper

def writePickle(struct, filename):
	file1 = open(filename,"wb") 			
	pickle.dump(struct,file1)
	file1.close()

def unpickle(filename):
	f = open(filename,"rb") 
	heroes = pickle.load(f)
	return heroes
#Part for extracting word tfidf vector for article
print 'Running project_new.py'
print 'Extracting word count vector for an article'

featureVector = unpickle('WC_output/hongKongProtests_wc.txt')
articleContent = unpickle('hongKongProtests.txt')

featureVector = np.transpose(featureVector)#featureVector.todense()


#Feature Vector extracted - Lets write the similarity formula

def similarity(featureVector,doc1,doc2):
	global articleContent
	location = 0
	person = 0
	organization = 0

	#Extracting word vector - unigrams and bigrams (from wc.py)
	featureVector1 = featureVector[doc1]
	featureVector2 = featureVector[doc2]
	
	#Finding time difference between the 2 articles
	try:
		try:
			if "pub_date" in articleContent[doc1] and "pub_date" in articleContent[doc2] and len(articleContent[doc1]["pub_date"].split("-"))>0 and len(articleContent[doc2]["pub_date"].split("-"))>0:
				year = articleContent[doc1]["pub_date"].split("-")[0]
				month = articleContent[doc1]["pub_date"].split("-")[1]
				day = articleContent[doc1]["pub_date"].split("-")[2].split("T")[0]
				datetime1 = datetime.datetime(int(year),int(month),int(day))

				year = articleContent[doc2]["pub_date"].split("-")[0]
				month = articleContent[doc2]["pub_date"].split("-")[1]
				day = articleContent[doc2]["pub_date"].split("-")[2].split("T")[0]
				datetime2 = datetime.datetime(int(year),int(month),int(day))
			else:
				datetime1 = (1,1,1)
				datetime2 = (1,1,1)
		except:
			datetime1 = (1,1,1)
			datetime2 = (1,1,1)
		#jcSim = jaccard_similarity_score(featureVector1,featureVector2)
		cosineSim = cosine_similarity(featureVector1,featureVector2)
		#Extracting person, location, organization features
		person1 = []
		location1 = []
		organization1 = []
		person2 = []
		location2 = []
		organization2 = []
		for i in xrange(len(articleContent[doc1]["keywords"])):
			if articleContent[doc1]["keywords"][i]["name"] == "persons":
				person1.append(stripper.strip(articleContent[doc1]["keywords"][i]["value"]))
			if articleContent[doc1]["keywords"][i]["name"] == "glocations":
				location1.append(stripper.strip(articleContent[doc1]["keywords"][i]["value"]))
			if articleContent[doc1]["keywords"][i]["name"] == "organizations":
				organization1.append(stripper.strip(articleContent[doc1]["keywords"][i]["value"]))

		for i in xrange(len(articleContent[doc2]["keywords"])):
			if articleContent[doc2]["keywords"][i]["name"] == "persons":
				person2.append(stripper.strip(articleContent[doc2]["keywords"][i]["value"]))
			if articleContent[doc2]["keywords"][i]["name"] == "glocations":
				location2.append(stripper.strip(articleContent[doc2]["keywords"][i]["value"]))
			if articleContent[doc2]["keywords"][i]["name"] == "organizations":
				organization2.append(stripper.strip(articleContent[doc2]["keywords"][i]["value"])	)

		person += len(set(person1).intersection(person2))
		location += len(set(location1).intersection(location2))
		organization+= len(set(organization1).intersection(organization2))

		date = datetime1 - datetime2
		date = date.days
		w_word = 2						#Weight for word vector
		w_person = 1 						#Weight for person
		w_location = 2 						#Weight for location
		w_org = 2						#Weight for organization
		alpha = 1.0 				#Time decay
		sim = w_word*cosineSim+w_person*person+w_location*location+w_org*organization
		return sim*math.exp(-alpha*(date)/50)
	except:
		return 0.0
print 'Getting the similarity values between different articles'
startTime = time.time()
numdocs = featureVector.shape[0]
docssimilarity = np.ones(shape=(numdocs,numdocs))  
for i in xrange(numdocs-1):
	for j in xrange(numdocs-1):
		if i == j:
			continue
		docssimilarity[i][j] = similarity(featureVector,i,j)

writePickle(docssimilarity,'DocSim/hk_docSimilarity.txt')

print docssimilarity

print 'Time elapsed',time.time()-startTime

#agglomerative clustering with similarity
