package com.rwang5688;

import java.util.Collections;
import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;

import com.rwang5688.dal.Task;


public class CreateTaskHandler implements RequestHandler<Map<String, Object>, ApiGatewayResponse> {

	private static final Logger logger = LogManager.getLogger(CreateTaskHandler.class);

	@Override
	public ApiGatewayResponse handleRequest(Map<String, Object> input, Context context) {
		logger.info("received: {}", input);
		try {
			// get the 'body' from input
			ObjectMapper mapper = new ObjectMapper();
			JsonNode body = mapper.readTree((String) input.get("body"));
			JsonNode taskExtraOptions = body.get("task_extra_options");
			Map<String, String> taskExtraOptionsMap = mapper.convertValue(taskExtraOptions,
														new TypeReference<Map<String, String>>(){});

			// create the Task object for post
			Task task = new Task();

			task.setUserId(body.get("user_id").asText());
			// task.setTaskId(body.get("task_id").asText());
			task.setTaskTool(body.get("task_tool").asText());
			task.setTaskExtraOptions(taskExtraOptionsMap);
			task.setTaskSourceCode(body.get("task_source_code").asText());
			task.setTaskSourceFileinfo(body.get("task_source_fileinfo").asText());
			task.setTaskPreprocessTar(body.get("task_preprocess_tar").asText());
			task.setTaskStatus(body.get("task_status").asText());
			task.setSubmitTimestamp(body.get("submit_timestamp").asText());
			task.setUpdateTimestamp(body.get("update_timestamp").asText());

			task.save(task);

			// send the response back
			return ApiGatewayResponse.builder()
					.setStatusCode(200)
					.setObjectBody(task)
					.setHeaders(Collections.singletonMap("X-Powered-By", "AWS Lambda & Serverless"))
					.build();
		} catch (Exception ex) {
			logger.error("Error in saving task: " + ex);

			// send the error response back
			Response responseBody = new Response("Error in saving task: ", input);
			return ApiGatewayResponse.builder()
					.setStatusCode(500)
					.setObjectBody(responseBody)
					.setHeaders(Collections.singletonMap("X-Powered-By", "AWS Lambda & Serverless"))
					.build();
		}
	}

}

