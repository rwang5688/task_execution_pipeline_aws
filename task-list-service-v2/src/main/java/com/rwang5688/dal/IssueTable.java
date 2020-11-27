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

import software.amazon.awssdk.enhanced.dynamodb.DynamoDbTable;
import software.amazon.awssdk.enhanced.dynamodb.model.QueryConditional;
import software.amazon.awssdk.enhanced.dynamodb.Key;
import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;


public class IssueTable {

        private static final Logger logger = LoggerFactory.getLogger(Issue.class);
        private static final String ISSUE_TABLE = System.getenv("ISSUE_TABLE");
        private static final TableSchema<Issue> ISSUE_TABLE_SCHEMA =
                StaticTableSchema.builder(Issue.class)
                        .newItemSupplier(Issue::new)
                        .addAttribute(String.class, a -> a.name("task_id")
                                .getter(Issue::getTaskId)
                                .setter(Issue::setTaskId)
                                .tags(primaryPartitionKey()))
                        .addAttribute(Integer.class, a -> a.name("task_issue_number")
                                .getter(Issue::getTaskIssueNumber)
                                .setter(Issue::setTaskIssueNumber)
                                .tags(primarySortKey()))
                        .addAttribute(String.class, a -> a.name("issue_key")
                                .getter(Issue::getIssueKey)
                                .setter(Issue::setIssueKey))
                        .addAttribute(String.class, a -> a.name("issue_certainty")
                                .getter(Issue::getIssueCertainty)
                                .setter(Issue::setIssueCertainty))
                        .addAttribute(Integer.class, a -> a.name("issue_complexity")
                                .getter(Issue::getIssueComplexity)
                                .setter(Issue::setIssueComplexity))
                        .addAttribute(String.class, a -> a.name("file_path")
                                .getter(Issue::getFilePath)
                                .setter(Issue::setFilePath))
                        .addAttribute(Integer.class, a -> a.name("start_line_no")
                                .getter(Issue::getStartLineNo)
                                .setter(Issue::setStartLineNo))
                        .addAttribute(Integer.class, a -> a.name("start_column_no")
                                .getter(Issue::getStartColumnNo)
                                .setter(Issue::setStartColumnNo))
                        .addAttribute(String.class, a -> a.name("function_name")
                                .getter(Issue::getFunctionName)
                                .setter(Issue::setFunctionName))
                        .addAttribute(String.class, a -> a.name("variable_name")
                                .getter(Issue::getVariableName)
                                .setter(Issue::setVariableName))
                        .addAttribute(String.class, a -> a.name("rule_set")
                                .getter(Issue::getRuleSet)
                                .setter(Issue::setRuleSet))
                        .addAttribute(String.class, a -> a.name("rule_code")
                                .getter(Issue::getRuleCode)
                                .setter(Issue::setRuleCode))
                        .addAttribute(String.class, a -> a.name("error_code")
                                .getter(Issue::getErrorCode)
                                .setter(Issue::setErrorCode))
                        .addAttribute(String.class, a -> a.name("message")
                                .getter(Issue::getMessage)
                                .setter(Issue::setMessage))
                        .build();

        private DynamoDBConnection dbConnection;
        private DynamoDbEnhancedClient enhancedClient;
        private DynamoDbTable<Issue> mappedTable;

        public IssueTable() {
                dbConnection = new DynamoDBConnection();
                enhancedClient = dbConnection.getEnhancedClient();
                mappedTable = enhancedClient.table(ISSUE_TABLE, ISSUE_TABLE_SCHEMA);
        }

        public List<Issue> getTaskIssues(String task_id) {
                List<Issue> results = new ArrayList<Issue>();

                try {
                        QueryConditional queryConditional = QueryConditional
                                                                .keyEqualTo(Key.builder()
                                                                .partitionValue(task_id)
                                                                .build());

                        Iterator<Issue> items = mappedTable.query(queryConditional).items().iterator();
                        while (items.hasNext()) {
                                Issue issue = items.next();
                                results.add(issue);
                        }
                } catch (DynamoDbException e) {
                        logger.info("IssueTable.getTaskIssues: " + e.getMessage());
                }

                return results;
        }

}

