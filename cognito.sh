# CAVEAT only works for single id pool and user pool i.e. clean account as per book
#!/bin/bash
. ./.env
. checkenv.sh

case $1 in
  setup)
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

    aws cognito-idp create-user-pool-domain --domain $TASK_LIST_COGNITO_DOMAIN_BASE --user-pool-id $TASK_LIST_USER_POOL_ID

    aws cognito-idp update-user-pool-client --user-pool-id $TASK_LIST_USER_POOL_ID --client-id $TASK_LIST_USER_POOL_CLIENT_ID\
     --supported-identity-providers "COGNITO"\
     --callback-urls "[\"https://s3-${TARGET_REGION}.amazonaws.com/${TASK_LIST_APPS_BUCKET}/index.html\"]"\
     --logout-urls "[\"https://s3-${TARGET_REGION}.amazonaws.com/${TASK_LIST_APPS_BUCKET}/index.html\"]"\
     --allowed-o-auth-flows "implicit"\
     --allowed-o-auth-scopes "email" "openid" "aws.cognito.signin.user.admin"\
     --allowed-o-auth-flows-user-pool-client
  ;;
  teardown)
    aws cognito-idp delete-user-pool-domain --domain $TASK_LIST_COGNITO_DOMAIN_BASE --user-pool-id $TASK_LIST_USER_POOL_ID
  ;;
  *)
    echo 'nope'
  ;;
esac
