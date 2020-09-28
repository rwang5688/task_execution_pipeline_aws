import os
import json
import copy
import uuid
import taskfile
import taskmessage


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print(f'get_env_var: Failed to get {env_var_name}.')
    return env_var


def get_env_vars():
    global preprocess_bucket_name
    global result_bucket_name
    global create_task_queue_name

    preprocess_bucket_name = get_env_var('TASK_EXEC_PREPROCESS_DATA_BUCKET')
    if preprocess_bucket_name == '':
        return False

    result_bucket_name = get_env_var('TASK_EXEC_RESULT_DATA_BUCKET')
    if result_bucket_name == '':
        return False

    create_task_queue_name = get_env_var('TASK_EXEC_CREATE_TASK_QUEUE')
    if create_task_queue_name == '':
        return False

    # success
    return True


def parse_arguments():
    import argparse
    global task_config_file_name

    parser = argparse.ArgumentParser()
    parser.add_argument('task_config_file_name', help='task config file name.')

    args = parser.parse_args()
    task_config_file_name = args.task_config_file_name

    if task_config_file_name is None:
        print('parse_arguments: task_config_file_name is missing.')
        return False

    # success
    return True


def get_json_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data
    return None


def main():
    print('\nStarting submitTask.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'preprocess_bucket_name: {preprocess_bucket_name}')
    print(f'result_bucket_name: {result_bucket_name}')
    print(f'create_task_queue_name: {create_task_queue_name}')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print(f'task_config_file_name: {task_config_file_name}')

    task_config = get_json_data(task_config_file_name)
    if task_config == None:
        print('get_json_data failed.  Exit.')
        return

    task = copy.deepcopy(task_config)
    task_id = str(uuid.uuid4())
    task['task_id'] = task_id

    print('Task:')
    print(task)

    task_file_attribute_name = 'task_source_fileinfo'
    success = taskfile.upload_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if not success:
        print(f'upload_task_file failed: {task_file_attribute_name}.  Exit.')
        return

    task_file_attribute_name = 'task_preprocess_tar'
    success = taskfile.upload_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if not success:
        print(f'upload_task_file failed: {task_file_attribute_name}.  Exit.')
        return

    task_file_attribute_name = 'task_source_code'
    success = taskfile.upload_task_file(result_bucket_name, task, task_file_attribute_name)
    if not success:
        print(f'upload_task_file failed: {task_file_attribute_name}.  Exit.')
        return

    action = 'create'
    success = taskmessage.send_task_message(create_task_queue_name, action, task)
    if not success:
        print('send_task_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

