from __future__ import division
from collections import defaultdict
import operator
import numpy as np
import pickle
import random
'''
topics = open('Topics.txt','r')

inputTopic = 9
for line in topics:
	if int(line.split('\t')[0]) == inputTopic:
		filename = line.split('\t')[1]

listOfDocs = open(filename+'.txt','r')
docs = []

for doc in listOfDocs:
	docs.append(int(doc))

mindoc = min(docs)
'''
print 'Running agg.py'
print 'Clustering the articles based on features extracted in project_new.py'
K = 20
docssimilarity = pickle.load(open('DocSim/hk_docSimilarity.txt', 'rb'))
articleContent = pickle.load(open('hongKongProtests.txt','rb'))
numdocs = docssimilarity.shape[0]

clusters = {}
for i in xrange(numdocs):
	clusters[i] = [i]

def clusterSim(c1,c2):
	similarities = []
	for i in c1:
		for j in c2:
			similarities.append(docssimilarity[i][j])
	return sum(similarities)/len(similarities)

def merge(cTuple):
	global clusters
	for j in clusters[cTuple[1]]:
		clusters[cTuple[0]].append(j)
	del clusters[cTuple[1]]

while len(clusters)>K: 								#Stopping criterion
	clusterDistance = defaultdict(float) 			#To store cluster distances
	for i in clusters:
		for j in clusters:
			if i!=j:
				clusterDistance[(i,j)] = clusterSim(clusters[i],clusters[j]) 	#Cluster similarity for each cluster (using average)

	clusters_to_merge = max(clusterDistance.iteritems(), key=operator.itemgetter(1))[0] 		#Returns cluster keys that are most similar to each other in this iteration
	merge(clusters_to_merge) 				#Merges the 2 clusters and deletes the second

print clusters

for i in clusters:
	for j in xrange(len(clusters[i])):
		print i,clusters[i][j],articleContent[clusters[i][j]]['headline'],articleContent[clusters[i][j]]['pub_date']
		print articleContent[clusters[i][j]]['keywords']
		raw_input()
