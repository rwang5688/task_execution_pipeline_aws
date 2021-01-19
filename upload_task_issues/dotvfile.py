import copy


TASK_ISSUE_TEMPLATE = {
    'task_id': '',
    'task_issue_number': '',
    'issue_key': 'k',
    'issue_certainty': 'c',
    'issue_complexity': 'ic',
    'file_path': 'fid',
    'start_line_no': 'sln',
    'start_column_no': 'scn',
    'function_name': 'fn',
    'variable_name': 'vn',
    'rule_set': 'rs',
    'rule_code': 'rc',
    'error_code': 'ec',
    'message': 'm',
    'paths': []
}

TASK_ISSUE_PATH_TEMPLATE = {
    'file_path': 'fid',
    'start_line_no': 'sln',
    'start_column_no': 'scn',
    'function_name': 'fn',
    'variable_name': 'vn',
    'message': 'm'
}


def load_dot_v_fid_dict(dot_v_file_json):
    # confirm dot v file "files" array exists
    if not 'files' in dot_v_file_json:
        print('load_dot_v_file_dict: Missing files array.')
        return None

    # flatten files json into a simple fid dictionary
    dot_v_fid_dict = {}
    files = dot_v_file_json['files']
    for f in files:
        fid = f['fid']
        file_path = f['path']
        dot_v_fid_dict[fid] = file_path

    return dot_v_fid_dict


def decode_dot_v_issue_paths(dot_v_fid_dict, dot_v_issue_paths):
    task_issue_paths = []
    for dot_v_issue_path in dot_v_issue_paths:
        # deep copy from template
        task_issue_path = copy.deepcopy(TASK_ISSUE_PATH_TEMPLATE)

        # map dot_v_issue_path keys and values
        for task_issue_path_key in task_issue_path.keys():
            if task_issue_path_key == 'file_path':
                if 'fid' in dot_v_issue_path.keys():
                    task_issue_path['file_path'] = dot_v_fid_dict.get(dot_v_issue_path['fid'], 'errors-occur-in-scan-result-file')
            else:
                # task_issue_path[task_issue_path_key] maps to dot_v_issue_path_key
                dot_v_issue_path_key = task_issue_path[task_issue_path_key]
                if dot_v_issue_path_key in dot_v_issue_path.keys():
                    task_issue_path[task_issue_path_key] = dot_v_issue_path[dot_v_issue_path_key]

        # append task_issue_path
        task_issue_paths.append(task_issue_path)

    return task_issue_paths


def decode_dot_v_issue(task_id, task_issue_number, dot_v_fid_dict, dot_v_issue):
    # deep copy from template
    task_issue = copy.deepcopy(TASK_ISSUE_TEMPLATE)

    # map dot_v_issue keys and values
    for task_issue_key in task_issue.keys():
        if task_issue_key == 'task_id':
            task_issue['task_id'] = task_id
        elif task_issue_key == 'task_issue_number':
            task_issue['task_issue_number'] = task_issue_number
        elif task_issue_key == 'file_path':
            if 'fid' in dot_v_issue.keys():
                task_issue['file_path'] = dot_v_fid_dict.get(dot_v_issue['fid'], 'errors-occur-in-scan-result-file')
        elif task_issue_key == 'paths':
            if 'paths' in dot_v_issue.keys():
                dot_v_issue_paths = dot_v_issue['paths']
                task_issue['paths'] = decode_dot_v_issue_paths(dot_v_fid_dict, dot_v_issue_paths)
        else:
            # task_issue[task_issue_key] maps to dot_v_issue_key
            dot_v_issue_key = task_issue[task_issue_key]
            if dot_v_issue_key in dot_v_issue.keys():
                task_issue[task_issue_key] = dot_v_issue[dot_v_issue_key]

    return task_issue


def decode_dot_v_file_issues(task_id, starting_task_issue_number, dot_v_file_json):
    # flatten dot v "files" array into a fid dictionary
    dot_v_fid_dict = load_dot_v_fid_dict(dot_v_file_json)
    if dot_v_fid_dict is None:
        print('write_dot_v_file_issues: load_dot_v_file_dict failed.')
        return None

    # debug: print dot v fid dictionary
    print('dot_v_fid_dict:')
    print(dot_v_fid_dict)

    # confirm dot v file "issues" array exists
    if not 'issues' in dot_v_file_json:
        print('write_dot_v_file_issues: Missing issues array.')
        return None

    # decode dot v issues and write to task issues list
    task_issues = []
    task_issue_number = starting_task_issue_number
    dot_v_issues = dot_v_file_json['issues']
    for dot_v_issue in dot_v_issues:
        task_issue = decode_dot_v_issue(task_id, task_issue_number, dot_v_fid_dict, dot_v_issue)
        task_issues.append(task_issue)
        task_issue_number += 1

    # return issues list
    return task_issues

