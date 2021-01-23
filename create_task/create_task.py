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
        print('get_env_var: Failed to get %s.' % env_var_name)
    return env_var


def get_env_vars():
    global cloud
    global process_task_queue_name
    global process_task_trigger_queue_name

    cloud = get_env_var('CLOUD')
    if cloud == '':
        return False

    process_task_queue_name = get_env_var('PROCESS_TASK_QUEUE')
    if process_task_queue_name == '':
        return False

    process_task_trigger_queue_name = get_env_var('PROCESS_TASK_TRIGGER_QUEUE')
    if process_task_trigger_queue_name == '':
        return False

    # success
    return True


def parse_event_record(event_record):
    global task
    global submit_timestamp

    event_body = eval(event_record['body'])
    if event_body is None:
        print('parse_event_record: event body is missing.')
        return False

    task = event_body['task']
    if task is None:
        print('parse_event_record: task is missing.')
        return False

    event_attributes = event_record['attributes']
    if event_attributes is None:
        print('parse_event_record: event attributes are missing.')
        return False

    submit_timestamp = event_attributes['SentTimestamp']
    if submit_timestamp is None:
        print('parse_event_record: sent timestamp is missing.')
        return False

    # success
    return True


# create_task handler
def create_task(event, context):
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
    print('cloud: %s' % cloud)
    print('process_task_queue_name: %s' % process_task_queue_name)
    print('process_task_trigger_queue_name: %s' % process_task_trigger_queue_name)

    # get task table
    task_table = tasktable.get_task_table()
    if task_table is None:
        print('get_task_table failed.  Exit.')
        return False

    # create task records
    event_records = event['Records']
    for event_record in event_records:
        # debug: print event record
        print('event_record: %s' % event_record)

        # parse event record
        success = parse_event_record(event_record)
        if not success:
            print('parse_event_record failed.  Next.')
            continue

        # debug: print event record attributes
        print('task: %s' % task)
        print('submit_timestamp: %s' % submit_timestamp)

        # create task record
        task_record = tasktable.create_task_record(task_table, task, submit_timestamp)
        if task_record is None:
            print('create_task_record failed.  Next.')
            continue

        # debug: get and print task record
        user_id = task_record['user_id']
        task_id = task_record['task_id']
        task_record = tasktable.get_task_record(task_table, user_id, task_id)
        if task_record is None:
            print('get_task_record failed.  Next.')
            continue
        print('task_record: %s' % task_record)

        task_fileinfo_json = task_record.get('task_fileinfo_json')
        task_fileinfo_json_url = taskurl.generate_preprocess_data_bucket_object_url(
                                        user_id, task_id, task_fileinfo_json)

        task_preprocess_tar = task_record.get('task_preprocess_tar')
        task_preprocess_tar_url = taskurl.generate_preprocess_data_bucket_object_url(
                                        user_id, task_id, task_preprocess_tar)

        task_source_code_zip = task_record.get('task_source_code_zip')
        task_source_code_zip_url = ""
        if task_source_code_zip is not None:
            task_source_code_zip_url = taskurl.generate_result_data_bucket_object_url(
                                            user_id, task_id, task_source_code_zip)

        success = tasktable.update_preprocess_urls(task_table, user_id, task_id,
                                                task_fileinfo_json_url,
                                                task_preprocess_tar_url,
                                                task_source_code_zip_url)
        if not success:
            print('update_preprocess_urls failed.  Next.')
            continue

        # get task record
        task_record = tasktable.get_task_record(task_table, user_id, task_id)
        if task_record is None:
            print('get_task_record failed.  Next.')
            continue
        print('task_record: %s' % task_record)

        # send task record to process task queue
        action = 'process'
        success = taskmessage.send_task_message(process_task_queue_name, action, task_record)
        if not success:
            print('send_message failed for process task queue.  Next.')
            continue

        # Note: Lambda with container image NOT available on aws-cn yet
        if cloud == 'aws':
            # send task record to process task trigger queue
            action = 'process'
            success = taskmessage.send_task_message(process_task_trigger_queue_name, action, task_record)
            if not success:
                print('send_message failed for process task trigger queue.  Next.')
                continue

        # Note: Start ECS Fargate cluster to process task.
        # ECS Fargate cluster appear to start a task as soon as process queue has message.

        # if send_task_message succeeds, update task status to "started"
        task_status = 'started'
        success = tasktable.update_task_status(task_table, user_id, task_id, task_status)
        if not success:
            print('update_task_status failed.  Next.')
            continue

    # success
    return True


# main function for testing create_task handler
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
        result = create_task(event, context)
        # print response
        print('## RESPONSE')
        print(str(result))
    finally:
        file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

