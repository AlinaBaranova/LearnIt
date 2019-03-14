import treetaggerwrapper

# sentence to process
sentence = "La matematica è come l'amore - un'idea semplice, che però può diventare complicata."

# open the tagger
tagger = treetaggerwrapper.TreeTagger(TAGLANG="it")

# process the sentence
tags = tagger.tag_text(sentence)
# "tags" is an array of strings; every string consists of word form, pos-tag and lemma separated by tabs

# print every string in the array
for tag in tags:
	print(tag)