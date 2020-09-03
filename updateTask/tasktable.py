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


def create_task_record(task_table, task, submitter_id, submit_timestamp):
    # populate task record
    # side-effect: this is actually a copy by reference, which causes changes to task :(
    task_record = task
    task_record['task_status'] = 'created'
    task_record['submitter_id'] = submitter_id
    task_record['submit_timestamp'] = submit_timestamp
    task_record['update_timestamp'] = str(time.time_ns() // 1000000)

    # add to task table and return task id
    print(f'Task Record: {task_record}')
    task_table.put_item(Item=task_record)

    task_id = task_record['task_id']
    return task_id


def get_task_record(task_table, task_id):
    response = task_table.get_item(
        Key={
            'task_id': task_id
        }
    )
    item = response['Item']
    return item


def update_task_status(task_table, task_id, task_status):
    task_table.update_item(
        Key={
            'task_id': task_id
        },
        UpdateExpression='SET task_status = :val1, update_timestamp = :val2',
        ExpressionAttributeValues={
            ':val1': task_status,
            ':val2': str(time.time_ns() // 1000000)
        }
    )
    return True

