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

def unpickle(filename):
	f = open(filename,"rb") 
	heroes = pickle.load(f)
	return heroes
#Part for extracting word tfidf vector for article

print 'Extracting word count vector for an article'

featureVector = unpickle('stockmarketarticleContent_wc.txt')
articleContent = unpickle('stockmarketarticleContent.txt')

featureVector = np.transpose(featureVector)


#Feature Vector extracted - Lets write the similarity formula

def similarity(featureVector,doc1,doc2):
	global articleContent
	location = 0
	featureVector1 = featureVector[doc1]
	featureVector2 = featureVector[doc2]
	
	year = articleContent[doc1]["pub_date"].split("-")[0]
	month = articleContent[doc1]["pub_date"].split("-")[1]
	day = articleContent[doc1]["pub_date"].split("-")[2].split("T")[0]
	datetime1 = datetime.datetime(int(year),int(month),int(day))

	year = articleContent[doc2]["pub_date"].split("-")[0]
	month = articleContent[doc2]["pub_date"].split("-")[1]
	day = articleContent[doc2]["pub_date"].split("-")[2].split("T")[0]
	datetime2 = datetime.datetime(int(year),int(month),int(day))

	jcSim = jaccard_similarity_score(featureVector1,featureVector2)
#	if doctext[doc1]["places"] == doctext[doc2]["places"]:
#		location+=1
	date = datetime1 - datetime2
	date = date.days
	w1 = 1 						#Weight for word vector
	w2 = 1 						#Weight for location
	w3 = 1 						#Weight for time distribution
	alpha = 1.0 				#Time decay
	sim = w1*jcSim
	return sim*math.exp(-alpha*(date)/730)

print 'Getting the similarity values between different articles'
startTime = time.time()
numdocs = featureVector.shape[0]
docssimilarity = np.ones(shape=(numdocs,numdocs))  
for i in xrange(numdocs):
	for j in xrange(numdocs):
		if i == j:
			continue
		docssimilarity[i][j] = similarity(featureVector,i,j)
		print i,j,docssimilarity[i][j]

writePickle(docssimilarity,'docSimilarityPickle.txt')

print docssimilarity

print 'Time elapsed',time.time()-startTime

#agglomerative clustering with similarity
