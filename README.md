# LearnIt
Learners dictionary of Italian for German speakers

## Parsing Wiktionary Dump (with JWKTL)
* JWKTL Getting Started: https://dkpro.github.io/dkpro-jwktl/documentation/getting-started/ - main guide

Links (use them instead the ones in the guide):
* Oracle Berkeley DB Java Edition: download from here https://www.oracle.com/technetwork/database/database-technologies/berkeleydb/downloads/index.html
* German Wiktionary dump: https://dumps.wikimedia.org/dewiktionary/latest/, file *dewiktionary-latest-pages-articles.xml.bz2*

Important notes not mentioned in the JWKTL Getting Started:
* create a Maven project
* add JWKTL dependency to your pom.xml file: https://dkpro.github.io/dkpro-jwktl/

## TreeTagger
* Follow the guide on http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/ to download TreeTagger
* Install package *treetaggerwrapper* for Python

## Word2Vec
* Get word2vec model: http://hlt.isti.cnr.it/wordembeddings/ (word vectors trained with skipgram's word2vec)
* Install package *gensim* for Python

## Run the project in Eclipse
* Install MySQL Java Connector (https://dev.mysql.com/downloads/connector/j/8.0.html). Make sure to create a lib folder in the project hierarchy in which the .jar  'mysql-connector-java-8.0.13.jar' has to be placed.
* Project Properties>GWT>JavaBuildPath>Add Jars, then select the lib folder from the project hierarchy and add it.
* database on MySQL

# Plan of report
1. Introduction
2. Related Work / Comparable Tools
3. Senses (Wiktionary, Langenscheidt and Leo)
4. Inflected Forms (verbs, nouns, adjectives)
5. Examples (Tatoeba)
6. Word Clouds of Similar Words
7. User Interface
8. Division of Tasks
9. Discussion
