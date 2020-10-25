import os
import logging
import jsonpickle
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import taskfile
import taskissue
import taskmessage


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


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print(f'get_env_var: Failed to get {env_var_name}.')
    return env_var


def get_env_vars():
    global result_bucket_name
    global generate_task_summary_queue_name

    result_bucket_name = get_env_var('RESULT_DATA_BUCKET')
    if result_bucket_name == '':
        return False

    generate_task_summary_queue_name = get_env_var('GENERATE_TASK_SUMMARY_QUEUE')
    if generate_task_summary_queue_name == '':
        return False

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


# upload_task_issues handler
def upload_task_issues(event, context):
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
    print(f'result_bucket_name: {result_bucket_name}')
    print(f'generate_task_summary_queue_name: {generate_task_summary_queue_name}')

    # get issue table
    issue_table = taskissue.get_issue_table()
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

        # get scan result tar blob in memory (max 3 GB)
        task_file_attribute_name = 'task_scan_result_tar'
        task[task_file_attribute_name] = 'scan_result.tar.gz'
        scan_result_tar_blob = taskfile.get_task_file_blob(result_bucket_name, task, task_file_attribute_name)
        if scan_result_tar_blob is None:
            print('get_task_file_blob failed.  Next.')
            continue

        # extract dot v files and write task issues
        success = taskissue.write_task_issues(issue_table, result_bucket_name, task, scan_result_tar_blob)
        if not success:
            print('write_task_issues failed.  Next.')
            continue

        # send task context to update task log stream queue
        action = 'generate_task_summary'
        success = taskmessage.send_task_message(generate_task_summary_queue_name, action, task)
        if not success:
            print('send_message failed.  Next.')
            continue

    # success
    return True


# main function for testing upload_task_issues handler
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
        result = upload_task_issues(event, context)
        # print response
        print('## RESPONSE')
        print(str(result))
    finally:
        file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

