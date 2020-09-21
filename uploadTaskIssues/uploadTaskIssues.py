import os
import logging
import jsonpickle
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import tarfile
from io import BytesIO
from io import StringIO
import json
import s3util
import sqsutil
import dotvfile
import issuetable


logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()


def preamble(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    logger.info('## EVENT\r' + jsonpickle.encode(event))
    logger.info('## CONTEXT\r' + jsonpickle.encode(context))
    client = boto3.client('lambda')
    account_settings = client.get_account_settings()
    print(account_settings['AccountUsage'])
    return True


def get_env_vars():
    global result_data_bucket_name

    result_data_bucket_name = ''
    if 'RESULT_DATA_BUCKET' in os.environ:
        result_data_bucket_name = os.environ['RESULT_DATA_BUCKET']

    # success
    return True


def parse_event_record(event_record):
    global task

    event_body = eval(event_record['body'])
    if event_body is None:
        print('parse_event: event body is missing.')
        return False

    task = event_body['task']
    if task is None:
        print('parse_event: task is missing.')
        return False

    # success
    return True


def get_scan_result_tar_content(bucket_name, task):
    # get bucket
    s3util.list_buckets()
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print(f'get_scan_result_tar_content: Bucket {bucket_name} does not exist.')
        return None

    # get folder $(user_id)/$(task_id)
    user_id = task['user_id']
    task_id = task['task_id']

    # get scan result tar file in memory
    scan_result_tar = 'scan_result.tar.gz'
    object_key = user_id + "/" + task_id + "/" + scan_result_tar
    s3 = s3util.get_s3_client()
    scan_result_tar_file = s3.get_object(Bucket = bucket_name, Key = object_key)
    if scan_result_tar_file is None:
        print(f'get_scan_result_tar_content: Failed to get scan result tar content {scan_result_tar}')

    # return scan result tar content (blob)
    scan_result_tar_content = scan_result_tar_file['Body'].read()
    return scan_result_tar_content


def write_task_issues(issue_table, task, scan_result_tar_content):
    # initialize issue key
    task_id = task['task_id']
    task_issue_number = 1

    # foreach dot v file, get, convert and write dot v file issues
    with tarfile.open(fileobj = BytesIO(scan_result_tar_content)) as tar:
        for tar_resource in tar:
            if (tar_resource.isfile()):
                # extract dot v file blob from tar resource
                dot_v_file_bytes = tar.extractfile(tar_resource).read()
                # load convert dot v file blob to a json object
                dot_v_file_json = json.loads(dot_v_file_bytes)
                print(f'dot_v_file_json: {dot_v_file_json}')
                # write dot v file issues and return next task_issue_number
                task_issue_number = dotvfile.write_dot_v_file_issues(issue_table,
                    task_id, task_issue_number, dot_v_file_json)

    # success
    return True


# uploadTaskIssues handler
def uploadTaskIssues(event, context):
    success = preamble(event, context)
    if not success:
        print('preamble failed. Exit.')
        return False

    # get env vars
    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return False

    print('Env vars:')
    print(f'result_data_bucket_name: {result_data_bucket_name}')

    # get issue table
    issue_table = issuetable.get_issue_table()
    if issue_table is None:
        print('get_issue_table failed.  Exit.')
        return False

    # get and write task issue records
    event_records = event['Records']
    for event_record in event_records:
        # debug: print event record
        print('Event record:')
        print(event_record)

        # parse event record
        success = parse_event_record(event_record)
        if not success:
            print('parse_event_record failed.  Exit.')
            continue

        # debug: print event record attributes
        print('Event record attributes:')
        print(f'task: {task}')

        # get scan result tar content in memory (max 3 GB)
        scan_result_tar_content = get_scan_result_tar_content(result_data_bucket_name, task)
        if scan_result_tar_content is None:
            print('get_scan_result_tar_content failed.  Next.')
            continue

        # extract dot v files and write task issues
        success = write_task_issues(issue_table, task, scan_result_tar_content)
        if not success:
            print('write_task_issues failed.  Next.')
            continue

    # success
    return True


# main function for testing updateTask handler
def main():
    xray_recorder.begin_segment('main_function')
    file = open('event.json', 'rb')
    try:
        # read sample event
        ba = bytearray(file.read())
        event = jsonpickle.decode(ba)
        logger.warning('## EVENT')
        logger.warning(jsonpickle.encode(event))
        # create sample context
        context = {'requestid': '1234'}
        # invoke handler
        result = uploadTaskIssues(event, context)
        # print response
        print('## RESPONSE')
        print(str(result))
    finally:
        file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

