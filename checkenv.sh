#!/bin/bash
declare -a vars=(AWS_ACCOUNT_ID TARGET_REGION \
  TASK_LIST_APPS_BUCKET \
  TASK_LIST_SOURCE_DATA_BUCKET TASK_LIST_LOG_DATA_BUCKET \
  TASK_LIST_SUBMIT_TASK_QUEUE TASK_LIST_PROCESS_TASK_QUEUE \
  TASK_LIST_UPDATE_TASK_QUEUE TASK_LIST_UPDATE_TASK_LOG_STREAM_QUEUE \
  TASK_LIST_TASK_TABLE \
  TASK_LIST_DOMAIN TASK_LIST_COGNITO_DOMAIN_BASE)

for var_name in "${vars[@]}"
do
  if [ -z "$(eval "echo \$$var_name")" ]; then
    echo "Missing environment variable $var_name. Please set before continuing"
    exit 1
  fi
done

