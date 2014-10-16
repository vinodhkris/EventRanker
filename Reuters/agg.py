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
filename = open("topicinfo.txt","r")
name = ''
for line in filename:
	name = line.split(" ")[0]
	K = int(line.split(" ")[1])
	break

#docssimilarity = pickle.load(open('DocSim/swc_docSimilarity.txt', 'rb'))
docssimilarity = pickle.load(open('DocSim/'+name+'_docSimilarity.txt', 'rb'))
#docssimilarity = pickle.load(open('DocSim/swc_docSimilarity.txt', 'rb'))
#docssimilarity = pickle.load(open('DocSim/swc_docSimilarity.txt', 'rb'))
#docssimilarity = pickle.load(open('DocSim/swc_docSimilarity.txt', 'rb'))

articleContent = pickle.load(open(name+'.txt','rb'))

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


#Top events - Graph construction
def GraphFormation( clusters, clusterDistance ):
	
	G=nx.Graph()
#	print clusters[1][1]
	for i in clusters:
	#	print events
		G.add_node(i)
	
	#print G.nodes()
	
	for i in clusters:
		for j in clusters:
			if i!=j:
				G.add_weighted_edges_from([(i,j,clusterDistance[(i,j)])]) 
	#print G.edges()
	
	
	return G
	
G=GraphFormation(clusters,clusterDistance)
pr =nx.pagerank(G,alpha=0.9,weight='weight')
pr = sorted(pr.items(), key=operator.itemgetter(1),reverse=True)
degree = sorted(G.degree(weight='weight').items(),key=operator.itemgetter(1),reverse=True)	

#print G.degree(0)
pos=nx.spring_layout(G)
#pylab.figure(2)
nx.draw(G,pos)
# specifiy edge labels explicitly
edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
#plt.show()


#Printing cluster info
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
	print '\nCluster',i
	for j in xrange(len(clusters[i])):
	#	print i,clusters[i][j],articleContent[clusters[i][j]]['headline'],articleContent[clusters[i][j]]['pub_date']
	#	print articleContent[clusters[i][j]]['keywords']

		headline = articleContent[clusters[i][j]]['headline']
		if articleContent[clusters[i][j]]["lead_paragraph"] is not None:
		#	print 'here'
			headline = headline + ' ' +articleContent[clusters[i][j]]["lead_paragraph"]
		headline = stripper.strip(headline)
	#	print headline
		for word in headline.split(' '):
			wordCount[i][word]+=1
	#	print wordCount[i]
		keywords = articleContent[clusters[i][j]]['keywords']

		for x in xrange(len(keywords)):
			if keywords[x]["name"] == "persons":
				personCount[i][keywords[x]["value"]]+=1
			if keywords[x]["name"] == "glocations":
				locCount[i][keywords[x]["value"]]+=1
			if keywords[x]["name"] == "organizations":
				orgCount[i][keywords[x]["value"]]+=1


for i in clusters:
	sorted_x = sorted(wordCount[i].items(), key=operator.itemgetter(1),reverse=True)
	sorted_person =  sorted(personCount[i].items(), key=operator.itemgetter(1),reverse=True)
	sortedLocation =  sorted(locCount[i].items(), key=operator.itemgetter(1),reverse=True)
	sortedOrg =  sorted(orgCount[i].items(), key=operator.itemgetter(1),reverse=True)
	'''
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
	'''
#print new_cluster

print 'Top 5 events according to Page rank'
for i in xrange(5):
	print i,pr[i]
print '\nTop 5 events according to degree'
for i in xrange(5):
	print i,degree[i],'\n'
	for j in xrange(len(clusters[degree[i][0]])):
		print articleContent[clusters[degree[i][0]][j]]['headline']
	print '\n'
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

	print '\n\n'
