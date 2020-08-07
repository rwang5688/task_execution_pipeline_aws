import os
import boto3
from botocore.exceptions import ClientError
import uuid
import time


def get_jobs_table():
    dynamodb = boto3.resource('dynamodb')

    # set jobs table name
    jobs_table_name = 'jobs-list-jobs-table-rwang5688-dev'
    if 'JOBS_TABLE' in os.environ:
        if 'STAGE' in os.environ:
            jobs_table_name = os.environ['JOBS_TABLE'] + '-' + os.environ['STAGE']
    print(f'get_jobs_table: table name is {jobs_table_name}.')

    # get and return jobs table
    jobs_table = dynamodb.Table(jobs_table_name)
    if jobs_table is None:
        print(f'get_jobs_table: {jobs_table_name} is missing.')
        return None
    return jobs_table


def create_job_record(jobs_table, job_tool, job_source, submitter_id, submit_timestamp):
    # populate job record
    job_record = {}
    job_id = str(uuid.uuid4())
    job_record['job_id'] = job_id
    job_record['job_tool'] = job_tool
    job_record['job_source'] = job_source
    job_record['job_status'] = 'created'
    job_record['job_logfile'] = ''
    job_record['submitter_id'] = submitter_id
    job_record['submit_timestamp'] = submit_timestamp
    job_record['update_timestamp'] = time.time_ns() // 1000000

    # add to jobs table and return job id
    print(f'Job Record: {job_record}')
    jobs_table.put_item(Item=job_record)
    return job_id


def get_job_record(jobs_table, job_id):
    response = jobs_table.get_item(
        Key={
            'job_id': job_id
        }
    )
    item = response['Item']
    return item


def update_job_status(jobs_table, job_id, job_status, job_logfile):
    jobs_table.update_item(
        Key={
            'job_id': job_id
        },
        UpdateExpression='SET job_status = :val1, job_logfile = :val2, update_timestamp = :val3',
        ExpressionAttributeValues={
            ':val1': job_status,
            ':val2': job_logfile,
            ':val3': time.time_ns() // 1000000
        }
    )
    return True

