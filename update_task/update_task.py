import os
import logging
import jsonpickle
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import tasktable
import taskurl
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
    global upload_task_issues_queue_name

    upload_task_issues_queue_name = get_env_var('UPLOAD_TASK_ISSUES_QUEUE')
    if upload_task_issues_queue_name == '':
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


# update_task handler
def update_task(event, context):
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
    print(f'upload_task_issues_queue_name: {upload_task_issues_queue_name}')

    # get task table
    task_table = tasktable.get_task_table()
    if task_table is None:
        print('get_task_table failed.  Exit.')
        return False

    # update task records
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

        # update task status
        user_id = task['user_id']
        task_id = task['task_id']
        task_status = task['task_status']
        success = tasktable.update_task_status(task_table, user_id, task_id, task_status)
        if not success:
            print('update_task_status failed.  Next.')
            continue

        # get task record
        task_record = tasktable.get_task_record(task_table, user_id, task_id)
        if task_record is None:
            print('get_task_record failed.  Next.')
            continue
        print('Task record:')
        print(task_record)

        task_dot_scan_log_tar = task_record['task_dot_scan_log_tar']
        task_dot_scan_log_tar_url = taskurl.generate_log_data_bucket_object_url(user_id, task_id, task_dot_scan_log_tar)

        task_summary_pdf = task_record['task_summary_pdf']
        task_summary_pdf_url = taskurl.generate_result_data_bucket_object_url(user_id, task_id, task_summary_pdf)

        task_issues_csv = task_record['task_issues_csv']
        task_issues_csv_url = taskurl.generate_result_data_bucket_object_url(user_id, task_id, task_issues_csv)

        success = tasktable.update_task_urls(task_table, user_id, task_id, task_dot_scan_log_tar_url, task_summary_pdf_url, task_issues_csv_url)
        if not success:
            print('update_task_urls failed.  Next.')
            continue

        # get task record
        task_record = tasktable.get_task_record(task_table, user_id, task_id)
        if task_record is None:
            print('get_task_record failed.  Next.')
            continue
        print('Task record:')
        print(task_record)

        # send task record to upload task issues queue
        action = 'upload_task_issues'
        success = taskmessage.send_task_message(upload_task_issues_queue_name, action, task_record)
        if not success:
            print('send_message failed.  Next.')
            continue

    # success
    return True


# main function for testing update_task handler
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
        result = update_task(event, context)
        # print response
        print('## RESPONSE')
        print(str(result))
    finally:
        file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

