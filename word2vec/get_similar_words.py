from gensim.models import Word2Vec
import treetaggerwrapper
import re

# model = Word2Vec.load("./home/common/word2vec/models/wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m")

# similar_words = model.most_similar(positive=["uno"], topn=10)
# for word in similar_words:
# 	print(word[0])

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

def synonyms_for_words(words, f_output):
	model = Word2Vec.load("./home/common/word2vec/models/wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m")
	word_vectors = model.wv
	tagger = treetaggerwrapper.TreeTagger(TAGLANG="it")

	open_pos = ["Substantiv", "Adjektiv", "Adverb", "Verb"]

	re_italian = re.compile("[a-zA-Zàèéìíòóùú]+")

	# how many words were processed
	count = 0

	output = ""

	with open(words) as file:
		for line in file:
			array = line.split("\t")
			word_id = array[0]
			word = array[1]
			pos = array[2]
			# print(word + "\n")
			count += 1
			if pos in open_pos:
				if word in word_vectors.vocab:
					similar_words_array = []
					gold_n = 5
					old_n = 0
					new_n = 10
					while new_n > 0:
						similar_words = model.most_similar(positive=[word], topn=old_n + new_n)

						similar_words_to_check = similar_words[-new_n:]

						for similar_word in similar_words_to_check:
							similar_word = similar_word[0]
								
							# replace all alphabetical non-unicode characters with unicode characters
							similar_word = make_unicode(similar_word)
							# get rid of punctuation marks
							similar_word = similar_word.strip("!();:«»,.?\"\'[]{}")

							# check if all characters belong to alphabet
							m = re_italian.fullmatch(similar_word)
							if m != None:
								# replace word forms with lemmas and check if lemma is the same as word
								tags = tagger.tag_text(similar_word)
								info_array = tags[0].split("\t")
								if len(info_array) == 3:
									lemma = info_array[2]
									if lemma != word:

										lemma_pos = lemma + ":" + info_array[1]
										# check if word not in array
										if lemma_pos not in similar_words_array:
											similar_words_array.append(lemma_pos)
											# print(lemma)

							old_n += new_n
							new_n = gold_n - len(similar_words_array)

						# print("--------------------------")

					output += word
					for similar_word in similar_words_array:
						output += "\t" + similar_word
					output += "\n"

			if count % 100 == 0:
				print(count)

	with open(f_output, "w") as file:
		file.write(output)

synonyms_for_words("../Tables/A1-B2_with-ids.tsv", "similar_words_for_all_words.tsv")