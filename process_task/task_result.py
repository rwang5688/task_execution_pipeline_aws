import os
import subprocess
import cachefile
import taskfile
import taskjson
import taskmessage


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print('get_env_var: Failed to get %s.' % env_var_name)
    return env_var


def get_env_vars():
    global cache_bucket_name
    global log_bucket_name
    global result_bucket_name
    global update_task_queue_name

    cache_bucket_name = get_env_var('TASK_EXEC_CACHE_DATA_BUCKET')
    if cache_bucket_name == '':
        return False

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


def upload_cache_files(task):
    # cache: java_rt_lib
    cache_name = 'java_rt_lib'
    cache_id_attribute_name = 'java_rt_lib_id'
    cache_file_attribute_name = 'java_rt_out_tar'
    if cache_file_attribute_name not in task:
        print('upload_cache_files: No need for cache %s.' % cache_name)
        return True

    cache_file_blob = cachefile.get_cache_file_blob(cache_bucket_name, task, \
                        cache_name, cache_id_attribute_name, cache_file_attribute_name)
    if cache_file_blob is not None:
        print('upload_cache_files: Cache file exists for %s.' % cache_name)
        return True

    upload_file_name = cachefile.upload_cache_file(cache_bucket_name, task, \
                        cache_name, cache_id_attribute_name, cache_file_attribute_name, \
                        local_cache_dir="extra-object")
    if upload_file_name == '':
        print('upload_cache_files failed: %s.' % cache_file_attribute_name)
        return False

    # success
    return True


def upload_result_files(task):
    task_file_attribute_name = 'task_dot_scan_log_tar'
    task_file_name = taskfile.upload_task_file(log_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('upload_result_files failed: %s.' % task_file_attribute_name)
        return False

    task_file_attribute_name = 'task_scan_result_tar'
    task_file_name = taskfile.upload_task_file(result_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('upload_result_files failed: %s.' % task_file_attribute_name)
        return False

    # success
    return True


def main():
    print('\nStarting task_result.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print('cache_bucket_name: %s' % cache_bucket_name)
    print('log_bucket_name: %s' % log_bucket_name)
    print('result_bucket_name: %s' % result_bucket_name)
    print('update_task_queue_name: %s' % update_task_queue_name)

    task = taskjson.read_task_json()
    if task is None:
        print("read_task_json failed.  Exit.")
        return

    print("read_task_json completed.")

    print("task:")
    print(task)

    success = upload_cache_files(task)
    if not success:
        print('upload_cache_files failed: task=%s.  Exit.' % task)
        return

    success = upload_result_files(task)
    if not success:
        print('upload_result_files failed: task=%s.  Exit.' % task)
        return

    action = 'update'
    success = taskmessage.send_task_message(update_task_queue_name, action, task)
    if not success:
        print('send_task_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

