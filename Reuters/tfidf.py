from nltk.tokenize import RegexpTokenizer
import numpy as np
import pickle
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import get_tfidf
stop = stopwords.words('english')

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

def ngrams(input, n):
  input = input.split(' ')
  output = {}
  for i in range(len(input)-n+1):
    g = ' '.join(input[i:i+n])
    output.setdefault(g, 0)
    output[g] += 1
  return output

def preprocess(article):
	tokens = tokenizer.tokenize(article)
	tokens_new = []
	lmtzr = PorterStemmer()
	for word in tokens:
		if word not in stop: 					#added stop words
			word = lmtzr.stem(word) 			#added stemming
			tokens_new.append(word)
	return tokens_new

filename = open("topicinfo.txt","r")
name = ''
for line in filename:
	name = line.split(" ")[0]
	break

print 'Running tfidf.py'
print 'Computing tfidf vector for unigrams and bigrams'
#ngrams('a a a a', 2) # {'a a': 3}
# Tokenizer for extracting words out of articles
tokenizer = RegexpTokenizer(r'\w+')

# docs = pickle.load(open('googlearticleContent.txt', 'rb'))
docs = pickle.load(open(name+'.txt', 'rb'))
# docs = pickle.load(open('hongKongProtests.txt', 'rb'))
#docs = pickle.load(open('soccerWorldCup.txt', 'rb'))
#docs = pickle.load(open('arabSpring.txt', 'rb'))

# List with a dictionary for each article. 
# Each dict contains the unqiue article words as key and number of occurences in the article as value
list_of_dics = []	

# Vocabulary is a dictionary with key value as unique ids and value as the word
vocabcount = 0			
vocab = {}		
wc_mat = get_tfidf.get_tfidf([doc['text'] for doc in docs])

writePickle(wc_mat,"tfidf_output/"+name+"_tfidf.txt")
#writePickle(wc_mat,"tfidf_output/arabSpring_tfidf.txt")
#writePickle(wc_mat,"tfidf_output/hongkongProtests_tfidf.txt")
#writePickle(wc_mat,"tfidf_output/stockMarkets_tfidf.txt")


