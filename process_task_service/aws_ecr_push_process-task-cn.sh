#!/bin/bash

cd ../process_task

aws ecr create-repository --repository-name process-task-cn --image-scanning-configuration scanOnPush=true
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 700702834148.dkr.ecr.us-west-2.amazonaws.com/process-task-cn

docker build -t 700702834148.dkr.ecr.us-west-2.amazonaws.com/process-task-cn:1.0 -f Dockerfile.mock .
docker push 700702834148.dkr.ecr.us-west-2.amazonaws.com/process-task-cn:1.0

cd ../process_task_service

