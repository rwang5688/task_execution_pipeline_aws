#!/bin/bash
. ./.env
. checkenv.sh

cluster_name=$ECS_CLUSTER_NAME
task_definition=$ECS_TASK_DEFINITION
subnet1=$ECS_TASK_NETWORK_VPC_SUBNET1
subnet2=$ECS_TASK_NETWORK_VPC_SUBNET2
security_group=$ECS_TASK_NETWORK_AWS_VPC_SECURITY_GROUP

aws ecs run-task --cluster $cluster_name \
        --launch-type "FARGATE" \
        --task-definition $task_definition \
        --count 1 \
        --platform-version "LATEST" \
        --network-configuration "awsvpcConfiguration={subnets=[$subnet1, $subnet2],securityGroups=[$security_group], assignPublicIp=ENABLED}" \
        --overrides "containerOverrides=[]"
