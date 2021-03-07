import os
import boto3


def get_ecs_client():
    region_name = ''
    if 'TARGET_REGION' in os.environ:
        region_name = os.environ['TARGET_REGION']
    print('get_ecs_client: region_name=%s' % region_name)

    session = boto3.Session(profile_name=None)
    ecs = session.client('ecs',
        region_name=region_name)
    return ecs


# run_fargate_task
def run_fargate_task(cluster_name, task_definition, aws_vpc_subnets: list, aws_vpc_security_group: str):
    print('run_fargate_task: cluster_name: %s' % cluster_name)
    print('run_fargate_task: task_definition: %s' % task_definition)
    print('run_fargate_task: aws_vpc_subnets: %s' % aws_vpc_subnets)
    print('run_fargate_task: aws_vpc_security_group: %s' % aws_vpc_security_group)
    client = get_ecs_client()
    try:
        response = client.run_task(
            cluster=cluster_name,
            launchType = 'FARGATE',
            taskDefinition=task_definition,
            count = 1,
            platformVersion='LATEST',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': aws_vpc_subnets,
                    'securityGroups': [aws_vpc_security_group],
                    'assignPublicIp': 'ENABLED'
                }
            },
            overrides={
                'containerOverrides': [],
            },
        )
        print('run ecs task response: %s' % str(response))
        return True
    except BaseException as exp:
        print(exp)
        return False
