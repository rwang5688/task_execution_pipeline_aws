import os
import boto3
from botocore.exceptions import ClientError
import uuid
import time


def get_task_table():
    dynamodb = boto3.resource('dynamodb')

    # set task table name
    task_table_name = ''
    if 'TASK_TABLE' in os.environ:
        if 'STAGE' in os.environ:
            task_table_name = os.environ['TASK_TABLE'] + '-' + os.environ['STAGE']
    print(f'get_task_table: table name is {task_table_name}.')

    # get and return task table
    task_table = dynamodb.Table(task_table_name)
    if task_table is None:
        print(f'get_task_table: {task_table_name} is missing.')
        return None
    return task_table


def create_task_record(task_table, task_tool, task_source, submitter_id, submit_timestamp):
    # populate job record
    task_record = {}
    task_id = str(uuid.uuid4())
    task_record['task_id'] = task_id
    task_record['task_tool'] = task_tool
    task_record['task_source'] = task_source
    task_record['task_status'] = 'created'
    task_record['task_logfile'] = ''
    task_record['submitter_id'] = submitter_id
    task_record['submit_timestamp'] = submit_timestamp
    task_record['update_timestamp'] = time.time_ns() // 1000000

    # add to task table and return job id
    print(f'Job Record: {task_record}')
    task_table.put_item(Item=task_record)
    return task_id


def get_task_record(task_table, task_id):
    response = task_table.get_item(
        Key={
            'task_id': task_id
        }
    )
    item = response['Item']
    return item


def update_task_status(task_table, task_id, task_status, task_logfile):
    task_table.update_item(
        Key={
            'task_id': task_id
        },
        UpdateExpression='SET task_status = :val1, task_logfile = :val2, update_timestamp = :val3',
        ExpressionAttributeValues={
            ':val1': task_status,
            ':val2': task_logfile,
            ':val3': time.time_ns() // 1000000
        }
    )
    return True

