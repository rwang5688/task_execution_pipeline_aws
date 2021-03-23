# task_execution_pipeline_aws_cn
Task Execution Pipeline for processing various static analysis tasks running on AWS.

# prerequisites
You need to handle the AWS account and permissions.
You need to deploy a ECS fargate cluster with 0 desired number of tasks on the ECS console.

# deploy
First replace all 'fill-this-value' with correct value in .env file.
Then run deploy.sh to deploy task execution pipeline.

# remove
You need to delete the ECS fargate cluster on the ECS console.
Run remove.sh to remove the task execution pipeline.

# problem and solution
1. If you provide the incorrect value to AWS account id in .env file, all the AWS lambda function will fail to deploy.
Provide the correct value and run deploy.sh again.
2. If you provide the incorrect value to ECS_XXX related variables in .env file, run ECS task will fail. 
And messages will be blocked in process task queue. Provide the correct value and redeploy create task lambda function to make create task works work in the future.
For messages that blocked in process task queue, run run_ecs_task.sh manually can consume the messages in process task queue and all later task will continue.


