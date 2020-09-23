import json
import dotvfile
import csvfile


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
    # initialize mock task id and task issue number
    task_id = 'xvsa-xfa-dummy'
    task_issue_number = 1
    print(f'writeDotVFileIssuesCSV: Starting task issue number is {task_issue_number}.')

    # write csv file header
    csv_file_name = task_id + '_issues.csv'
    success = csvfile.write_task_issues_csv_header(csv_file_name)
    if not success:
        print('writeDotVFileIssuesCSV: write_task_issues_csv_header failed.  Exit.')
        return

    # read mock dot v file json
    dot_v_file_json = read_dot_v_file_json(task_id)
    if dot_v_file_json is None:
        print('writeDotVFileIssuesCSV: read_dot_v_file_json failed.  Exit.')
        return

    # decode dot v file issues
    task_issues = dotvfile.decode_dot_v_file_issues(task_id, task_issue_number, dot_v_file_json)
    if task_issues is None:
        print('write_task_issues: decode_dot_v_file_issues failed.  Next.')
        return

    # write to csv file
    success = csvfile.append_task_issues_csv_rows(csv_file_name, task_issues)
    if not success:
        print('writeDotVFileIssuesCSV: append_task_issues_csv_rows failed.  Next.')
        return

    # success: update task issue number
    num_task_issues = len(task_issues)
    task_issue_number += num_task_issues
    print(f'writeDotVFileIssuesCSV: Wrote {num_task_issues} issues.')
    print(f'writeDotVFileIssuesCSV: Next task issue number is {task_issue_number}.')


if __name__ == '__main__':
    main()

