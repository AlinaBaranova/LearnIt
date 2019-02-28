import json
import treetaggerwrapper
import re

# it_string = "Mi sveglio presto."
# tagger = treetaggerwrapper.TreeTagger(TAGLANG="it")
# tags = tagger.tag_text(it_string)
# # tags = treetaggerwrapper.make_tags(tags)
# for tag in tags:
# 	print(tag)

# process sentences (tokenize, lemmatize, do POS-tagging) with TreeTagger
def tag_and_lemmatize(f_input, f_output):
	# create final dictionary
	result = {}

	count = 0

	# open Italian TreeTagger
	tagger = treetaggerwrapper.TreeTagger(TAGLANG="it")

	# load json file with sentences and their ids into dictionary
	with open(f_input) as file:
		sentences = json.load(file)

	# for every sentence in dictionary
	for sentence_id in sentences:
		# create array for sentence
		sentence_array = []

		# get sentence
		sentence = sentences[sentence_id]
		# process it
		tags = tagger.tag_text(sentence)

		# for every processed word in sentence
		for tag in tags:
			word_array = tag.split("\t")
			
			# create dictionary and write word, its POS-tag and lemma into it
			word_dict = {}
			word_dict["word"] = word_array[0]
			if len(word_array) > 1:
				word_dict["tag"] = word_array[1]
				if len(word_array) > 2:
					word_dict["lemma"] = word_array[2]

			# write dictionary for word innto array for sentence
			sentence_array.append(word_dict)

		# add sentence array to final dictionary
		result[sentence_id] = sentence_array
		count += 1
		if count % 5000 == 0:
			print(count)

	# print random item from final dictionary
	print(next(iter(result.values())))

	# write final dictionary to file
	with open(f_output, "w") as file:
		json.dump(result, file)

# transform dictionary with sentence ids and processed sentences into dictionary with word-tag labels and arrays of sentence ids where these words are encountered
def examples_to_example_words(f_input, f_output):
	# load dictionary with sentence ids and processed sentences
	with open(f_input) as file:
		sentences = json.load(file)

	# result dictionary
	wordTags = {}

	# introduce count to track running of program
	count = 0

	# regular expresstion for extracting general tag from detailed tag (e.g. "VER" from "VER:cond")
	re_tag = re.compile("[A-Z]+")

	for sentence_id in sentences:
		# get all dictionaries with words for sentence
		words = sentences[sentence_id]
		for word in words:
			# get "word + \t + tag" label
			if "lemma" in word and "tag" in word:
				# extract general tag from detailed tag
				n = re_tag.match(word["tag"])
				if n:
					wordTag = word["lemma"].lower() + "\t" + n.group(0)
					# if label in result dictionary, augment set with sentence id if id is not there yet
					if wordTag in wordTags:
						ids_set = wordTags[wordTag]
						ids_set.add(sentence_id)
						wordTags[wordTag] = ids_set
					# if label is not in result dictionary, add label and sentence id to result dictionary
					else:
						new_set = set()
						new_set.add(sentence_id)
						wordTags[wordTag] = new_set
						if "0" in wordTags[wordTag]:
							print(wordTags[wordTag])
				else:
					print(word["tag"])

		count += 1
		if count % 5000 == 0:
			print(count)

	# change sets to arrays
	new_wordTags = {}
	for wordTag in wordTags:
		new_wordTags[wordTag] = list(wordTags[wordTag])

	# print random item from result dictionary
	# print(next(iter(new_wordTags.values())))

	# write result dictionary to file
	with open(f_output, "w") as file:
		json.dump(new_wordTags, file)

