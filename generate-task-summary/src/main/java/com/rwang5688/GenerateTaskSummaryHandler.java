package com.rwang5688;

import java.lang.StringBuilder;
import java.util.Map;
import java.util.List;
import java.util.concurrent.CompletableFuture;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import software.amazon.awssdk.services.lambda.model.GetAccountSettingsRequest;
import software.amazon.awssdk.services.lambda.model.GetAccountSettingsResponse;
import software.amazon.awssdk.services.lambda.model.ServiceException;
import software.amazon.awssdk.services.lambda.LambdaAsyncClient;
import software.amazon.awssdk.services.lambda.model.AccountUsage;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.SQSEvent;
import com.amazonaws.services.lambda.runtime.events.SQSEvent.SQSMessage;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

import com.rwang5688.dal.TaskTable;
import com.rwang5688.dal.Task;
import com.rwang5688.dal.IssueTable;
import com.rwang5688.dal.Issue;

import com.rwang5688.file.S3File;
import com.rwang5688.file.CSVFile;
import com.rwang5688.file.JRExport;
import java.util.Arrays;


// Handler value: example.Handler
public class GenerateTaskSummaryHandler implements RequestHandler<SQSEvent, String>{
  private static final Logger logger = LoggerFactory.getLogger(GenerateTaskSummaryHandler.class);
  private static final LambdaAsyncClient lambdaClient = LambdaAsyncClient.create();
  private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();
  private static final ObjectMapper mapper = new ObjectMapper();

  public GenerateTaskSummaryHandler()
  {
    //CompletableFuture<GetAccountSettingsResponse> accountSettings = lambdaClient.getAccountSettings(GetAccountSettingsRequest.builder().build());
    //try {
    //  GetAccountSettingsResponse settings = accountSettings.get();
    //} catch(Exception e) {
    //  e.getStackTrace();
    //}
  }

  private String bucket_name;

  private void setAttributesBasedOnEnvVars()
  {
    try {
      JsonNode env = mapper.readTree(gson.toJson(System.getenv()));
      logger.info("env=" + env.toString());

      bucket_name = env.get("RESULT_DATA_BUCKET").asText();

      logger.info("bucket_name=" + bucket_name);
    } catch (Exception e) {
      logger.error("setAttributesBasedOnEnvVars: " + e);
    }
  }

  private String user_id;
  private String task_id;
  private String task_summary_pdf;
  private String task_issues_csv;

  private void setAttributesBasedOnMsg(SQSMessage msg)
  {
    try {
      JsonNode body = mapper.readTree((String) msg.getBody());
      logger.info("body=" + body.toString());

      JsonNode task = body.get("task");
      logger.info("task=" + task.toString());

      user_id = task.get("user_id").asText();
      task_id = task.get("task_id").asText();
      task_summary_pdf = task.get("task_summary_pdf").asText();
      task_issues_csv = task.get("task_issues_csv").asText();

      logger.info("user_id=" + user_id);
      logger.info("task_id=" + task_id);
      logger.info("task_summary_pdf=" + task_summary_pdf);
      logger.info("task_issues_csv=" + task_issues_csv);
    } catch (Exception e) {
      logger.error("setAttributesBasedOnMsg: " + e);
    }
  }

  private Task task;

  private void readTask() {
    TaskTable taskTable = new TaskTable();
    task = taskTable.get(user_id, task_id);
    if (task != null) {
      logger.info("setTask: task=" + task.toString());
    } else {
      logger.info("setTask: task not found for user_id=" + user_id + ", task_id=" + task_id + ".");
    }
  }

  private void downloadTaskIssuesCSV() {
    S3File s3File = new S3File();
    String bucketName = bucket_name;
    String objectKey = user_id + "/" + task_id + "/" + task_issues_csv;
    String filePath = "/tmp/" + task_issues_csv;
    boolean success = s3File.downloadObject(bucketName, objectKey, filePath);
    if (success) {
      logger.info("downloadTaskIssuesCSV: Successfully downloaded " +
                    "bucketName=" + bucketName + ", " +
                    "objectKey=" + objectKey + ", " +
                    "filePath=" + filePath + ".");
    } else {
      logger.info("downloadTaskIssuesCSV: Failed to download " +
                    "bucketName=" + bucketName + ", " +
                    "objectKey=" + objectKey + ", " +
                    "filePath=" + filePath + ".");
    }
  }

  private List<String[]> csvAll;

  private void readTaskIssuesCSVData() {
    CSVFile csvFile = new CSVFile();
    String csvFilePath = "/tmp/" + task_issues_csv;
    logger.info("readTaskIssuesCSVFile: csvFilePath=" + csvFilePath);
    csvAll = csvFile.readAll(csvFilePath, false);
    logger.info("readTaskIssuesCSVData: Read " + csvAll.size() + " rows.");
    //for (String[] row : csvAll) {
    //  logger.info("readTaskIssuesCSVData: row=" + Arrays.toString(row));
    //}
  }

