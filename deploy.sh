#!/bin/bash
. ./.env
. checkenv.sh


function deploy () {
  for SERVICE in "${SERVICES[@]}"
  do
    echo ----------[ deploying $SERVICE ]----------
    cd $SERVICE
    if [ -f package.json ]; then
      npm install
    fi
    serverless deploy
    cd ..
  done
}


function domain () {
  cd resources
  npm install
  serverless create_domain
  cd ..
}


# (user-service sls deploy need to be done bf running this script
# and we need to manually edit .env to add the various ids and arns)
# create user pool domain
# set user pool login and logout pages
# extract user pool arn for deploying database CRUD service
#. ./cognito.sh setup


# create resources and functions
SERVICES=(resources)
deploy

# create jobs-service API domain
domain

# deploy jobs-service API functions
#SERVICES=(jobs-service)
#deploy

# pack frontend js into one file
# deploy frontend app
#cd frontend
#npm run build
#aws s3 sync dist/ s3://$JOBS_LIST_APPS_BUCKET
#cd ..