# based on dictionary with word-tag labels and arrays of sentence ids where these words are encountered, make dictionary with ids of words from book and arrays of sentence ids where these words are encountered
def examples_to_words(f_input_example_words, f_input_words, f_output, f_output_rv):
	# correspondence between book's parts of speech and TreeTagger parts of speech
	correspondence = {"Substantiv": "NOM", "Adjektiv": "ADJ", "Pronomen": "PRO", "Adverb": "ADV", "Verb": "VER", "Präposition": "PRE", "Konjunktion": "CON", "Interjektion": "INT", "Artikel": "DET"}
	# PRO, VER, DET - startswith

	# result dictionary
	word_ids = {}
	word_ids_rv = {}

	# count words that were not found
	count = 0

	# load dictionary with word-tag labels and arrays of sentence ids where these words are encountered
	with open(f_input_example_words) as file:
		wordTags = json.load(file)

	# open file with words from book
	with open(f_input_words) as file:
		# for every line, extract word's id, lemma and tag
		for line in file:
			array = line.split("\t")
			word_id = array[0]
			word = array[1].lower()
			tag = array[2]
			if tag in correspondence:
				# concatenate lemma with corresponding TreeTagger tag
				wordTag_book = word + "\t" + correspondence[tag]
			# if tag is not in correspondence, it was changed for Tatoeba
			else:
				# concatenate lemma with tag
				wordTag_book = word + "\t" + tag
			# find wordTag combination from the book in dictionary with example words
			if wordTag_book in wordTags:
				# if found, add to result dictionary
				# print("Word found: " + wordTag_book)
				word_ids[word_id] = wordTags[wordTag_book]
			# if the word-tag combination was not found, check if word is reflexive verb
			else:
				# it word is reflexive verb
				if word.endswith("si"):
					# turn into non-reflexive
					new_word = word[:-2] + "e"
					# only one case here, because "Verb" has a value in correspondence
					wordTag_book = new_word + "\t" + correspondence[tag] 
					if wordTag_book in wordTags:
						word_ids_rv[word_id] = wordTags[wordTag_book]
					else:
						count += 1
						print("Reflexive verb not found: " + word + ", " + wordTag_book)
						# for wordTag in wordTags:
						# 	if wordTag.startswith(word + "\t"):
						# 		print(wordTag + ": " + str(len(wordTags[wordTag])))
				# if word is not reflexive verb
				else:
					count += 1
					print("Word not found: " + wordTag_book)
					# for wordTag in wordTags:
					# 	if wordTag.startswith(word + "\t"):
					# 		print(wordTag + ": " + str(len(wordTags[wordTag])))
			# else:
			# 	print("Tag not found: " + word + ", \"" + tag + "\"")
			# 	for wordTag in wordTags:
			# 		if wordTag.startswith(word + "\t"):
			# 			print(wordTag + ": " + str(len(wordTags[wordTag])))

	# print how many words were not found
	print("TOTAL words not found: " + str(count))

	# write result dictionary to file
	with open(f_output, "w") as file:
		json.dump(word_ids, file)

	# write file with reflexive verbs
	with open(f_output_rv, "w") as file:
		json.dump(word_ids_rv, file)


# tag_and_lemmatize("sentences_ita_with-ids.json", "sentences_processed.json")
# examples_to_example_words("sentences_processed.json", "examples_to_example_words.json")
# examples_to_words("examples_to_example_words.json", "../Tables/A1-B2_with-ids_for-extraction-tatoeba.tsv", "sentences_to_words.json", "sentences_to_words_rv.json")


# look at examples for some words which have different pos in TreeTagger
def examples_for_certain_words(word_array, f_input_example_words, f_sentences, f_output):
	# string for result
	result = ""

	# load dictionary with sentences' ids and sentences
	with open(f_sentences) as file:
		id_sentences = json.load(file)

	# load dictionary with word-tag combinations and array of sentences where word with this tag was found
	with open(f_input_example_words) as file:
		wordTags = json.load(file)

	# find words from the list in wordTags
	for wordTag_array in word_array:
		if wordTag_array in wordTags:
			# extract ids of example sentences
			example_ids = wordTags[wordTag_array]
			# add word and its pos-tag to result
			result += wordTag_array + "\n\n"
			# add text of every example sentence in array 
			for example_id in example_ids:
				result += id_sentences[example_id]
			result += "--------------------------------------------------------\n\n"
		else:
			print("Word-tag combination from array was not found in wordTags!!!")

	# write result to file
	with open(f_output, "w") as file:
		file.write(result)


# word_array = ["marrone\tNOM", "tale\tPRO", "tale\tNOM", "tale\tCON"]
# examples_for_certain_words(word_array, "examples_to_example_words.json", "sentences_ita_with-ids.json", "examples_to_certain_words.txt")