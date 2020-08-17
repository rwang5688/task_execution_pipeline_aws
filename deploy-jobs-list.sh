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
  cd jobs-list-service
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
# Require user pool ARN to enable user pool access to DynamoDB CRUD operations in jobs service.
# Lines below are from "cognito.sh":
    # echo '#>>'>>.env
    # export JOBS_LIST_COGNITO_DOMAIN=$JOBS_LIST_COGNITO_DOMAIN_BASE.auth.$TARGET_REGION.amazoncognito.com
    # echo JOBS_LIST_COGNITO_DOMAIN=$JOBS_LIST_COGNITO_DOMAIN>>.env

    # export JOBS_LIST_USER_POOL_ID=`aws cognito-idp list-user-pools --max-results 1 | jq -r '.UserPools | .[0].Id'`
    # echo JOBS_LIST_USER_POOL_ID=$JOBS_LIST_USER_POOL_ID>>.env

    # export JOBS_LIST_USER_POOL_CLIENT_ID=`aws cognito-idp list-user-pool-clients --user-pool-id $JOBS_LIST_USER_POOL_ID | jq -r '.UserPoolClients | .[0].ClientId'`
    # echo JOBS_LIST_USER_POOL_CLIENT_ID=$JOBS_LIST_USER_POOL_CLIENT_ID>>.env

    # export JOBS_LIST_USER_POOL_ARN=`aws cognito-idp describe-user-pool --user-pool-id $JOBS_LIST_USER_POOL_ID | jq -r '.UserPool.Arn'`
    # echo JOBS_LIST_USER_POOL_ARN=$JOBS_LIST_USER_POOL_ARN>>.env

    # export JOBS_LIST_ID_POOL_ID=`aws cognito-identity list-identity-pools --max-results 1 | jq -r '.IdentityPools | .[0].IdentityPoolId'`
    # echo JOBS_LIST_ID_POOL_ID=$JOBS_LIST_ID_POOL_ID>>.env
    # echo '#<<'>>.env

# Given Cognito domain name base and user pool id:
# create user pool domain.
# set user pool registration and sign-in pages.
. ./cognito.sh setup

# create jobs-service API domain
domain

# deploy jobs-service API functions
SERVICES=(jobs-list-service)
deploy

# pack frontend js into one file
cd frontend
npm run build

# deploy frontend app
aws s3 sync dist/ s3://$JOBS_LIST_APPS_BUCKET
cd ..

