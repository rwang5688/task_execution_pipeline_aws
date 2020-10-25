package com.rwang5688;

import java.lang.StringBuilder;
import java.util.Map;
import java.util.List;
import java.util.concurrent.CompletableFuture;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.SQSEvent;
import com.amazonaws.services.lambda.runtime.events.SQSEvent.SQSMessage;

import software.amazon.awssdk.services.lambda.model.GetAccountSettingsRequest;
import software.amazon.awssdk.services.lambda.model.GetAccountSettingsResponse;
import software.amazon.awssdk.services.lambda.model.ServiceException;
import software.amazon.awssdk.services.lambda.LambdaAsyncClient;
import software.amazon.awssdk.services.lambda.model.AccountUsage;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

import com.rwang5688.dal.Task;
import com.rwang5688.dal.Issue;

// Handler value: example.Handler
public class GenerateTaskSummaryHandler implements RequestHandler<SQSEvent, String>{
  private static final Logger logger = LoggerFactory.getLogger(GenerateTaskSummaryHandler.class);
  private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();
  private static final LambdaAsyncClient lambdaClient = LambdaAsyncClient.create();

  public GenerateTaskSummaryHandler()
  {
    CompletableFuture<GetAccountSettingsResponse> accountSettings = lambdaClient.getAccountSettings(GetAccountSettingsRequest.builder().build());
    try {
      GetAccountSettingsResponse settings = accountSettings.get();
    } catch(Exception e) {
      e.getStackTrace();
    }
  }

  @Override
  public String handleRequest(SQSEvent event, Context context)
  {
    String response = new String();

    // call Lambda API
    logger.info("Getting account settings");
    CompletableFuture<GetAccountSettingsResponse> accountSettings =
        lambdaClient.getAccountSettings(GetAccountSettingsRequest.builder().build());

    // log execution details
    logger.info("ENVIRONMENT VARIABLES: {}", gson.toJson(System.getenv()));
    logger.info("CONTEXT: {}", gson.toJson(context));
    logger.info("EVENT: {}", gson.toJson(event));

    // process event
    for(SQSMessage msg : event.getRecords()){
      logger.info("Process msg: " + msg.getBody());
      try {
        // get task id
        ObjectMapper mapper = new ObjectMapper();
        JsonNode body = mapper.readTree((String) msg.getBody());
        logger.info("body: " + body.toString());
        JsonNode task = body.get("task");
        String user_id = task.get("user_id").asText();
        String task_id = task.get("task_id").asText();
        logger.info("user_id: " + user_id);
        logger.info("task_id: " + task_id);

        // get task
        Task taskRecord = new Task().get(user_id, task_id);
        logger.info("Task: " + taskRecord.toString());

        // get task issues
        List<Issue> taskIssues = new Issue().getTaskIssues(task_id);
        for (Issue issue : taskIssues) {
          logger.info("Issue: " + issue.toString());
        }
      } catch (Exception ex) {
        logger.error("Error in retrieving task issues: " + ex);
      }
      logger.info("Done with msg: " + msg.getBody());
    }

    // process Lambda API response
    try {
      GetAccountSettingsResponse settings = accountSettings.get();
      response = gson.toJson(settings.accountUsage());
      logger.info("Account usage: {}", response);
    } catch(Exception e) {
      e.getStackTrace();
    }
    return response;
  }
}

