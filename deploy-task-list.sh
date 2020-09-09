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
  cd task-list-service
  npm install
  serverless create_domain
  cd ..
}


# As workaround due to non-Unix environment,
# Perform these manual deployment steps before running "deploy.sh" script:

# 1) Deploy user-service
# "cd user-service"
# "serverless deploy"

# 2) Edit .env file and replace Cognito domain name base, user pool id and ARN.
# Require user pool ARN to enable user pool access to DynamoDB CRUD operations in task-list-service.
# Lines below are from "cognito.sh":
    # echo '#>>'>>.env
    # export TASK_LIST_COGNITO_DOMAIN=$TASK_LIST_COGNITO_DOMAIN_BASE.auth.$TARGET_REGION.amazoncognito.com
    # echo TASK_LIST_COGNITO_DOMAIN=$TASK_LIST_COGNITO_DOMAIN>>.env

    # export TASK_LIST_USER_POOL_ID=`aws cognito-idp list-user-pools --max-results 1 | jq -r '.UserPools | .[0].Id'`
    # echo TASK_LIST_USER_POOL_ID=$TASK_LIST_USER_POOL_ID>>.env

    # export TASK_LIST_USER_POOL_CLIENT_ID=`aws cognito-idp list-user-pool-clients --user-pool-id $TASK_LIST_USER_POOL_ID | jq -r '.UserPoolClients | .[0].ClientId'`
    # echo TASK_LIST_USER_POOL_CLIENT_ID=$TASK_LIST_USER_POOL_CLIENT_ID>>.env

    # export TASK_LIST_USER_POOL_ARN=`aws cognito-idp describe-user-pool --user-pool-id $TASK_LIST_USER_POOL_ID | jq -r '.UserPool.Arn'`
    # echo TASK_LIST_USER_POOL_ARN=$TASK_LIST_USER_POOL_ARN>>.env

    # export TASK_LIST_ID_POOL_ID=`aws cognito-identity list-identity-pools --max-results 1 | jq -r '.IdentityPools | .[0].IdentityPoolId'`
    # echo TASK_LIST_ID_POOL_ID=$TASK_LIST_ID_POOL_ID>>.env
    # echo '#<<'>>.env

# Given Cognito domain name base and user pool id:
# create user pool domain.
# set user pool registration and sign-in pages.
. ./cognito.sh setup

# create task-list-service API domain
domain

# deploy task-list-service API functions
SERVICES=(task-list-service)
deploy

# pack frontend js into one file
cd frontend
npm install
npm run build

# deploy frontend app
aws s3 sync dist/ s3://$TASK_LIST_APPS_BUCKET
cd ..

