#!/bin/bash
# AWS specific environment variables
export AWS_ACCOUNT_ID=700702834148
export TARGET_CLOUD=aws
export TARGET_REGION=us-west-2

# task-list workflow and database specific environment variables
export TASK_EXEC_PREPROCESS_DATA_BUCKET=task-exec-preprocess-data-bucket-rwang5688
export TASK_EXEC_LOG_DATA_BUCKET=task-exec-log-data-bucket-rwang5688
export TASK_EXEC_RESULT_DATA_BUCKET=task-exec-result-data-bucket-rwang5688
export TASK_EXEC_CREATE_TASK_QUEUE=task-exec-create-task-queue-rwang5688
export TASK_EXEC_WRITE_TASK_FILES_QUEUE=task-exec-write-task-files-queue-rwang5688
export TASK_EXEC_PROCESS_TASK_QUEUE=task-exec-process-task-queue-rwang5688
export TASK_EXEC_UPDATE_TASK_QUEUE=task-exec-update-task-queue-rwang5688
export TASK_EXEC_UPLOAD_TASK_ISSUES_QUEUE=task-exec-upload-task-issues-queue-rwang5688
export TASK_EXEC_TASK_TABLE=task-exec-task-table-rwang5688
export TASK_EXEC_FILE_TABLE=task-exec-file-table-rwang5688
export TASK_EXEC_ISSUE_TABLE=task-exec-issue-table-rwang5688

