#!/bin/bash
. ../.env
. ../checkenv.sh

serverless remove

aws dynamodb delete-table --table-name ${TASK_EXEC_TASK_TABLE}-dev
aws dynamodb delete-table --table-name ${TASK_EXEC_ISSUE_TABLE}-dev

