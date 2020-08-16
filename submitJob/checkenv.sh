#!/bin/bash
declare -a vars=(AWS_ACCOUNT_ID AWS_DEFAULT_REGION \
  JOBS_LIST_SOURCE_DATA_BUCKET JOBS_LIST_LOG_DATA_BUCKET \
  JOBS_LIST_SUBMIT_JOB_QUEUE JOBS_LIST_PROCESS_JOB_QUEUE \
  JOBS_LIST_UPDATE_JOB_QUEUE JOBS_LIST_UPDATE_JOBS_LOG_STREAM_QUEUE \
  JOBS_LIST_JOBS_TABLE)

for var_name in "${vars[@]}"
do
  if [ -z "$(eval "echo \$$var_name")" ]; then
    echo "Missing environment variable $var_name. Please set before continuing"
    exit 1
  fi
done

