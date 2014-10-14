from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_tfidf(docs):
	tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
	tfidf_matrix_train = tfidf_vectorizer.fit_transform(docs)  #finds the tfidf score with normalization
	return tfidf_matrix_train.todense()