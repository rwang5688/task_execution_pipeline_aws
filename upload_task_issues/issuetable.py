import os
import logging
import boto3
from botocore.exceptions import ClientError
import copy


def get_issue_table():
    dynamodb = boto3.resource('dynamodb')

    # set issue table name
    issue_table_name = ''
    if 'ISSUE_TABLE' in os.environ:
        issue_table_name = os.environ['ISSUE_TABLE']
    print('get_issue_table: table name is %s.' % issue_table_name)

    # get and return issue table
    issue_table = dynamodb.Table(issue_table_name)
    if issue_table is None:
        print('get_issue_table: %s is missing.' % issue_table_name)
        return None
    return issue_table


def write_issue_record(issue_table, issue):
    try:
        # deep copy issue to issue record
        issue_record = copy.deepcopy(issue)

        # add to issue table and return issue record
        print('issue_record: %s' % issue_record)
        issue_table.put_item(Item=issue_record)

        return issue_record
    except ClientError as err:
        logging.error(err)
        return False
    except Exception as err:
        logging.error(err)
        return False


def get_issue_record(issue_table, task_id, task_issue_number):
    try:
        response = issue_table.get_item(
            Key={
                'task_id': task_id,
                'task_issue_number': task_issue_number
            }
        )
        issue_record = response['Item']
        return issue_record
    except ClientError as err:
        logging.error(err)
        return None
    except Exception as err:
        logging.error(err)
        return None


def batch_write_issue_records(issue_table, issues):
    try:
        with issue_table.batch_writer() as batch:
            for issue in issues:
                batch.put_item(Item=issue)
        return True
    except ClientError as err:
        logging.error(err)
        return False
    except Exception as err:
        logging.error(err)
        return False

