package learnit.process_wiktionary;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class CleanData {
	public static void main(String[] args) {
		String[] filenames = {"A1", "A2", "B1", "B2"};
		String outputfile = "A1-B2.tsv";
		mergeLists(filenames, outputfile);
		
		assignIdsToWords("A1-B2.tsv", "A1-B2_with_ids.tsv");
	}
	
	// assigns ids to every line of file and writes result to new file
	public static void assignIdsToWords(String inputFile, String outputFile) {
		try {
			// open file to read words from
			BufferedReader reader = new BufferedReader(new FileReader(inputFile));
			// open file to write words with ids to
			BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));
				
			// create an id counter
			int counter = 1;
			// write every word with id to output file
			String line;
			while ((line=reader.readLine()) != null) {
				writer.write(counter + "\t" + line + "\n");
				counter += 1;
			}
				
			// close files
			writer.close();
			reader.close();
				
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	// creates files with words unique for every level and file with words of all levels
	public static void mergeLists(String[] filenames, String outputfile) { // filenames without extention (assumed it is "tsv")
		// create an array list for words and poses of all the levels
		ArrayList<String> words = new ArrayList<String>();
		// create a string which will contain all unique words with their levels
		String wordsAllLevels = "";
		
		// extract word-tag pairs from every file
		for (String filename : filenames) {
			try {
				System.out.println(filename);
				// open file
				BufferedReader reader = new BufferedReader(new FileReader(filename + ".tsv"));
				// create a string for level
				String wordsForLevel = "";
				
				// go line by line
				String line;
				while ((line=reader.readLine()) != null) {
					if (! line.equals("")) {
						String[] wordTag = line.split("\t");
						
						// if word-tag pair is not in array list that contains all words that have been seen before, add it to words of this level and add it to array list
						if (! words.contains(wordTag[0] + wordTag[1])) {
							wordsForLevel += wordTag[0] + "\t" + wordTag[1] + "\t" + filename + "\n";
							words.add(wordTag[0] + wordTag[1]);
						}
					}	
				}
				
				reader.close();
				
				// write words for level to file
				BufferedWriter writer = new BufferedWriter(new FileWriter(filename + "_unique.tsv"));
				writer.write(wordsForLevel);
				writer.close();
				
				// add words of this level to words of all levels
				wordsAllLevels += wordsForLevel;
				
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		
		// write words of all levels to file
		try {
			BufferedWriter writer = new BufferedWriter(new FileWriter(outputfile));
			writer.write(wordsAllLevels);
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
