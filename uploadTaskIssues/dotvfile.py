import copy
import issuetable


def load_dot_v_fid_dict(dot_v_file_json):
    if not 'files' in dot_v_file_json:
        print('load_dot_v_file_dict: Missing files array')
        return None

    # flatten files json into a simple fid dictionary
    dot_v_fid_dict = {}
    files = dot_v_file_json['files']
    for f in files:
        fid = f['fid']
        file_path = f['path']
        dot_v_fid_dict[fid] = file_path

    return dot_v_fid_dict


def translate_dot_v_issue(task_id, task_issue_number, dot_v_fid_dict, dot_v_issue):
    # do something more sophisticated
    issue = copy.deepcopy(dot_v_issue)
    issue['task_id'] = task_id
    issue['task_issue_number'] = task_issue_number

    return issue


def write_issue_record(issue_table, issue):
    # create issue record
    issue_record = issuetable.create_issue_record(issue_table, issue)
    if issue_record is None:
        print('write_issue_record: create_issue_record failed.')
        return False

    # debug: get and print issue record
    task_id = issue_record['task_id']
    task_issue_number = issue_record['task_issue_number']
    issue_record = issuetable.get_issue_record(issue_table, task_id, task_issue_number)
    if issue_record is None:
        print('write_issue_record: get_issue_record failed.')
        return False

    print('Issue record:')
    print(issue_record)

    return True


def write_dot_v_file_issues(issue_table, task_id, task_issue_number, dot_v_file_json):
    # convert dot v files array to a fid dictionary
    dot_v_fid_dict = load_dot_v_fid_dict(dot_v_file_json)
    if dot_v_fid_dict is None:
        print('write_dot_v_file_issues: load_dot_v_file_dict failed.')
        return task_issue_number

    # debug: print dot v fid dictionary
    print('dot_v_fid_dict:')
    print(dot_v_fid_dict)

    # confirm dot v issues array exists
    if not 'issues' in dot_v_file_json:
        print('write_dot_v_file_issues: Missing issues array')
        return task_issue_number

    # get and write dot v issues
    dot_v_issues = dot_v_file_json['issues']
    for dot_v_issue in dot_v_issues:
        issue = translate_dot_v_issue(task_id, task_issue_number, dot_v_fid_dict, dot_v_issue)
        success = write_issue_record(issue_table, issue)
        if not success:
            print('write_dot_v_file_issues: write_issue_record failed.')
            continue
        task_issue_number += 1

    # return next task issue number
    return task_issue_number

