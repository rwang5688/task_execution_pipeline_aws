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


function domain-v1 () {
  cd task-list-service
  serverless delete_domain
  cd ..
}


function domain-v2 () {
  cd task-list-service-v2
  serverless delete_domain
  cd ..
}


# remove frontend apps
aws s3 rm s3://${TASK_LIST_APPS_BUCKET} --recursive

# remove task-list-frontend resources and task-list-service API functions
SERVICES=(task-list-frontend task-list-service task-list-service-v2)
remove

# delete task-list-service and task-list-service-v2 API domains
domain-v1
domain-v2

# delete user pool domain
. ./cognito.sh teardown

