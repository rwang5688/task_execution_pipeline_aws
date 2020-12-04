package com.rwang5688.dal;

import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import software.amazon.awssdk.enhanced.dynamodb.DynamoDbEnhancedClient;

import software.amazon.awssdk.enhanced.dynamodb.TableSchema;
import software.amazon.awssdk.enhanced.dynamodb.mapper.StaticTableSchema;
import static software.amazon.awssdk.enhanced.dynamodb.mapper.StaticAttributeTags.primaryPartitionKey;
import static software.amazon.awssdk.enhanced.dynamodb.mapper.StaticAttributeTags.primarySortKey;
import java.util.Map;

import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.model.QueryConditional;
import software.amazon.awssdk.enhanced.dynamodb.Key;
import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;


public class TaskTable {

        private static final Logger logger = LoggerFactory.getLogger(Task.class);
        private static final String TASK_TABLE = System.getenv("TASK_TABLE");
        private static final TableSchema<Task> TASK_TABLE_SCHEMA =
                StaticTableSchema.builder(Task.class)
                        .newItemSupplier(Task::new)
                        .addAttribute(String.class, a -> a.name("user_id")
                                .getter(Task::getUserId)
                                .setter(Task::setUserId)
                                .tags(primaryPartitionKey()))
                        .addAttribute(String.class, a -> a.name("task_id")
                                .getter(Task::getTaskId)
                                .setter(Task::setTaskId)
                                .tags(primarySortKey()))
                        .addAttribute(String.class, a -> a.name("project_name")
                                .getter(Task::getProjectName)
                                .setter(Task::setProjectName))
                        .addAttribute(String.class, a -> a.name("task_tool")
                                .getter(Task::getTaskTool)
                                .setter(Task::setTaskTool))
                        //.addAttribute(Map.class, a -> a.name("task_extra_options")
                        //      .getter(Task::getTaskExtraOptions)
                        //      .setter(Task::setTaskExtraOptions))
                        .addAttribute(String.class, a -> a.name("task_fileinfo_json")
                                .getter(Task::getTaskFileinfoJson)
                                .setter(Task::setTaskFileinfoJson))
                        .addAttribute(String.class, a -> a.name("task_fileinfo_json_url")
                                .getter(Task::getTaskFileinfoJsonUrl)
                                .setter(Task::setTaskFileinfoJsonUrl))
                        .addAttribute(String.class, a -> a.name("task_preprocess_tar")
                                .getter(Task::getTaskPreprocessTar)
                                .setter(Task::setTaskPreprocessTar))
                        .addAttribute(String.class, a -> a.name("task_preprocess_tar_url")
                                .getter(Task::getTaskPreprocessTarUrl)
                                .setter(Task::setTaskPreprocessTarUrl))
                        .addAttribute(String.class, a -> a.name("task_source_code_zip")
                                .getter(Task::getTaskSourceCodeZip)
                                .setter(Task::setTaskSourceCodeZip))
                        .addAttribute(String.class, a -> a.name("task_source_code_zip_url")
                                .getter(Task::getTaskSourceCodeZipUrl)
                                .setter(Task::setTaskSourceCodeZipUrl))
                        .addAttribute(String.class, a -> a.name("task_status")
                                .getter(Task::getTaskStatus)
                                .setter(Task::setTaskStatus))
                        .addAttribute(String.class, a -> a.name("task_dot_scan_log_tar")
                                .getter(Task::getTaskDotScanLogTar)
                                .setter(Task::setTaskDotScanLogTar))
                        .addAttribute(String.class, a -> a.name("task_dot_scan_log_tar_url")
                                .getter(Task::getTaskDotScanLogTarUrl)
                                .setter(Task::setTaskDotScanLogTarUrl))
                        .addAttribute(String.class, a -> a.name("task_scan_result_tar")
                                .getter(Task::getTaskScanResultTar)
                                .setter(Task::setTaskScanResultTar))
                        .addAttribute(String.class, a -> a.name("task_scan_result_tar_url")
                                .getter(Task::getTaskScanResultTarUrl)
                                .setter(Task::setTaskScanResultTarUrl))
                        .addAttribute(String.class, a -> a.name("task_summary_pdf")
                                .getter(Task::getTaskSummaryPdf)
                                .setter(Task::setTaskSummaryPdf))
                        .addAttribute(String.class, a -> a.name("task_summary_pdf_url")
                                .getter(Task::getTaskSummaryPdfUrl)
                                .setter(Task::setTaskSummaryPdfUrl))
                        .addAttribute(String.class, a -> a.name("task_issues_csv")
                                .getter(Task::getTaskIssuesCsv)
                                .setter(Task::setTaskIssuesCsv))
                        .addAttribute(String.class, a -> a.name("task_issues_csv_url")
                                .getter(Task::getTaskIssuesCsvUrl)
                                .setter(Task::setTaskIssuesCsvUrl))
                        .addAttribute(String.class, a -> a.name("submit_timestamp")
                                .getter(Task::getSubmitTimestamp)
                                .setter(Task::setSubmitTimestamp))
                        .addAttribute(String.class, a -> a.name("update_timestamp")
                                .getter(Task::getUpdateTimestamp)
                                .setter(Task::setUpdateTimestamp))
                        .build();

        private DynamoDBConnection dbConnection;
        private DynamoDbEnhancedClient enhancedClient;
        private DynamoDbTable<Task> mappedTable;

        public TaskTable() {
                dbConnection = new DynamoDBConnection();
                enhancedClient = dbConnection.getEnhancedClient();
                mappedTable = enhancedClient.table(TASK_TABLE, TASK_TABLE_SCHEMA);
        }

        public Task get(String user_id, String task_id) {
                Task result = null;

                try {
                        Task taskToGet = new Task();
                        taskToGet.setUserId(user_id);
                        taskToGet.setTaskId(task_id);
                        logger.info("TaskTable.get: taskToGet=" + taskToGet.toString());
                        result = mappedTable.getItem(taskToGet);
                } catch (DynamoDbException e) {
                        logger.info("TaskTable.get: " + e.getMessage());
                }

                // debug
                if (result != null) {
                        logger.info("TaskTable.get: task=" + result.toString());
                } else {
                        logger.info("TaskTable.get: task does not exist for user_id=" + user_id + ", task_id=" + task_id + ".");
                }

                return result;
        }

        public void save(Task task) {
                if (task == null) {
                        logger.info("TaskTable.save: task is null.");
                        return;
                }

                try {
                        logger.info("TaskTable.save: task=" + task.toString());
                        mappedTable.putItem(task);
                } catch (DynamoDbException e) {
                        logger.info("TaskTable.save: " + e.getMessage());
                }
        }

        public Boolean delete(String user_id, String task_id) {
                Task task = null;

                task = get(user_id, task_id);
                if (task == null) {
                        logger.info("TaskTable.delete: task does not exist.");
                        return false;
                }

                logger.info("TaskTable.delete: task=" + task.toString());
                mappedTable.deleteItem(task);
                return true;
        }

        public List<Task> list() {
                List<Task> results = new ArrayList<Task>();

                try {
                        Iterator<Task> items = mappedTable.scan().items().iterator();
                        while (items.hasNext()) {
                                Task task = items.next();
                                results.add(task);
                        }
                } catch (DynamoDbException e) {
                        logger.info("TaskTable.list: " + e.getMessage());
                }

                return results;
        }

}

