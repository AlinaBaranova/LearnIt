import treetaggerwrapper
import json
import re

def lemmatize_freq_list(freq_list, f_output):
	tagger = treetaggerwrapper.TreeTagger(TAGLANG="it")
	# count for processed words
	c = 0

	lemmas = set()
	with open(freq_list) as file:
		for line in file:
			c += 1
			word_array = line.split(" ")
			word = word_array[0]

			tags = tagger.tag_text(word)
			tt_array = tags[0].split("\t")
			if len(tt_array) == 3:
				lemma = tt_array[2]
				lemmas.add(lemma)
			if c%10000 == 0:
				print(c)

	lemmas_list = list(lemmas)
	with open(f_output, "w") as file:
		json.dump(lemmas_list, file)

# lemmatize_freq_list("frequency_list.txt", "frequency_list_lemmatized.json")

def preprocess_list_from_johannes(lemma_list, f_output):
	re_sharp = re.compile("(.*?)#")
	lemmas = set()

	with open(lemma_list) as file:
		for line in file:
			# split line with ","
			words = line.split(",")
			for word in words:
				# get rid of parts of complex words
				if not word.endswith("-"):
					n = re_sharp.match(word)
					if n != None:
						word = n.group(1)
					# get rid of punctuation marks in the end of word
					word = word.strip("!?.")
					lemmas.add(word)

	with open(f_output, "w") as file:
		for lemma in lemmas:
			file.write(lemma)

# preprocess_list_from_johannes("it-lemmas_Johannes.txt", "it-lemmas_Johannes_sorted.txt")

def join_two_lists(list_one, list_two, f_output):
	all_lemmas = set()

	for name in [list_one, list_two]:
		with open(name) as file:
			for line in file:
				all_lemmas.add(line.strip("\n"))

	with open(f_output, "w") as file:
		json.dump(list(all_lemmas), file)

join_two_lists("it-lemmas_Johannes_sorted.txt", "all_lemmas_wiktionary.txt", "lemmas_joined.json")