# LearnIt

This learners dictionary of Italian is aimed at German speakers whose level of Italian spans from A1 to B2, according to the Common European Framework of Reference for Languages (CEFR). The tool provides the users with an opportunity of consulting level-specific vocabulary lists, as well as enables searching particular words from these lists. Both German-Italian and Italian-German directions of search are possible. Every dictionary entry contains the word's part of speech, senses, information about the word's inflection (when available), usage examples (when available) and a word cloud of similar words (when available).

### Resources

The CEFR is the source for the lists of level-specific vocabulary. Word senses were extracted from Wiktionary, and example sentences were taken from the Tatoeba. Word clouds were generated using Word2Vec and a Python package WordCloud.

### Languages used

Alina Baranova:
- Java: extracting senses from Wiktionary with the JWKTL library
- Python: retrieving examples from the corpus Tatoeba and assigning levels to them, extracting words that have a high degree of similarity with words in the vocabulary lists using Word2Vec, generating word clouds of these similar words with WordCloud

Marta Berardi:
- Java: creating inflectional rules for verbs, nouns and adjectives, frontend/backend coding (using GWT)
- SQL: creating an SQL database that includes information about words, word senses, inflections, examples and word clouds
- HTML & CSS: website frontend
