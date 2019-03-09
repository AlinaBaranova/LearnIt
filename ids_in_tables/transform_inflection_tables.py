import json

# compress table with verb forms for easier search
def compress_verb_table(verb_table, verb_table_compressed):
	# compressed version of table
	output = ""

	# make an array of lines out of verb table
	with open(verb_table) as file:
		lines = file.readlines()
	lines = [line.strip() for line in lines]

	# for every line in array of lines
	for index_main in range(len(lines)):
		# if line has "1s" in it, write verb, tense and tense type to output
		if "\t1s\t" in lines[index_main]:
			beginning = lines[index_main].split("\t")[:3]
			beginning = "\t".join(beginning)
			output += beginning
			# write all forms for this verb, tense and tense type to one line
			for index_minor in range(index_main, len(lines)):
				if lines[index_minor].startswith(beginning):
					output += "\t" + lines[index_minor].split("\t")[4]
				else:
					output += "\n"
					break
		# if line has "/" in it, write the whole line to output
		elif "\t/\t" in lines[index_main]:
			output += lines[index_main] + "\n"

	# write output to file
	with open(verb_table_compressed, "w") as file:
		file.write(output)

# compress_verb_table("../Tables/word_forms/VerbFlexion.tsv", "../Tables/word_forms/VerbFlexion_compressed.tsv")

# create dictionary of words + their pos and word ids
def make_dictionary_for_transformation(words, f_output):
	# result dictionary
	words_dict = {}

	with open(words) as file:
		for line in file:
			# get array from line
			word_info = line.split("\t")
			word_pos = word_info[1] + "\t" + word_info[2]
			word_id = word_info[0]
			# add word + its pos and word_id to dictionary
			words_dict[word_pos] = word_id

	# write result dictionary to file
	with open(f_output, "w") as file:
		json.dump(words_dict, file)

# make_dictionary_for_transformation("../Tables/A1-B2_with-ids.tsv", "words.json")

# add word ids to inflection table
def replace_with_ids(words, f_input, pos, f_output, replace=True):
	# inflection table where words are replaced with word ids
	output = ""

	# load dictionary of words + their pos and word ids
	with open(words) as file:
		words_dict = json.load(file)

	# for every line in table with inflection
	with open(f_input) as file:
		for line in file:
			line_arr = line.split("\t")
			word = line_arr[0]
			# decide on inserting new column for ids or replacing first column with ids
			if replace == False:
				rest = "\t".join(line_arr)
			else:
				rest = "\t".join(line_arr[1:])

			# find word of certain pos in the dictionary; add id to output
			word_pos = word + "\t" + pos
			if word_pos in words_dict:
				word_id = words_dict[word_pos]
			else:
				print(word_pos)

			# add the rest of line to output
			output += word_id + "\t" + rest

	# write inflection table with ids to file
	with open(f_output, "w") as file:
		file.write(output)

# replace_with_ids("words.json", "../Tables/word_forms/AdjektivFlexion.tsv", "Adjektiv", "../Tables/word_forms/AdjektivFlexion_with-ids.tsv", False)
# replace_with_ids("words.json", "../Tables/word_forms/PronomenFlexion.tsv", "Pronomen", "../Tables/word_forms/PronomenFlexion_with-ids.tsv", False)
# replace_with_ids("words.json", "../Tables/word_forms/SubstantivFlexion.tsv", "Substantiv", "../Tables/word_forms/SubstantivFlexion_with-ids.tsv", False)
replace_with_ids("words.json", "../Tables/word_forms/VerbFlexion_compressed.tsv", "Verb", "../Tables/word_forms/VerbFlexion_with-ids.tsv", False)
