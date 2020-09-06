#!/bin/bash
# set env vars
. ./env.sh

# import AWS credentials
aws configure import --csv "file://aws-admin_credentials.csv"
cat ~/.aws/credentials

# read task config json, create task id, upload files, submit task
echo "[CMD] python3 submitTask.py $1"
python3 ./submitTask.py $1

