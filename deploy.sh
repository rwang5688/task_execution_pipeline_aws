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
  cd jobs-service
  npm install
  serverless create_domain
  cd ..
}


# Before running "deploy.sh" script:
# Manually run "sls deploy user-service".
# Manually edit .env file with Cognito setup required domain name base, user pool id and ARN.
# user pool ARN required for user pool access to database CRUD operations in jobs service.

# Given domain name base and user pool id:
# create user pool domain.
# set user pool registration and sign-in pages.
#. ./cognito.sh setup

# create resources and functions
SERVICES=(resources createJob updateJob)
deploy

# create jobs-service API domain
#domain

# deploy jobs-service API functions
#SERVICES=(jobs-service)
#deploy

# pack frontend js into one file
#cd frontend
#npm run build

# deploy frontend app
#aws s3 sync dist/ s3://$JOBS_LIST_APPS_BUCKET
#cd ..

