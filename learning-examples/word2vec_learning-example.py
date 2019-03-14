from gensim.models import Word2Vec

# load the model (file "wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10" in home/common/word2vec/models)
model = Word2Vec.load("/Users/alinabaranova/Documents/WS_2018-2019/CoLeWe/Project/word2vec/home/common/word2vec/models/wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m")

# get similar words for "mangiare"; number of similar words - 10
similar_words = model.most_similar(positive=["mangiare"], topn=10)
# "similar words" is an array which consist of small arrays; every small array contains a similar word and its similarity score to "mangiare"

# print words (without their similarity scores)
for word in similar_words:
	print(word[0])