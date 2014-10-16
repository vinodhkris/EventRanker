from __future__ import division
from collections import defaultdict
import operator
import numpy as np
import pickle
import random
import networkx as nx
import matplotlib.pyplot as plt
import stripper
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
def writePickle(struct, filename):
	file1 = open(filename,"wb") 			
	pickle.dump(struct,file1)
	file1.close()

print 'Running agg.py'
print 'Clustering the articles based on features extracted in project_new.py'
K = 10
docssimilarity = pickle.load(open('DocSim/swc_docSimilarity.txt', 'rb'))
articleContent = pickle.load(open('soccerWorldCup.txt','rb'))
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

def GraphFormation( clusters, clusterDistance ):
	
	G=nx.Graph()
#	print clusters[1][1]
	for i in clusters:
	#	print events
		G.add_node(i)
	
	print G.nodes()
	
	for i in clusters:
		for j in clusters:
			if i!=j:
				G.add_weighted_edges_from([(i,j,clusterDistance[(i,j)])]) 
	print G.edges()
	
	
	return G
	
	
G=GraphFormation(clusters,clusterDistance)
pr =nx.pagerank(G,alpha=0.9,weight='weight')
print pr
print sorted(G.degree(weight='weight').values())
#print G.degree(0)
pos=nx.spring_layout(G)
#pylab.figure(2)
nx.draw(G,pos)
# specifiy edge labels explicitly


edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
'''labels={}
labels[0]=r'$1$'
labels[1]=r'$2$'
labels[2]=r'$3$'
labels[3]=r'$4$'
labels[4]=r'$5$'
nx.draw_networkx_labels(G,pos,labels,font_size=16)
# show graphs
'''
#plt.show()

new_cluster = {}
num = 0
for word in clusters:
	new_cluster[num] = clusters[word]
	num+=1
writePickle(new_cluster,'new_cluster.txt')

wordCount = {}
orgCount = {}
personCount = {}
locCount = {}
for i in clusters:
	wordCount[i] = defaultdict(int)
	personCount[i] = defaultdict(int)
	orgCount[i] = defaultdict(int)
	locCount[i] = defaultdict(int)

	for j in xrange(len(clusters[i])):
		print i,clusters[i][j],articleContent[clusters[i][j]]['headline'],articleContent[clusters[i][j]]['pub_date']
		print articleContent[clusters[i][j]]['keywords']

		headline = articleContent[clusters[i][j]]['headline']
		if articleContent[clusters[i][j]]["lead_paragraph"] is not None:
			print 'here'
			headline = headline + ' ' +articleContent[clusters[i][j]]["lead_paragraph"]
		headline = stripper.strip(headline)
		for word in headline.split(' '):
			wordCount[i][word]+=1

		keywords = articleContent[clusters[i][j]]['keywords']

		for x in xrange(len(keywords)):
			if keywords[x]["name"] == "persons":
				personCount[i][keywords[x]["value"]]+=1
			if keywords[x]["name"] == "glocations":
				locCount[i][keywords[x]["value"]]+=1
			if keywords[x]["name"] == "organizations":
				orgCount[i][keywords[x]["value"]]+=1


for i in clusters:
	sorted_x = sorted(wordCount[i].items(), key=operator.itemgetter(1))
	sorted_person =  sorted(personCount[i].items(), key=operator.itemgetter(1))
	sortedLocation =  sorted(locCount[i].items(), key=operator.itemgetter(1))
	sortedOrg =  sorted(orgCount[i].items(), key=operator.itemgetter(1))
	print '\nCluster',i,'labels'
	for j in xrange(5):
		if j <len(sorted_x):
			print sorted_x[j]

	print 'Top 3 persons'
	for j in xrange(3):
		if j <len(sorted_person):
			print sorted_person[j]

	print 'Top 3 locs'
	for j in xrange(3):
		if j <len(sortedLocation):
			print sortedLocation[j]

	print 'Top 3 orgs'
	for j in xrange(3):
		if j <len(sortedOrg):
			print sortedOrg[j]

