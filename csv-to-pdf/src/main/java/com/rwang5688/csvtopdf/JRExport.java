package com.rwang5688.csvtopdf;

import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JasperCompileManager;
import net.sf.jasperreports.engine.JasperReport;
import net.sf.jasperreports.engine.data.JRCsvDataSource;
import net.sf.jasperreports.engine.JasperFillManager;
import net.sf.jasperreports.engine.JasperPrint;
import net.sf.jasperreports.engine.JasperExportManager;

import java.util.Map;
import java.util.HashMap;


public class JRExport {
    private String[] getColumnNames(String csvFilePath) {
        String[] columnNames;

        CSVFile csvFile = new CSVFile();
        columnNames = csvFile.readHeader(csvFilePath);

        return columnNames;
    }

    public void exportPDFFile(String xmlFilePath,
                                String csvFilePath,
                                String pdfFilePath) {
        try {
            // debug
            System.out.println("JRExport.exportPDFFile: Begin with " +
                            "xmlFilePath=" + xmlFilePath + ", " +
                            "csvFilePath=" + csvFilePath + ", " +
                            "pdfFilePath=" + pdfFilePath + ". ");

            System.out.println("JRExport.exportPDFFile: Read and compile report definition");
            JasperReport report = JasperCompileManager.compileReport(xmlFilePath);
            System.out.println("JRExport.exportPDFFile: Finished compileReport.");

            System.out.println("JRExport.exportPDFFile: Initialize data source.");
            JRCsvDataSource csvDataSource = new JRCsvDataSource(csvFilePath);
            System.out.println("JRExport.exportPDFFile: Finished JRCsvDataSource initialization.");

            System.out.println("JRExport.exportPDFFile: Skip and get first row as column names.");
            csvDataSource.setUseFirstRowAsHeader(true);
            String[] columnNames = getColumnNames(csvFilePath);
            csvDataSource.setColumnNames(columnNames);
            Map<String, Integer> colNames = csvDataSource.getColumnNames();
            System.out.println("JRExport.exportPDFFile: Set column names to: " + colNames.toString());

            System.out.println("JRExport.exportPDFFile: Create and fill report.");
            HashMap<String, Object> params = new HashMap<String, Object>();
            JasperPrint jasperPrint = JasperFillManager.fillReport(report, params, csvDataSource);
            System.out.println("JRExport.exportPDFFile: Fniished fillReport.");
            csvDataSource.close();

            // export filled report to PDF file
            System.out.println("JRExport.exportPDFFile: Export report to PDF file.");
            JasperExportManager.exportReportToPdfFile(jasperPrint, pdfFilePath);
            System.out.println("JRExport.exportPDFFile: Finished exportReportToPdfFile.");
        } catch (JRException e) {
            System.out.println("JRExport.exportPDFFile: " + e);
        }
    }
}

