import os
import json
import copy
import uuid
import cachefile
import taskfile
import taskmessage


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print('get_env_var: Failed to get %s' % env_var_name)
    return env_var


def get_env_vars():
    global preprocess_bucket_name
    global cache_bucket_name
    global result_bucket_name
    global create_task_queue_name

    preprocess_bucket_name = get_env_var('TASK_EXEC_PREPROCESS_DATA_BUCKET')
    if preprocess_bucket_name == '':
        return False

    cache_bucket_name = get_env_var('TASK_EXEC_CACHE_DATA_BUCKET')
    if cache_bucket_name == '':
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
    global task_conf_file_name

    parser = argparse.ArgumentParser()
    parser.add_argument('task_conf_file_name', help='task conf file name.')

    args = parser.parse_args()
    task_conf_file_name = args.task_conf_file_name

    if task_conf_file_name is None:
        print('parse_arguments: task_conf_file_name is missing.')
        return False

    # success
    return True


def get_json_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data
    return None


def upload_preprocess_files(task):
    task_file_attribute_name = 'task_fileinfo_json'
    task_file_name = taskfile.upload_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('upload_task_file failed: %s.' % task_file_attribute_name)
        return False

    task_file_attribute_name = 'task_preprocess_tar'
    task_file_name = taskfile.upload_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('upload_task_file failed: %s.' % task_file_attribute_name)
        return False

    task_file_attribute_name = 'task_source_code_zip'
    task_file_name = taskfile.upload_task_file(result_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('upload_task_file failed: %s.' % task_file_attribute_name)
        return False

    return True


def upload_cache_files(task):
    # cache: java_rt_lib
    cache_name = 'java_rt_lib'
    cache_id_attribute_name = 'task_rt_lib_id'
    cache_file_attribute_name = 'task_rt_lib_tar'
    if cache_file_attribute_name not in task:
        print('upload_cache_file: No need for cache %s.' % cache_name)
        return True

    cache_file_blob = cachefile.get_cache_file_blob(cache_bucket_name, task, \
                        cache_name, cache_id_attribute_name, cache_file_attribute_name)
    if cache_file_blob is not None:
        print('upload_cache_file: Cache file exists for %s.' % cache_name)
        return True

    cache_file_name = cachefile.upload_cache_file(cache_bucket_name, task, \
                        cache_name, cache_id_attribute_name, cache_file_attribute_name)
    if cache_file_name == '':
        print('upload_cache_file failed: %s.' % cache_file_attribute_name)
        return False

    # success
    return True


def main():
    print('\nStarting submit_task.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print('preprocess_bucket_name: %s' % preprocess_bucket_name)
    print('result_bucket_name: %s' % result_bucket_name)
    print('create_task_queue_name: %s' % create_task_queue_name)

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print('task_conf_file_name: %s' % task_conf_file_name)

    task_conf = get_json_data(task_conf_file_name)
    if task_conf == None:
        print('get_json_data failed.  Exit.')
        return

    task = copy.deepcopy(task_conf)
    task_id = task['task_id']
    if task_id == 'uuid':
        # need to generate task_id
        task_id = str(uuid.uuid4())
        task['task_id'] = task_id

    print('Task:')
    print(task)

    success = upload_preprocess_files(task)
    if not success:
        print('upload_preprocess_files failed: task=%s.  Exit.' % task)
        return

    success = upload_cache_files(task)
    if not success:
        print('upload_cache_files failed: task=%s.  Exit.' % task)
        return

    action = 'create'
    success = taskmessage.send_task_message(create_task_queue_name, action, task)
    if not success:
        print('send_task_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

