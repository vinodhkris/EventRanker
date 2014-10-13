import numpy as np
import pickle
import random

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

docssimilarity = pickle.load(open('docSimilarityPickle.txt', 'rb'))
numdocs = docssimilarity.shape[0]

k = 3
kmeans = random.sample(docs, k)
# kmeans = [7126, 7187, 7089]
print kmeans

classes = np.zeros(numdocs, dtype=np.int)

# 100 iterations of kmeans
for iter in xrange(100):
	# Find class memebership of each doc
	for docid in docs:
		sim = []
		for kid in kmeans:
			sim.append(docssimilarity[docid-mindoc][kid-mindoc])
		maxindex = sim.index(max(sim))
		classes[docid-mindoc] = maxindex
	print classes

	# Compute mean similarity scores for k clusters
	summeans = np.zeros(k)
	countmeans = np.zeros(k, dtype=np.int)
	for doc in docs:
		docclass = classes[doc-mindoc]
		summeans[docclass] += docssimilarity[kmeans[docclass]-mindoc][doc-mindoc]
		countmeans[docclass] += 1

	if(not np.all(countmeans)):
		print "\n\n****Locha!****\nOne or more classes have no members:"
		print countmeans 
		break

	meansims = summeans/countmeans
	print summeans
	print countmeans
	print meansims

	# Find the k docs with similarity scores closest to the new means
	# firstrow = docssimilarity[0,:]
	for i in xrange(k):
		baseline = docssimilarity[kmeans[i]-mindoc,:]
		diff = np.absolute(baseline - meansims[i])
		# print diff
		meandocid = np.argmin(diff) + mindoc
		kmeans[i] = meandocid

	print kmeans
