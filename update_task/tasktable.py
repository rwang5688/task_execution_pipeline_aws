import os
import boto3
from botocore.exceptions import ClientError
import copy
import time


def get_task_table():
    dynamodb = boto3.resource('dynamodb')

    # set task table name
    task_table_name = ''
    if 'TASK_TABLE' in os.environ:
        task_table_name = os.environ['TASK_TABLE']
    print(f'get_task_table: table name is {task_table_name}.')

    # get and return task table
    task_table = dynamodb.Table(task_table_name)
    if task_table is None:
        print(f'get_task_table: {task_table_name} is missing.')
        return None
    return task_table


def create_task_record(task_table, task, submit_timestamp):
    # create a deep copy of task and append status and timestamp
    task_record = copy.deepcopy(task)
    task_record['task_status'] = 'created'
    task_record['submit_timestamp'] = submit_timestamp
    task_record['update_timestamp'] = str(time.time_ns() // 1000000)

    # add to task table and return task id
    print(f'Task Record: {task_record}')
    task_table.put_item(Item=task_record)

    return task_record


def get_task_record(task_table, user_id, task_id):
    response = task_table.get_item(
        Key={
            'user_id': user_id,
            'task_id': task_id
        }
    )
    task_record = response['Item']
    return task_record


def update_task_status(task_table, user_id, task_id, task_status):
    task_table.update_item(
        Key={
            'user_id': user_id,
            'task_id': task_id
        },
        UpdateExpression='SET task_status = :val1, update_timestamp = :val2',
        ExpressionAttributeValues={
            ':val1': task_status,
            ':val2': str(time.time_ns() // 1000000)
        }
    )
    return True


def update_task_urls(task_table, user_id, task_id, task_dot_scan_log_tar_url, task_summary_pdf_url, task_issues_csv_url):
    task_table.update_item(
        Key={
            'user_id': user_id,
            'task_id': task_id
        },
        UpdateExpression='SET task_dot_scan_log_tar_url = :val1, task_summary_pdf_url = :val2, task_issues_csv_url = :val3',
        ExpressionAttributeValues={
            ':val1': task_dot_scan_log_tar_url,
            ':val2': task_summary_pdf_url,
            ':val3': task_issues_csv_url
        }
    )
    return True

