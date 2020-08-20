#!/bin/bash
# set env vars
. ./env.sh

# import AWS credentials
aws configure import --csv "file://aws-admin_accessKeys.csv"
cat ~/.aws/credentials

# execute script
python3 ./submitJob.py $1 $2

