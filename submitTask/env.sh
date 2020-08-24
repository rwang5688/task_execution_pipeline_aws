#!/bin/bash
# AWS specific environment variables
export AWS_ACCOUNT_ID=700702834148
export TARGET_REGION=us-west-2

# task-list workflow and database specific environment variables
export TASK_LIST_SOURCE_DATA_BUCKET=task-list-source-data-bucket-rwang5688
export TASK_LIST_LOG_DATA_BUCKET=task-list-log-data-bucket-rwang5688
export TASK_LIST_SUBMIT_TASK_QUEUE=task-list-submit-task-queue-rwang5688
export TASK_LIST_PROCESS_TASK_QUEUE=task-list-process-task-queue-rwang5688
export TASK_LIST_UPDATE_TASK_QUEUE=task-list-update-task-queue-rwang5688
export TASK_LIST_UPDATE_TASK_LOG_STREAM_QUEUE=task-list-update-task-log-stream-queue-rwang5688
export TASK_LIST_TASK_TABLE=task-list-task-table-rwang5688

