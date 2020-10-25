#!/bin/bash

# TODO: We need to figure out how to inject AWS credentials in CICD env
# import AWS credentials
aws configure import --csv "file://default_credentials.csv"
cat ~/.aws/credentials