  private void downloadTaskIssuesXML(String objectKey) {
    S3File s3File = new S3File();
    String bucketName = bucket_name;
    String filePath = "/tmp/" + objectKey;
    boolean success = s3File.downloadObject(bucketName, objectKey, filePath);
    if (success) {
      logger.info("downloadTaskIssuesXML: Successfully downloaded " +
                    "bucketName=" + bucketName + ", " +
                    "objectKey=" + objectKey + ", " +
                    "filePath=" + filePath + ".");
    } else {
      logger.info("downloadTaskIssuesXML: Failed to download " +
                    "bucketName=" + bucketName + ", " +
                    "objectKey=" + objectKey + ", " +
                    "filePath=" + filePath + ".");
    }
  }

  private void copyTaskSummaryPDFFile() {
    S3File s3File = new S3File();
    String bucketName = bucket_name;
    String fromObjectKey = "task_summary.pdf";
    String toObjectKey = user_id + "/" + task_id + "/" + task_summary_pdf;
    logger.info("copyTaskSummaryPDFFile: Copying from " +
                "bucketName=" + bucketName + ", " + "fromObjectKey=" + fromObjectKey + " to " +
                "bucketName=" + bucketName + ", " + "toObjectKey=" + toObjectKey + ".");
    String response = s3File.copyObject(bucketName, fromObjectKey, bucketName, toObjectKey);
    logger.info("copyTaskSummaryPDFFile: response=" + response);
  }

  private void exportTaskIssuesPDFFile() {
    String xmlFileName = "task_issues.xml";
    downloadTaskIssuesXML(xmlFileName);
    String xmlFilePath = "/tmp/" + xmlFileName;
    logger.info("exportTaskIssuesPDFFile: xmlFilePath=" + xmlFilePath);

    String csvFilePath = "/tmp/" + task_issues_csv;
    logger.info("exportTaskIssuesPDFFile: csvFilePath=" + csvFilePath);

    String[] csvFileNameElements = task_issues_csv.split("\\.csv");
    logger.info("exportTaskIssuesPDFFile: csvFileNameElements=" + Arrays.toString(csvFileNameElements));
    String csvFileNameBase = csvFileNameElements[0];
    logger.info("exportTaskIssuesPDFFile: csvFileNameBase=" + csvFileNameBase);

    String pdfFileName = csvFileNameBase + ".pdf";
    String pdfFilePath = "/tmp/" + pdfFileName;
    logger.info("exportTaskIssuesPDFFile: pdfFilePath=" + pdfFilePath);

    JRExport jrExport = new JRExport();
    jrExport.exportPDFFile(xmlFilePath, csvFilePath, pdfFilePath);

    S3File s3File = new S3File();
    String bucketName = bucket_name;
    String objectKey = user_id + "/" + task_id + "/" + pdfFileName;
    String filePath = pdfFilePath;
    logger.info("exportTaskIssuesPDFFile: Uploading " +
                    "bucketName=" + bucketName + ", " +
                    "objectKey=" + objectKey + ", " +
                    "filePath=" + filePath + ".");
    String response = s3File.uploadObject(bucketName, objectKey, filePath);
    logger.info("exportTaskIssuesPDFFile: response=" + response);
  }

  @Override
  public String handleRequest(SQSEvent event, Context context)
  {
    String response = new String();

    // call Lambda API
    //logger.info("Getting account settings");
    //CompletableFuture<GetAccountSettingsResponse> accountSettings =
    //    lambdaClient.getAccountSettings(GetAccountSettingsRequest.builder().build());

    // log execution details
    logger.info("ENVIRONMENT VARIABLES: {}", gson.toJson(System.getenv()));
    logger.info("CONTEXT: {}", gson.toJson(context));
    logger.info("EVENT: {}", gson.toJson(event));

    setAttributesBasedOnEnvVars();

    // process event
    for(SQSMessage msg : event.getRecords()){
      logger.info("Process msg: " + msg.getBody());
      try {
        setAttributesBasedOnMsg(msg);
        readTask();
        downloadTaskIssuesCSV();
        readTaskIssuesCSVData();
        copyTaskSummaryPDFFile();
        // open issue: JRExport.exportPDFFile times out inside Lambda function
        //exportTaskIssuesPDFFile();
      } catch (Exception e) {
        logger.error("handleRequest: " + e);
      }
      logger.info("Done with msg: " + msg.getBody());
    }

    // process Lambda API response
    //try {
    //  GetAccountSettingsResponse settings = accountSettings.get();
    //  response = gson.toJson(settings.accountUsage());
    //  logger.info("Account usage: {}", response);
    //} catch(Exception e) {
    //  e.getStackTrace();
    //}
    return response;
  }
}

