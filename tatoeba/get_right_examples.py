import json

# choose maximum 5 examples for words that best suit to their level
def right_examples_for_words(word_levels, examples_to_words, sentences_levels, f_output):
	# result dictionary
	result = {}

	# get word ids and word levels
	words = {}
	with open(word_levels) as file:
		for line in file:
			line = line.strip()
			array = line.split("\t")
			word_id = array[0]
			word_level = array[3]
			words[word_id] = word_level

	# load sentence ids and their levels
	with open(sentences_levels) as file:
		sentences = json.load(file)

	# load word ids and arrays with their examples
	with open(examples_to_words) as file:
		all_examples = json.load(file)

	# count for words that don't have enough examples
	# c = 0

	# array with levels
	levels = ["None", "A1", "A2", "B1", "B2"]
	# find best examples for every word
	for word_id in all_examples:
		# get ids of examples
		examples = all_examples[word_id]
		# get index of word level from array with levels
		level_index = levels.index(words[word_id])
		final_examples = []

		# while not enough suitable examples are found for current level and there are lower levels left, try a level lower
		while level_index != -1 and len(final_examples) < 5:
			word_level = levels[level_index]
			
			# while not enough suitable examples are found and there are examples left, search further
			example_index = 0
			while example_index < len(examples) and len(final_examples) < 5:
				# if the level of example and current level of word is the same, add example to final examples for this word
				example_level = sentences[examples[example_index]]
				if example_level == word_level:
					final_examples.append(examples[example_index])
				example_index += 1

			level_index -= 1

		result[word_id] = final_examples

		# check if word has enough examples
		# if len(final_examples) < 5:
			# print("Didn't find enough examples for this word")
			# c += 1

	# print("Didn't find enough examples for words: " + str(c))

	# write result to file
	with open(f_output, "w") as file:
		json.dump(result, file)

# write reflexive verbs and their examples to text file; they need to be examined to determine if all the examples include reflexive verbs
def write_examples_for_reflexive_verbs(words, sentences_with_ids, reflexive_verbs_with_examples, final_examples_for_words, f_output):
	# string for result
	result = ""

	# load ids of reflexive verbs
	with open(reflexive_verbs_with_examples) as file:
		rvs_with_examples = json.load(file)
		rv_ids = list(rvs_with_examples.keys())

	# load words and their ids
	word_ids = {}
	with open(words) as file:
		for line in file:
			word_info = line.split("\t")
			word_id = word_info[0]
			word_text = word_info[1]
			word_ids[word_id] = word_text

	# load sentences and their ids
	with open(sentences_with_ids) as file:
		sentence_ids = json.load(file)

	# load word ids and their examples' ids
	with open(final_examples_for_words) as file:
		examples_for_words = json.load(file)

	# for every reflexive verb, write verb and its examples to file
	for rv_id in rv_ids:
		rv_text = word_ids[rv_id]
		result += rv_text + "\n\n"

		example_ids = examples_for_words[rv_id]
		for example_id in example_ids:
			result += sentence_ids[example_id]

		result += "------------------------------------------\n\n"

	# write result to file
	with open(f_output, "w") as file:
		file.write(result)

# right_examples_for_words("../Tables/A1-B2_with-ids.tsv", "sentences_to_words_full.json", "sentences_with-levels.json", "examples_final.json")
write_examples_for_reflexive_verbs("../Tables/A1-B2_with-ids.tsv", "sentences_ita_with-ids.json", "sentences_to_words_rv.json", "examples_final.json", "examples_for_reflexive_verbs.txt")