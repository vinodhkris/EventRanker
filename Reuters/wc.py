from nltk.tokenize import RegexpTokenizer
import numpy as np
import pickle
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

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

print 'Running wc.py'
print 'Computing word count vector for unigrams and bigrams'
#ngrams('a a a a', 2) # {'a a': 3}
# Tokenizer for extracting words out of articles
tokenizer = RegexpTokenizer(r'\w+')

# docs = pickle.load(open('googlearticleContent.txt', 'rb'))
docs = pickle.load(open('soccerWorldCup.txt', 'rb'))
# docs = pickle.load(open('hongKongProtests.txt', 'rb'))
#docs = pickle.load(open('soccerWorldCup.txt', 'rb'))
# docs = pickle.load(open('arabSpring.txt', 'rb'))

# List with a dictionary for each article. 
# Each dict contains the unqiue article words as key and number of occurences in the article as value
list_of_dics = []	

# Vocabulary is a dictionary with key value as unique ids and value as the word
vocabcount = 0			
vocab = {}						
for doc in docs:
	#unigrams
	#tokens = tokenizer.tokenize(doc['text'])
	tokens = preprocess(doc['text'])
	dic = {}
	for token in tokens:
		if token not in dic:
			dic[token] = 1
		else:
			dic[token] += 1

	 	if token not in vocab:
	 		vocab[vocabcount] = token
	 		vocabcount += 1

	 #bigrams
	bi_dic = ngrams(doc['text'], 2) # {'a a': 3}

	for word in bi_dic:
		vocab[vocabcount] = word
	 	vocabcount += 1

	final_dic = dict(dic.items() + bi_dic.items())
	list_of_dics.append(final_dic)
	
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

writePickle(wc_mat,"WC_output/soccerWorldCup_wc.txt")



