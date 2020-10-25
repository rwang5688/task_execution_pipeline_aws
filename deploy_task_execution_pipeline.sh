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

