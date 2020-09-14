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
aws s3 rm s3://${TASK_LIST_PREPROCESS_DATA_BUCKET} --recursive
aws s3 rm s3://${TASK_LIST_LOG_DATA_BUCKET} --recursive
aws s3 rm s3://${TASK_LIST_RESULT_DATA_BUCKET} --recursive

# remove resources and functions
SERVICES=(updateTask createTask resources)
remove

# delete tasks database table
aws dynamodb delete-table --table-name ${TASK_LIST_TASK_TABLE}-dev

