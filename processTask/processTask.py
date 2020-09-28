import os
import subprocess
import taskmessage
import taskfile


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print(f'get_env_var: Failed to get {env_var_name}.')
    return env_var


def get_env_vars():
    global preprocess_bucket_name
    global process_task_queue_name

    preprocess_bucket_name = get_env_var('TASK_EXEC_PREPROCESS_DATA_BUCKET')
    if preprocess_bucket_name == '':
        return False

    process_task_queue_name = get_env_var('TASK_EXEC_PROCESS_TASK_QUEUE')
    if process_task_queue_name == '':
        return False

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


def execute_task_tool(task):
    # get task_tool
    task_tool = ''
    if 'task_tool' in task:
        task_tool = task['task_tool']
    else:
        print('execute_task_tool: Missing task_tool.')
        return False

    # command: "$(task_tool)"
    process = subprocess.Popen([task_tool],
        shell=True,
        stdout=subprocess.PIPE, universal_newlines=True,
        env=os.environ)
    read_process_stdout(process)

    # success
    return True


def execute_task_callback(task_callback, user_id, task_id, task_status):
    # command: "python3 $(task_callback) $(user_id) $(task_id) $(task_status)"
    process = subprocess.Popen(["python3", task_callback, user_id, task_id, task_status],
        stdout=subprocess.PIPE, universal_newlines=True)
    read_process_stdout(process)

    # success
    return True


def main():
    print('\nStarting processTask.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print(f'preprocess_bucket_name: {preprocess_bucket_name}')
    print(f'process_task_queue_name: {process_task_queue_name}')

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

    task_file_attribute_name = 'task_source_fileinfo'
    task_file_name = taskfile.download_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print(f'download_task_file failed: {task_file_attribute_name}.  Exit.')
        return

    print(f'{task_file_attribute_name}: {task_file_name}')

    task_file_attribute_name = 'task_preprocess_tar'
    task_file_name = taskfile.download_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print(f'download_task_file failed: {task_file_attribute_name}.  Exit.')
        return

    print(f'{task_file_attribute_name}: {task_file_name}')

    success = set_env_vars(task)
    if not success:
        print('set_env_vars failed.  Exit.')
        return

    print(f'set_env_vars: {os.environ}')

    success = execute_task_tool(task)
    if not success:
        print('execute_task_tool failed.  Exit.')
        return

    task_tool = task['task_tool']
    print(f'execute_task_tool completed for {task_tool}.')

    task_callback = 'taskResult.py'
    user_id = task['user_id']
    task_id = task['task_id']
    task_status = 'completed'
    success = execute_task_callback(task_callback, user_id, task_id, task_status)
    if not success:
        print('execute_task_callback failed.  Exit.')
        return

    print(f'execute_task_callback completed for {task_callback}.')

    success = taskmessage.delete_task_message(process_task_queue_name, message)
    if not success:
        print('delete_task_message failed.  Exit.')
        return

    # success
    print('\nReceived and deleted message:')
    print(message)


if __name__ == '__main__':
    main()

