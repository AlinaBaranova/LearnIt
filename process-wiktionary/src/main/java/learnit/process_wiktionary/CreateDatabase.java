package learnit.process_wiktionary;

import java.io.File;

import de.tudarmstadt.ukp.jwktl.JWKTL;

public class CreateDatabase {
	private static String PATH_TO_DUMP_FILE = "/Users/alinabaranova/Documents/WS_2018-2019/CoLeWe/Project/dewiktionary-20190120-pages-articles.xml";
	private static String TARGET_DIRECTORY = "/Users/alinabaranova/Documents/WS_2018-2019/CoLeWe/Project/wiktionary-data";
	private static boolean OVERWRITE_EXISTING_FILES = true;
	
	public static void main(String[] args) throws Exception {
		File dumpFile = new File(PATH_TO_DUMP_FILE);
		File outputDirectory = new File(TARGET_DIRECTORY);
		boolean overwriteExisting = OVERWRITE_EXISTING_FILES;
		
		JWKTL.parseWiktionaryDump(dumpFile, outputDirectory, overwriteExisting);
	}
}
