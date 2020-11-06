import os
import subprocess
import taskfile
import taskmessage


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print('get_env_var: Failed to get %s.' % env_var_name)
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
    global task_dot_scan_log_tar
    global task_scan_result_tar

    parser = argparse.ArgumentParser()
    parser.add_argument('user_id', help='The user id of the task to update.')
    parser.add_argument('task_id', help='The id of the task to update.')
    parser.add_argument('task_status', help='The status of the task to update.')
    parser.add_argument('task_dot_scan_log_tar', help='The scan log tar of the task to update.')
    parser.add_argument('task_scan_result_tar', help='The scan result tar of the task to update.')

    args = parser.parse_args()
    user_id = args.user_id
    task_id = args.task_id
    task_status = args.task_status
    task_dot_scan_log_tar = args.task_dot_scan_log_tar
    task_scan_result_tar = args.task_scan_result_tar

    if user_id is None:
        print('parse_arguments: user_id is missing.')
        return False

    if task_id is None:
        print('parse_arguments: task_id is missing.')
        return False

    if task_status is None:
        print('parse_arguments: task_status is missing.')
        return False

    if task_dot_scan_log_tar is None:
        print('parse_arguments: task_dot_scan_log_tar is missing.')
        return False

    if task_scan_result_tar is None:
        print('parse_arguments: task_scan_result_tar is missing.')
        return False

    # success
    return True


def init_task(user_id, task_id, task_status, task_dot_scan_log_tar, task_scan_result_tar):
    task = {}
    task['user_id'] = user_id
    task['task_id'] = task_id
    task['task_status'] = task_status
    task['task_dot_scan_log_tar'] = task_dot_scan_log_tar
    task['task_scan_result_tar'] = task_scan_result_tar
    return task


def main():
    print('\nStarting task_result.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print('log_bucket_name: %s' % log_bucket_name)
    print('result_bucket_name: %s' % result_bucket_name)
    print('update_task_queue_name: %s' % update_task_queue_name)

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print('user_id: %s' % user_id)
    print('task_id: %s' % task_id)
    print('task_status: %s' % task_status)
    print('task_dot_scan_log_tar: %s' % task_dot_scan_log_tar)
    print('task_scan_result_tar: %s' % task_scan_result_tar)

    task = init_task(user_id, task_id, task_status, task_dot_scan_log_tar, task_scan_result_tar)

    task_file_attribute_name = 'task_dot_scan_log_tar'
    success = taskfile.upload_task_file(log_bucket_name, task, task_file_attribute_name)
    if not success:
        print('upload_task_file failed: %s.  Exit.' % task_file_attribute_name)
        return

    task_file_attribute_name = 'task_scan_result_tar'
    success = taskfile.upload_task_file(result_bucket_name, task, task_file_attribute_name)
    if not success:
        print('upload_task_file failed: %s.  Exit.' % task_file_attribute_name)
        return

    action = 'update'
    success = taskmessage.send_task_message(update_task_queue_name, action, task)
    if not success:
        print('send_task_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

