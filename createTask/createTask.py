import os
import logging
import jsonpickle
import boto3
from botocore.exceptions import ClientError
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
import s3util
import sqsutil
import tasktable


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


def parse_event_record(event_record):
    global task_tool
    global task_source
    global submitter_id
    global submit_timestamp

    event_body = eval(event_record['body'])
    if event_body is None:
        print('parse_event: event body is missing.')
        return False

    task = event_body['task']
    if task is None:
        print('parse_event: task is missing.')
        return False

    task_tool = task['task_tool']
    if task_tool is None:
        print('parse_message: task tool is missing.')
        return False

    task_source = task['task_source']
    if task_source is None:
        print('parse_message: task source is missing.')
        return False

    event_attributes = event_record['attributes']
    if event_attributes is None:
        print('parse_event: event attributes are missing.')
        return False

    submitter_id = event_attributes['SenderId']
    if submitter_id is None:
        print('parse_event: sender id is missing.')
        return False

    submit_timestamp = event_attributes['SentTimestamp']
    if submit_timestamp is None:
        print('parse_event: sent timestamp is missing.')
        return False

    # success
    return True


def send_message(queue_name, item):
    # get queue url
    sqsutil.list_queues()
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'send_message: Queue {queue_name} does not exist.')
        return False

    # send message
    message_body = {
        "action": "process",
        "task": {
            "task_id": item['task_id'],
            "task_tool": item['task_tool'],
            "task_source": item['task_source']
        }
    }
    message_id = sqsutil.send_message(queue_url, str(message_body))
    print(f'MessageId: {message_id}')
    print(f'MessageBody: {message_body}')

    # debug: receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print(f'send_message: cannot retrieve sent messge.')
        return False
    print('Received message:')
    print(message)

    # success
    return True


# createTask handler
def createTask(event, context):
    success = preamble(event, context)
    if not success:
        print('preamble failed. Exit.')
        return False

    # get task table
    task_table = tasktable.get_task_table()
    if task_table is None:
        print('get_task_table failed.  Exit.')
        return False

    # create task record
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

        # debug: print task record attributes
        print('Task record attributes:')
        print(f'task_tool: {task_tool}')
        print(f'task_source: {task_source}')
        print(f'submitter_id: {submitter_id}')
        print(f'submit_timestamp: {submit_timestamp}')

        # create task record
        task_id = tasktable.create_task_record(task_table, task_tool, task_source, submitter_id, submit_timestamp)
        if task_id is None:
            print('create_task_record failed.  Next.')
            continue

        # debug: get and print task record
        item = tasktable.get_task_record(task_table, task_id)
        if item is None:
            print('get_task_record failed.  Next.')
            continue
        print('Task record:')
        print(item)

        # set process task queue name
        queue_name = ''
        if 'PROCESS_TASK_QUEUE' in os.environ:
            queue_name = os.environ['PROCESS_TASK_QUEUE']

        # send task context to process task queue
        success = send_message(queue_name, item)
        if not success:
            print('send_message failed.  Next.')
            continue

        # TO DO:
        # Start ECS task to process task!!!

        # update task status
        task_status = "started"
        task_logfile = ""
        success = tasktable.update_task_status(task_table, task_id, task_status, task_logfile)
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

