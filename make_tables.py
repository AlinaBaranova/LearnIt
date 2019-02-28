import json

def tables_for_words_and_examples(final_examples, sentences_with_ids, f_output_words, f_output_examples):
	# string for output of words and their examples
	output_words = ""
	# string for output of examples
	output_examples = ""

	# set for all sentences that suit as examples for words from the book
	sentences_used = set()

	# load dictionary of word ids and examples
	with open(final_examples) as file:
		examples_for_words = json.load(file)

	# fill output of words and their examples
	for word_id in examples_for_words:
		output_words += word_id
		examples_for_word = examples_for_words[word_id]

		# count for examples
		c_examples = 0
		# while there are less than 5 examples written, write tab and example if there is example left, and write only tab if there is no example left
		while c_examples < 5:
			if c_examples < len(examples_for_word):
				example_id = examples_for_word[c_examples]
				output_words += "\t" + example_id
				# add id of example to array of ids of sentences that are used as examples
				sentences_used.add(example_id)
			else:
				output_words += "\t"
			c_examples += 1

		output_words += "\n"

	# write words and their examples to file
	with open(f_output_words, "w") as file:
		file.write(output_words.strip())

	# load dictionary of sentence ids and sentences
	with open(sentences_with_ids) as file:
		sentences = json.load(file)

	# fill output of examples
	for example_id in sentences_used:
		output_examples += example_id + "\t" + sentences[example_id]

	# write examples to file
	with open(f_output_examples, "w") as file:
		file.write(output_examples.strip())

tables_for_words_and_examples("examples_final.json", "sentences_ita_with-ids.json", "../Tables/examples_for_words.tsv", "../Tables/examples.tsv")