import json
from wordcloud import WordCloud

# generate wordcloud images for similar words extracted from word2vec model for words of open classes
def images_for_similar_words(similarity_scores):
	# load dictionary with word ids, similar words and their similarity scores
	with open(similarity_scores) as file:
		all_scores = json.load(file)

		for word_id in all_scores:
			# get dictionary with similar words and their similarity scores for one word
			scores = all_scores[word_id]
			# generate an image and write it to file named with word id
			wordcloud = WordCloud(width=1000, height=1000, prefer_horizontal=1.0, background_color="white").generate_from_frequencies(scores)
			wordcloud.to_file("img/" + str(word_id) + ".png")

images_for_similar_words("similarity_scores_for_all_words.json")