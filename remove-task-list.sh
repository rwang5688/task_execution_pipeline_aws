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
  cd jobs-list-service
  serverless delete_domain
  cd ..
}


# remove frontend apps
aws s3 rm s3://${JOBS_LIST_APPS_BUCKET} --recursive

# remove jobs-service API functions
SERVICES=(jobs-list-service)
remove

# delete jobs-service API domain
domain

# delete user pool domain
. ./cognito.sh teardown

