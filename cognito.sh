# CAVEAT only works for single id pool and user pool i.e. clean account as per book
#!/bin/bash
. ./.env
. checkenv.sh

case $1 in
  setup)
    # echo '#>>'>>.env
    # export JOBS_LIST_COGNITO_DOMAIN=$JOBS_LIST_COGNITO_DOMAIN_BASE.auth.us-west-2.amazoncognito.com
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

    aws cognito-idp create-user-pool-domain --domain $JOBS_LIST_COGNITO_DOMAIN_BASE --user-pool-id $JOBS_LIST_USER_POOL_ID

    aws cognito-idp update-user-pool-client --user-pool-id $JOBS_LIST_USER_POOL_ID --client-id $JOBS_LIST_USER_POOL_CLIENT_ID\
     --supported-identity-providers "COGNITO"\
     --callback-urls "[\"https://s3-${TARGET_REGION}.amazonaws.com/${JOBS_LIST_APPS_BUCKET}/index.html\"]"\
     --logout-urls "[\"https://s3-${TARGET_REGION}.amazonaws.com/${JOBS_LIST_APPS_BUCKET}/index.html\"]"\
     --allowed-o-auth-flows "implicit"\
     --allowed-o-auth-scopes "email" "openid" "aws.cognito.signin.user.admin"\
     --allowed-o-auth-flows-user-pool-client
  ;;
  teardown)
    aws cognito-idp delete-user-pool-domain --domain $JOBS_LIST_COGNITO_DOMAIN_BASE --user-pool-id $JOBS_LIST_USER_POOL_ID
  ;;
  *)
    echo 'nope'
  ;;
esac
