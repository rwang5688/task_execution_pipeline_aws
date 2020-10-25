import os
import subprocess
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
    global log_bucket_name
    global result_bucket_name
    global update_task_queue_name

    log_bucket_name = get_env_var('TASK_EXEC_LOG_DATA_BUCKET')
    if log_bucket_name == '':
        return False

    result_bucket_name = get_env_var('TASK_EXEC_RESULT_DATA_BUCKET')
    if result_bucket_name == '':
        return False

    update_task_queue_name = get_env_var('TASK_EXEC_UPDATE_TASK_QUEUE')
    if update_task_queue_name == '':
        return False

    # success
    return True


def parse_arguments():
    import argparse
    global user_id
    global task_id
    global task_status

    parser = argparse.ArgumentParser()
    parser.add_argument('user_id', help='The user id of the task to update.')
    parser.add_argument('task_id', help='The id of the task to update.')
    parser.add_argument('task_status', help='The status of the task to update.')

    args = parser.parse_args()
    user_id = args.user_id
    task_id = args.task_id
    task_status = args.task_status

    if user_id is None:
        print('parse_arguments: user_id is missing.')
        return False

    if task_id is None:
        print('parse_arguments: task_id is missing.')
        return False

    if task_status is None:
        print('parse_arguments: task_status is missing.')
        return False

    # success
    return True


def init_task(user_id, task_id, task_status):
    task = {}
    task['user_id'] = user_id
    task['task_id'] = task_id
    task['task_status'] = task_status
    task['task_dot_scan_log_tar'] = '.scan_log.tar.gz'
    task['task_scan_result_tar'] = 'scan_result.tar.gz'
    return task


def main():
    print('\nStarting task_result.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'log_bucket_name: {log_bucket_name}')
    print(f'result_bucket_name: {result_bucket_name}')
    print(f'update_task_queue_name: {update_task_queue_name}')

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print(f'user_id: {user_id}')
    print(f'task_id: {task_id}')
    print(f'task_status: {task_status}')

    task = init_task(user_id, task_id, task_status)

    task_file_attribute_name = 'task_dot_scan_log_tar'
    success = taskfile.upload_task_file(log_bucket_name, task, task_file_attribute_name)
    if not success:
        print(f'upload_task_file failed: {task_file_attribute_name}.  Exit.')
        return

    task_file_attribute_name = 'task_scan_result_tar'
    success = taskfile.upload_task_file(result_bucket_name, task, task_file_attribute_name)
    if not success:
        print(f'upload_task_file failed: {task_file_attribute_name}.  Exit.')
        return

    action = 'update'
    success = taskmessage.send_task_message(update_task_queue_name, action, task)
    if not success:
        print('send_task_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

