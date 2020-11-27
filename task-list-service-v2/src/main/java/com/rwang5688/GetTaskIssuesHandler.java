package com.rwang5688;

import java.util.Collections;
import java.util.Map;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

import com.rwang5688.dal.Issue;
import com.rwang5688.dal.IssueTable;


public class GetTaskIssuesHandler implements RequestHandler<Map<String, Object>, ApiGatewayResponse> {

	private static final Logger logger = LoggerFactory.getLogger(GetTaskIssuesHandler.class);
    private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();

	@Override
	public ApiGatewayResponse handleRequest(Map<String, Object> input, Context context) {
		// log execution details
		logger.info("ENVIRONMENT VARIABLES: {}", gson.toJson(System.getenv()));
		logger.info("CONTEXT: {}", gson.toJson(context));
        logger.info("INPUT: {}", gson.toJson(input));

        try {
            // get the 'pathParameters' from input
            Map<String, String> pathParameters =  (Map<String, String>)input.get("pathParameters");
            String taskId = pathParameters.get("id");

            // get task issues
            List<Issue> taskIssues = new IssueTable().getTaskIssues(taskId);
            for (Issue issue : taskIssues) {
                logger.info("handleRequest: issue=" + issue);
            }

            // send the response back
            return ApiGatewayResponse.builder()
                    .setStatusCode(200)
                    .setObjectBody(taskIssues)
                    .setHeaders(Collections.singletonMap("X-Powered-By", "AWS Lambda & Serverless"))
                    .build();
        } catch (Exception ex) {
            logger.error("Error in retrieving task issues: " + ex);

            // send the error response back
            Response responseBody = new Response("Error in retrieving task issues: ", input);
            return ApiGatewayResponse.builder()
                    .setStatusCode(500)
                    .setObjectBody(responseBody)
                    .setHeaders(Collections.singletonMap("X-Powered-By", "AWS Lambda & Serverless"))
                    .build();
        }
    }

}

