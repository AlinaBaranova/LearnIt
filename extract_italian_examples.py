import json

# extracts Italian examples from file with all examples
def extract_examples(f_read, f_write):
	result = ""

	# open file with all examples
	with open(f_read) as file:
		for line in file:
			array = line.split("\t")
			# check if example is in Italian (second column - language)
			if array[1] == "ita":
				result += array[2]

	# write Italian examples to file
	with open(f_write, "w") as file:
		file.write(result)

# make json file out of tsv file with sentences and their ids
def make_json(f_read, f_write):
	result = {}

	with open(f_read) as file:
		for line in file:
			array = line.split("\t")
			result[array[0]] = array[1]

	with open(f_write, "w") as file:
		json.dump(result, file)

make_json("sentences_ita_with-ids.tsv", "sentences_ita_with-ids.json")