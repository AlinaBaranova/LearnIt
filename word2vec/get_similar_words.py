from gensim.models import Word2Vec
import treetaggerwrapper
import re
import json

# model = Word2Vec.load("./home/common/word2vec/models/wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m")

# similar_words = model.most_similar(positive=["uno"], topn=10)
# for word in similar_words:
# 	print(word[0])

# transforms words of cp1251 encoding to utf-encoding (mostly Italian characters)
def make_unicode(string):
	# letters
	string = string.replace("Ã¨", "è").replace("Ã©", "é")
	string = string.replace("Ã¬", "ì")
	string = string.replace("Ã²", "ò")
	string = string.replace("Ã¹", "ù")
	string = string.replace("Ã", "à")

	# quotes
	string = string.replace("Â«", "«").replace("Â»", "»")

	return string

# gets first 5 proper similar words to all words of open classes
def synonyms_for_words(words, f_output_table, f_output_similarity_scores):
	# load model and TreeTagger
	model = Word2Vec.load("./home/common/word2vec/models/wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m")
	word_vectors = model.wv
	tagger = treetaggerwrapper.TreeTagger(TAGLANG="it")

	# open classes (do not include interjection)
	open_pos = ["Substantiv", "Adjektiv", "Adverb", "Verb"]

	re_italian = re.compile("[a-zA-Zàèéìíòóùú]+")

	# load frequency list
	# freq = set()
	# with open("frequency_list.txt") as file:
	# 	for line in file:
	# 		array = line.split(" ")
	# 		word = array[0]
	# 		freq.add(word)

	# load lemmatized version of frequency list
	# with open("frequency_list_lemmatized.json") as file:
	# 	freq_lemmatized = json.load(file)

	# load lemmas from Wiktionary and lemmas of Johannes, combined
	with open("lemmas_joined.json") as file:
		lemmas_joined = json.load(file)

	# how many words were processed
	count = 0
	# how many words were sorted out as non-Italian words
	sorted_out = 0
	# words of open classes not found in model vocabulary
	not_found = []
	# check how many similar words are needed to get five proper ones
	n_similar_words = {}
	# similar words and their similarity scores for all words
	similarity_scores_all = {}

	output = {}

	with open(words) as file:
		for line in file:
			# get word, its id and its pos-tag
			array = line.split("\t")
			word_id = array[0]
			word = array[1]
			pos = array[2]
			count += 1
			# check if word is noun, adjective, verb or adverb
			if pos in open_pos:
				# check if word in model's vocabulary
				if word in word_vectors.vocab:
					# check if word not already in output (for homonyms of different parts of speech)
					if word_id not in output.keys():
						# array for words similar to the current one
						similar_words_array = []
						# dictionary for similar words and similarity scores
						similarity_scores = {}
						gold_n = 5
						old_n = 0
						new_n = 10
						while new_n > 0:
							n_total = old_n + new_n
							similar_words = model.most_similar(positive=[word], topn=n_total)

							similar_words_to_check = similar_words[-new_n:]

							for similar_word in similar_words_to_check:
								similarity_score = float("%.4f" % similar_word[1])
								similar_word = similar_word[0]
									
								# replace all alphabetical non-unicode characters with unicode characters
								similar_word = make_unicode(similar_word)

								# get rid of punctuation marks
								similar_word = similar_word.strip("!();:«»,.?\"\'[]{}")

								# check if all characters belong to alphabet
								m = re_italian.fullmatch(similar_word)
								if m != None:

									# replace word forms with lemmas
									tags = tagger.tag_text(similar_word)
									info_array = tags[0].split("\t")
									if len(info_array) == 3:
										lemma = info_array[2]
										# check if lemma is the same as word
										if lemma != word:
											# check if lemma is in combined list of lemmas
											if lemma in lemmas_joined:
												# check if word not in array of similar words
												if lemma not in similar_words_array:
													# add to array of similar words
													similar_words_array.append(lemma)
													# add to dictionary of similarity scores
													similarity_scores[lemma] = similarity_score
											else:
												sorted_out += 1

								old_n += new_n
								new_n = gold_n - len(similar_words_array)

						output[word_id] = similar_words_array[:5]
						n_similar_words[word] = n_total
						similarity_scores_all[word_id] = similarity_scores

				else:
					# words of open classes which are not found in model vocabulary
					not_found.append(word)

			if count % 100 == 0:
				print(count)

	print("Sorted out: " + str(sorted_out))
	print("Not found: " + ", ".join(not_found))

	with open(f_output_table, "w") as file:
		for word_id in output:
			file.write(word_id)
			for word in output[word_id]:
				file.write("\t" + word)
			file.write("\n")

	with open("n_similar_words.tsv", "w") as file:
		for word in n_similar_words:
			file.write(word + "\t" + str(n_similar_words[word]))

	with open("f_output_similarity_scores", "w") as file:
		json.dump(similarity_scores_all, file)

synonyms_for_words("../Tables/A1-B2_with-ids.tsv", "../Tables/similar_words_for_all_words.tsv", "similarity_scores_for_all_words.json")