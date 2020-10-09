import json
import sqsutil


def receive_task_message(queue_name):
    # get queue url
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'receive_task_message: {queue_name} does not exist.')
        return None

    # receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print('receive_task_message: cannot retrieve message.')
        return None

    # success
    return message


def get_task_from_message(message):
    # get message body
    message_body = eval(message['Body'])
    if message_body is None:
        print('receive_task_message: message body is missing.')
        return None

    # get task
    task = message_body['task']
    if task is None:
        print('receive_task_message: task is missing.')
        return None

    # success
    return task


def delete_task_message(queue_name, message):
    # get queue url
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'delete_task_message: {queue_name} does not exist.')
        return False

    # delete message
    sqsutil.delete_message(queue_url, message)
    return True


def send_task_message(queue_name, action, task):
    # get queue url
    queue_url = sqsutil.get_queue_url(queue_name)
    if queue_url is None:
        print(f'send_task_message: Queue {queue_name} does not exist.')
        return False

    # assume user_id and task_id are set
    message_body = {}
    message_body['action'] = action
    message_body['task'] = task

    # send message as json
    message_body_json = json.dumps(message_body)
    message_id = sqsutil.send_message(queue_url, message_body_json)
    print(f'MessageId: {message_id}')
    print(f'MessageBodyJSON: {message_body_json}')

    # debug: receive message
    message = sqsutil.receive_message(queue_url)
    if message is None:
        print(f'send_task_message: cannot retrieve sent messge.')
        print(f'(When downstream Lambda function is running, missing message is expected.)')
    print('Received message:')
    print(message)

    # success
    return True

