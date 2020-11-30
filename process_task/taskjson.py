import json


TASK_JSON_FILE_NAME="xcal-task.json"


def write_task_json(task):
    with open(TASK_JSON_FILE_NAME, mode="w") as task_json_file:
        if task_json_file is None:
            print("write_task_json: Failed to open %s." % TASK_JSON_FILE_NAME)
            return False

        json.dump(task, task_json_file)

    # success
    return True


def read_task_json():
    task = None

    with open(TASK_JSON_FILE_NAME, mode="r") as task_json_file:
        if task_json_file is None:
            print("read_task_json: Failed to open %s." % TASK_JSON_FILE_NAME)
            return False

        task = json.load(task_json_file)

    return task

