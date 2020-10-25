import json
import dotvfile
import csvfile


def parse_arguments():
    import argparse
    global task_id

    parser = argparse.ArgumentParser()
    parser.add_argument('task_id', help='task id (root of the dot v file).')

    args = parser.parse_args()
    task_id = args.task_id

    if task_id is None:
        print('parse_arguments: task_id is missing.')
        return False

    # success
    return True


def read_dot_v_file_json(task_id):
    # file name: $(task_id).v
    json_file_name = task_id + '.v'

    # read dot v file
    with open(json_file_name, mode='r') as dot_v_file:
        if dot_v_file is None:
            print('write_task_issues_csv_header: Failed to open csv file.')
            return None

        # read dot v file json
        dot_v_file_json = json.load(dot_v_file)
        return dot_v_file_json


def main():
    print('Starting dotvfile_to_csvfile...')

    # get task id from command line
    success = parse_arguments()
    if not success:
        print('dotvfile_to_csvfile: parse_arguments failed.  Exit.')
        return

    print(f'task_id: {task_id}')

    # read dot v file json
    dot_v_file_json = read_dot_v_file_json(task_id)
    if dot_v_file_json is None:
        print('dotvfile_to_csvfile: read_dot_v_file_json failed.  Exit.')
        return

    # initialize task issue number
    task_issue_number = 1
    print(f'Starting task_issue_number: {task_issue_number}.')

    # write csv file header
    csv_file_name = task_id + '_issues.csv'
    success = csvfile.write_task_issues_csv_header(csv_file_name)
    if not success:
        print('dotvfile_to_csvfile: write_task_issues_csv_header failed.  Exit.')
        return

    # decode dot v file issues
    task_issues = dotvfile.decode_dot_v_file_issues(task_id, task_issue_number, dot_v_file_json)
    if task_issues is None:
        print('write_task_issues: decode_dot_v_file_issues failed.  Next.')
        return

    # write to csv file
    success = csvfile.append_task_issues_csv_rows(csv_file_name, task_issues)
    if not success:
        print('dotvfile_to_csvfile: append_task_issues_csv_rows failed.  Next.')
        return

    # update task issue number
    num_task_issues = len(task_issues)
    task_issue_number += num_task_issues
    print(f'Wrote {num_task_issues} issues.')
    print(f'Next task_issue_number: {task_issue_number}.')


if __name__ == '__main__':
    main()

