import json
import operator

# sort out examples for reflexive verbs
def sort_examples_rv(words, examples_to_rvs, f_sentences, examples_to_other_words, f_output):
	# array with reflexive pronouns
	ref_prons = ["mi", "ti", "si", "ci", "vi"]

	# result dictionary
	result = {}

	# make a dictionary out of ids of verbs from book and verbs
	verbs = {}
	with open(words) as file:
		for line in file:
			array = line.split("\t")
			if array[2] == "Verb":
				verbs[array[0]] = array[1]

	# load dictionary with sentences
	with open(f_sentences) as file:
		sentences_processed = json.load(file)

	# load dictionary with reflexive verbs and arrays of sentences' ids
	with open(examples_to_rvs) as file:
		rv_examples = json.load(file)

	# for every reflexive verb, go through its examples and make sure word before reflexive verb is reflexive pronoun
	for rv_id in rv_examples:
		# array with sentences' ids for a verb
		examples = rv_examples[rv_id]
		# verb lemma (non-reflexive variant)
		verb = verbs[rv_id][:-2] + "e"

		result[rv_id] = []
		# for processed sentence for every sentence id
		for example_id in examples:
			# processed sentence
			sentence_words = sentences_processed[example_id]
			# go through all words in sentence
			for i in range(len(sentence_words)):
				if "lemma" in sentence_words[i]:
					# check if word is the verb
					if sentence_words[i]["lemma"] == verb:
						if i != 0:
							# check if word before the verb is reflexive pronoun
							word_before = sentence_words[i-1]["lemma"].lower()
							if word_before in ref_prons:
								# if word before is reflexive pronoun, add it to array of final examples
								result[rv_id].append(example_id)
		# if verb doesn't have any examples in the end, print it
		if result[rv_id] == []:
			print(verb)

	# open dictionary with word ids (all words except reflexive verbs) and arrays of their examples' ids
	with open(examples_to_other_words) as file:
		other_words = json.load(file)

	print("Before adding reflexive verbs:" + str(len(other_words)))

	# add reflexive verbs with examples to other words
	for rv_id in result:
		other_words[rv_id] = result[rv_id]

	print("After adding reflexive verbs:" + str(len(other_words)))

	# write full dictionary to file
	with open(f_output, "w") as file:
		json.dump(other_words, file)

# return key which has the highest value; if there are several keys with highest value, return None
def key_with_max_value(dic):
	key = max(dic, key = lambda x: dic.get(x))
	value = dic[key]
	if value != 0:
		for k in dic:
			if dic[k] == value and k != key:
				if k > key:
					key = k
		return key
	else:
		return None

# assign levels to sentences
def assign_levels(processed_sentences, words_book, f_output):
	# result dictionary
	result = {}

	# correspondence between book's parts of speech and TreeTagger parts of speech
	correspondence = {"Substantiv": "NOM", "Adjektiv": "ADJ", "Pronomen": "PRO", "Adverb": "ADV", "Verb": "VER", "Präposition": "PRE", "Konjunktion": "CON", "Interjektion": "INT", "Artikel": "DET"}

	# make dictionary with word-tag combinations and their levels
	words = {}
	with open(words_book) as file:
		for line in file:
			line = line.strip()
			array = line.split("\t")
			word = array[1]
			tag = array[2]
			if tag in correspondence:
				tag = correspondence[tag]
			word_tag = word + "\t" + tag
			word_tag = word_tag.lower()
			words[word_tag] = array[3]

	# load processed sentences
	with open(processed_sentences) as file:
		sentences = json.load(file)

	# statistics
	c_a1 = 0
	c_a2 = 0
	c_b1 = 0
	c_b2 = 0
	c_none = 0

	# for every sentence, determine how many words of each level there are
	for sentence_id in sentences:
		# dictionary for determining level of sentence
		determine_level = {"A1": 0, "A2": 0, "B1": 0, "B2": 0}
		# get array of words of sentence
		sentence = sentences[sentence_id]
		# for every word-tag combination, look for it in word-tag combinations of words from book
		for word in sentence:
			if "lemma" in word and "tag" in word:
				word_tag = word["lemma"] + "\t" + word["tag"]
				word_tag = word_tag.lower()
				# if word-tag combination from sentence is found, increase level corresponding to word-tag combination from book
				if word_tag in words:
					word_level = words[word_tag]
					determine_level[word_level] += 1
		# get level with highest score
		sentence_level = key_with_max_value(determine_level)
		if sentence_level == "A1":
			c_a1 += 1
		elif sentence_level == "A2":
			c_a2 += 1
		elif sentence_level == "B1":
			c_b1 += 1
		elif sentence_level == "B2":
			c_b2 += 1
		else:
			c_none += 1
		# write sentence id and score to result dictionary
		result[sentence_id] = sentence_level

	# print statistics
	print("A1: " + str(c_a1))
	print("A2: " + str(c_a2))
	print("B1: " + str(c_b1))
	print("B2: " + str(c_b2))
	print("No level: " + str(c_none))

	# write result to file
	with open(f_output, "w") as file:
		json.dump(result, file)

# sort_examples_rv("../Tables/A1-B2_with-ids.tsv", "sentences_to_words_rv.json", "sentences_processed.json", "sentences_to_words.json", "sentences_to_words_full.json")
assign_levels("sentences_processed.json", "../Tables/A1-B2_with-ids.tsv", "sentences_with-levels.json")