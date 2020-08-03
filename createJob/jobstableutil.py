import boto3
from botocore.exceptions import ClientError
import uuid


# hard code table name for now
def get_jobs_table():
    dynamodb = boto3.resource('dynamodb')
    jobs_table = dynamodb.Table('jobs-list-jobs-table-rwang5688-dev')
    return jobs_table


def create_job_record(jobs_table, event_record):
    global job_record
    job_record = {}
    job_id = str(uuid.uuid4())
    job_record['id'] = job_id
    job_record['sender_id'] = event_record['Attributes']['SenderId']
    job_record['sent_timestamp'] = event_record['Attributes']['SentTimestamp']
    event_body = eval(event_record['Body'])
    job_record['source'] = event_body['job']['source']
    job_record['job_status'] = 'created'
    jobs_table.put_item(Item=job_record)
    return job_id


def get_job_record(jobs_table, job_id):
    response = jobs_table.get_item(
        Key={
            'id': job_id
        }
    )
    item = response['Item']
    return item


def update_job_status(jobs_table, job_id, job_status):
    jobs_table.update_item(
        Key={
            'id': job_id
        },
        UpdateExpression='SET job_status = :val1',
        ExpressionAttributeValues={
            ':val1': job_status
        }
    )
    return True

