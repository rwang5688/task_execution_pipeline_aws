#!/bin/bash
. ./.env
. checkenv.sh


function remove () {
  for SERVICE in "${SERVICES[@]}"
  do
    echo ----------[ removing $SERVICE ]----------
    cd $SERVICE
    serverless remove
    cd ..
  done
}


# remove data
aws s3 rm s3://${TASK_EXEC_PREPROCESS_DATA_BUCKET} --recursive
aws s3 rm s3://${TASK_EXEC_LOG_DATA_BUCKET} --recursive
aws s3 rm s3://${TASK_EXEC_RESULT_DATA_BUCKET} --recursive

# remove resources and functions
SERVICES=(generateTaskSummary uploadTaskIssues updateTask createTask resources)
remove

# delete task and issue database tables
aws dynamodb delete-table --table-name ${TASK_EXEC_TASK_TABLE}-dev
aws dynamodb delete-table --table-name ${TASK_EXEC_ISSUE_TABLE}-dev

