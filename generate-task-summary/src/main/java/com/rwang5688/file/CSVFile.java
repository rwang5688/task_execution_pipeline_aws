package com.rwang5688.file;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileReader;

import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import java.util.List;
import java.util.ArrayList;


public class CSVFile {
    private static final Logger logger = LoggerFactory.getLogger(CSVFile.class);

	public String[] readHeader(String csvFilePath)
	{
		String[] result = new String[0];

		try {
			FileReader fileReader = new FileReader(csvFilePath);
			CSVReader csvReader = new CSVReader(fileReader);

			String[] nextRecord;
			while ((nextRecord = csvReader.readNext()) != null) {
				result = nextRecord;
				break;
			}

			csvReader.close();
			fileReader.close();
		}
		catch (Exception e) {
			logger.error("CSVFile.readHeader: " + e);
		}

		return result;
	}

    public List<String[]> readAll(String csvFilePath, boolean skipHeader) {
		List<String[]> result = new ArrayList<String[]>();

	    try {
		    FileReader fileReader = new FileReader(csvFilePath);
			CSVReader csvReader;
		    if (skipHeader) {
				csvReader = new CSVReaderBuilder(fileReader)
												.withSkipLines(1)
												.build();
			} else {
				csvReader = new CSVReaderBuilder(fileReader)
												.withSkipLines(0)
												.build();
			}

			result = csvReader.readAll();

			csvReader.close();
			fileReader.close();
	    }
	    catch (Exception e) {
		    logger.error("CSVFile.readAll: " + e);
        }

        return result;
	}
}

