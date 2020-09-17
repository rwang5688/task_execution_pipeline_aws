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

# remove task-list-frontend resources and task-list-service API functions
SERVICES=(task-list-frontend task-list-service)
remove

# delete task-list-service API domain
domain

# delete user pool domain
. ./cognito.sh teardown

