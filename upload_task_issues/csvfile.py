import csv


TASK_ISSUE_FIELD_NAMES = [
    'task_id',
    'task_issue_number',
    'issue_key',
    'issue_certainty',
    'issue_complexity',
    'file_path',
    'start_line_no',
    'start_column_no',
    'function_name',
    'variable_name',
    'rule_set',
    'rule_code',
    'error_code',
    'message',
    'paths'
]


def write_task_issues_csv_header(csv_file_name):
    with open(csv_file_name, mode='w') as csv_file:
        if csv_file is None:
            print('write_task_issues_csv_header: Failed to open csv file.')
            return False

        writer = csv.DictWriter(csv_file, fieldnames=TASK_ISSUE_FIELD_NAMES)
        writer.writeheader()

    # success
    return True


def append_task_issues_csv_rows(csv_file_name, task_issues):
    with open(csv_file_name, mode='a') as csv_file:
        if csv_file is None:
            print('write_task_issues_csv_rows: Failed to open csv file.')
            return False

        writer = csv.DictWriter(csv_file, fieldnames=TASK_ISSUE_FIELD_NAMES)
        writer.writerows(task_issues)

    # success
    return True

