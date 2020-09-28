import os
import logging
import jsonpickle
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import tasktable
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
    global process_task_queue_name

    process_task_queue_name = get_env_var('PROCESS_TASK_QUEUE')
    if process_task_queue_name == '':
        return False

    # success
    return True


def parse_event_record(event_record):
    global task
    global submit_timestamp

    event_body = eval(event_record['body'])
    if event_body is None:
        print('parse_event: event body is missing.')
        return False

    task = event_body['task']
    if task is None:
        print('parse_event: task is missing.')
        return False

    event_attributes = event_record['attributes']
    if event_attributes is None:
        print('parse_event: event attributes are missing.')
        return False

    submit_timestamp = event_attributes['SentTimestamp']
    if submit_timestamp is None:
        print('parse_event: sent timestamp is missing.')
        return False

    # success
    return True


# createTask handler
def createTask(event, context):
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
    print(f'process_task_queue_name: {process_task_queue_name}')

    # get task table
    task_table = tasktable.get_task_table()
    if task_table is None:
        print('get_task_table failed.  Exit.')
        return False

    # create task records
    event_records = event['Records']
    for event_record in event_records:
        # debug: print event record
        print('Event record:')
        print(event_record)

        # parse event record
        success = parse_event_record(event_record)
        if not success:
            print('parse_event_record failed.  Next.')
            continue

        # debug: print event record attributes
        print('Event record attributes:')
        print(f'task: {task}')
        print(f'submit_timestamp: {submit_timestamp}')

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
        print('Task record:')
        print(task_record)

        # send task record to process task queue
        action = 'process'
        success = taskmessage.send_task_message(process_task_queue_name, action, task_record)
        if not success:
            print('send_message failed for process task queue.  Next.')
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


# main function for testing createTask handler
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
        result = createTask(event, context)
        # print response
        print('## RESPONSE')
        print(str(result))
    finally:
        file.close()
    file.close()
    xray_recorder.end_segment()


if __name__ == '__main__':
    main()

