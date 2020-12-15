#!/bin/bash
. ./.env
. checkenv.sh


function compile () {
  for SERVICE in "${SERVICES[@]}"
  do
    echo ----------[ compiling $SERVICE ]----------
    cd $SERVICE
    mvn clean install
    cd ..
  done
}

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


# compile java functions
SERVICES=(generate-task-summary)
compile

# create resources and functions
SERVICES=(resources create_task update_task upload_task_issues generate-task-summary)
deploy

# copy generate-task-summary resources
cd generate-task-summary
aws s3 sync src/main/resources/jrExport s3://${TASK_EXEC_RESULT_DATA_BUCKET}
cd ..

# Lambda with container image doesn't work as expected
# when we need to write to file system
# ... comment out for now
#if [[ ${TARGET_CLOUD} == "aws" ]]; then
#  SERVICES=(process_task_service)
#  deploy
#fi

