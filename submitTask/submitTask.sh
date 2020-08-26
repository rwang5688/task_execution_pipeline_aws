#!/bin/bash
# set env vars
. ./env.sh

# import AWS credentials
aws configure import --csv "file://aws-admin_credentials.csv"
cat ~/.aws/credentials

# execute script
python3 ./submitTask.py $1 $2

