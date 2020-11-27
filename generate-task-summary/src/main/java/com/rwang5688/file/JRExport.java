package com.rwang5688.file;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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
    private static final Logger logger = LoggerFactory.getLogger(JRExport.class);

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
            logger.info("JRExport.exportPDFFile: Begin with " +
                            "xmlFilePath=" + xmlFilePath + ", " +
                            "csvFilePath=" + csvFilePath + ", " +
                            "pdfFilePath=" + pdfFilePath + ". ");

            logger.info("JRExport.exportPDFFile: Read and compile report definition");
            JasperReport report = JasperCompileManager.compileReport(xmlFilePath);
            logger.info("JRExport.exportPDFFile: Finished compileReport.");

            logger.info("JRExport.exportPDFFile: Initialize data source.");
            JRCsvDataSource csvDataSource = new JRCsvDataSource(csvFilePath);
            logger.info("JRExport.exportPDFFile: Finished JRCsvDataSource initialization.");

            logger.info("JRExport.exportPDFFile: Skip and get first row as column names.");
            csvDataSource.setUseFirstRowAsHeader(true);
            String[] columnNames = getColumnNames(csvFilePath);
            csvDataSource.setColumnNames(columnNames);
            Map<String, Integer> colNames = csvDataSource.getColumnNames();
            logger.info("JRExport.exportPDFFile: Set column names to: " + colNames.toString());

            logger.info("JRExport.exportPDFFile: Create and fill report.");
            HashMap<String, Object> params = new HashMap<String, Object>();
            JasperPrint jasperPrint = JasperFillManager.fillReport(report, params, csvDataSource);
            logger.info("JRExport.exportPDFFile: Fniished fillReport.");
            csvDataSource.close();

            // export filled report to PDF file
            logger.info("JRExport.exportPDFFile: Export report to PDF file.");
            JasperExportManager.exportReportToPdfFile(jasperPrint, pdfFilePath);
            logger.info("JRExport.exportPDFFile: Finished exportReportToPdfFile.");
        } catch (JRException e) {
            logger.error("JRExport.exportPDFFile: " + e);
        }
    }
}

