package com.rwang5688.csvtopdf;

import java.util.Arrays;
import java.util.List;

/**
 * csv-to-pdf.
 */
public final class App {
    private App() {
    }

    /**
     * main.
     * @param args The arguments of the program.
     */
    public static void main(String[] args) {
        String csvFilePath = "";
        String xmlFilePath = "";
        String pdfFilePath = "";

        System.out.println("Start csv-to-pdf ...");

        System.out.println("==");
        System.out.println("Set file paths");
        System.out.println("==");
        csvFilePath = args[0];
        System.out.println("csvFilePath=" + csvFilePath);

        // parse CSV file base
        String[] csvFilePathElements = csvFilePath.split("\\.csv");
        System.out.println("csvFilePathElements=" + Arrays.toString(csvFilePathElements));
        String csvFileNameBase = csvFilePathElements[0];
        System.out.println("csvFileNameBase=" + csvFileNameBase);

        // set and print XML file path as src/resources/main/jrExport/$(csvFileNameBase).xml
        xmlFilePath = "src/main/resources/jrExport/" + csvFileNameBase + ".xml";
        System.out.println("xmlFilePath=" + xmlFilePath);

        // set and print PDF file path as $(csvFileNameBase).pdf
        pdfFilePath = csvFileNameBase + ".pdf";
        System.out.println("pdfFilePath=" + pdfFilePath);

        System.out.println("==");
        System.out.println("Test CSV file reader");
        System.out.println("==");
        CSVFile csvFile = new CSVFile();
        // read the entire CSV file including header (skipHeader=false)
        List<String[]> csvAll = csvFile.readAll(csvFilePath, false);
        for (String[] row : csvAll) {
            System.out.println("row: " + Arrays.toString(row));
        }

        System.out.println("==");
        System.out.println("Test JaperReport PDF file export");
        System.out.println("==");
        JRExport jrExport = new JRExport();
        jrExport.exportPDFFile(xmlFilePath,
                            csvFilePath,
                            pdfFilePath);

        System.out.println("... End csv-to-pdf");
    }
}

