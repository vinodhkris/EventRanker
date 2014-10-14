from nltk.tokenize import RegexpTokenizer
import numpy as np
import pickle

#################################################################################
#																				#
# Input : Pickled article content text file from a topic 						#
# Output : Pickled word count matrix of dimensions (vocabsize x articlecount)	#
#																				#
#################################################################################

def writePickle(struct, filename):
	file1 = open(filename,"wb") 			
	pickle.dump(struct,file1)
	file1.close()


# Tokenizer for extracting words out of articles
tokenizer = RegexpTokenizer(r'\w+')

# docs = pickle.load(open('googlearticleContent.txt', 'rb'))
# docs = pickle.load(open('stockmarketarticleContent.txt', 'rb'))
# docs = pickle.load(open('hongKongProtests.txt', 'rb'))
docs = pickle.load(open('soccerWorldCup.txt', 'rb'))
# docs = pickle.load(open('arabSpring.txt', 'rb'))

# List with a dictionary for each article. 
# Each dict contains the unqiue article words as key and number of occurences in the article as value
list_of_dics = []	

# Vocabulary is a dictionary with key value as unique ids and value as the word
vocabcount = 0			
vocab = {}						

for doc in docs:
	tokens = tokenizer.tokenize(doc['text'])
	dic = {}
	for token in tokens:
		if token not in dic:
			dic[token] = 1
		else:
			dic[token] += 1

	 	if token not in vocab:
	 		vocab[vocabcount] = token
	 		vocabcount += 1

	list_of_dics.append(dic)
	
# Word count matrix with rows = vocab size & columns = articles
wc_mat = np.zeros((vocabcount, len(docs)))

# Fill every column of the word count matrix
doccount = 0
for doc in docs:
	for index in vocab.keys():
		word = vocab[index]
		if word in list_of_dics[doccount]:
			wc_mat[index][doccount] = list_of_dics[doccount][word]
	doccount += 1

writePickle(wc_mat,"soccerWorldCup_wc.txt")



