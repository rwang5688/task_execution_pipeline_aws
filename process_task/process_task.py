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
    global preprocess_bucket_name
    global cache_bucket_name
    global process_task_queue_name

    preprocess_bucket_name = get_env_var('TASK_EXEC_PREPROCESS_DATA_BUCKET')
    if preprocess_bucket_name == '':
        return False

    cache_bucket_name = get_env_var('TASK_EXEC_CACHE_DATA_BUCKET')
    if cache_bucket_name == '':
        return False

    process_task_queue_name = get_env_var('TASK_EXEC_PROCESS_TASK_QUEUE')
    if process_task_queue_name == '':
        return False

    # success
    return True


def download_preprocess_files(task):
    task_file_attribute_name = 'task_fileinfo_json'
    task_file_name = taskfile.download_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('download_task_file failed: %s.' % task_file_attribute_name)
        return False

    task_file_attribute_name = 'task_preprocess_tar'
    task_file_name = taskfile.download_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('download_task_file failed: %s.' % task_file_attribute_name)
        return False

    # success
    return True


def download_cache_files(task):
    # cache: java_rt_out first, then java_rt_lib
    cache_name = 'java_rt_lib'
    cache_id_attribute_name = 'java_rt_lib_id'
    cache_rt_lib_attribute_name = 'java_rt_lib_tar'
    cache_rt_out_attribute_name = 'java_rt_out_tar'
    if (cache_rt_out_attribute_name and cache_rt_lib_attribute_name) not in task:
        print('download_cache_files: No need for cache %s.' % cache_name)
        return True

    # first try downloading rt_o.tgz
    download_file_name = cachefile.download_cache_file(cache_bucket_name, task,
                        cache_name, cache_id_attribute_name, cache_rt_out_attribute_name)
    if download_file_name == '':
        # next try downloading rt.tgz
        print('download_cache_files failed: %s.' % cache_rt_out_attribute_name)
        download_file_name = cachefile.download_cache_file(cache_bucket_name, task,
                            cache_name, cache_id_attribute_name, cache_rt_lib_attribute_name)
        if download_file_name == '':
            # error
            print('download_cache_files failed: %s.' % cache_rt_lib_attribute_name)
            return False

    # success
    return True


def set_env_vars(task):
    task_id = ''
    if 'task_id' in task:
        task_id = task['task_id']
    else:
        print('set_env_vars: Missing task_id.')
        return False
    os.environ['SCAN_TASK_ID'] = task_id

    if 'task_extra_options' in task:
        task_extra_options = task['task_extra_options']
        for task_extra_option in task_extra_options:
            os.environ[task_extra_option] = task_extra_options[task_extra_option]

    #env = dict(os.environ)   # Make a copy of the current environment
    #subprocess.Popen(['python3', '-m', 'Pyro4.naming'], env=env)

    # success
    return True


def read_process_stdout(process):
    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break
    return return_code


def execute_task_tool(task):
    # get task_tool
    if "task_tool" in task:
        task_tool = task["task_tool"]
    else:
        print('execute_task_tool: Missing task_tool.')
        return False

    # command: "$(task_tool)"
    process = subprocess.Popen([task_tool],
        shell=True,
        stdout=subprocess.PIPE, universal_newlines=True,
        env=os.environ)
    return_code = read_process_stdout(process)

    # for now: always set task_status to "completed"
    # later: read task_status from executing task_tool
    if return_code == 0:
        task["task_status"] = "completed"
        # success
        return True
    else:
        task["task_status"] = "scan-failed"
        return False


def execute_task_callback(task_callback):
    # command: "python3 $(task_callback)"
    process = subprocess.Popen(["python3", task_callback],
        stdout=subprocess.PIPE, universal_newlines=True)
    return_code = read_process_stdout(process)
    if return_code != 0:
        return False
    else:
        # success
        return True


def main():
    print('\nStarting process_task.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print('preprocess_bucket_name: %s' % preprocess_bucket_name)
    print('cache_bucket_name: %s' % cache_bucket_name)
    print('process_task_queue_name: %s' % process_task_queue_name)

    message = taskmessage.receive_task_message(process_task_queue_name)
    if message is None:
        print('receive_task_message failed.  Exit.')
        return

    print('Message:')
    print(message)

    task = taskmessage.get_task_from_message(message)
    if task is None:
        print('get_task_from_message failed.  Exit.')
        return

    print('Task:')
    print(task)

    success = download_preprocess_files(task)
    if not success:
        print('download_preprocess_files failed.  Exit.')
        return

    # tar -xvzf doesn't work properly in Windows Bash
    # need to add the tar command to xvsa_start.sh
    success = download_cache_files(task)
    if not success:
        print('download_cache_files failed.  Exit.')
        return

    success = set_env_vars(task)
    if not success:
        print('set_env_vars failed.  Exit.')
        return

    print('set_env_vars: %s' % os.environ)

    success = execute_task_tool(task)
    if not success:
        print('execute_task_tool failed.')

    task_tool = task["task_tool"]
    task_status = task["task_status"]
    print('execute_task_tool completed for task_tool=%s with task_status=%s.' % (task_tool, task_status))

    success = taskjson.write_task_json(task)
    if not success:
        print("write_task_json failed.  Exit.")
        return

    print('write_task_json completed for task_tool=%s with task_status=%s.' % (task_tool, task_status))

    task_callback = 'task_result.py'
    success = execute_task_callback(task_callback)
    if not success:
        print('execute_task_callback failed.')

    print('execute_task_callback completed for %s.' % task_callback)

    success = taskmessage.delete_task_message(process_task_queue_name, message)
    if not success:
        print('delete_task_message failed.  Exit.')
        return

    # success
    print('\nReceived and deleted message:')
    print(message)


if __name__ == '__main__':
    main()

