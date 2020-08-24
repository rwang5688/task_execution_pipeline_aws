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


function domain () {
  cd task-list-service
  serverless delete_domain
  cd ..
}


# remove frontend apps
aws s3 rm s3://${TASK_LIST_APPS_BUCKET} --recursive

# remove jobs-service API functions
SERVICES=(task-list-service)
remove

# delete jobs-service API domain
domain

# delete user pool domain
. ./cognito.sh teardown

