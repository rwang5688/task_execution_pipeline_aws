import tarfile
from io import BytesIO
from io import StringIO
import json
import issuetable
import dotvfile
import csvfile
import s3util


def get_task_attribute_value(task, task_attribute_name):
    task_attribute_value = ''
    if task_attribute_name in task:
        task_attribute_value = task[task_attribute_name]
    else:
        print('get_task_attribute_value: Task attribute %s is not defined.' %  task_attribute_name)

    return task_attribute_value


def get_issue_table():
    return issuetable.get_issue_table()


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

    print('issue_record: %s' % issue_record)

    return True


def upload_tmp_file(bucket_name, task, tmp_file_name):
    # get bucket
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('upload_tmp_file: Bucket %s does not exist.' % bucket_name)
        return False

    # get user_id, task_id
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return False

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return False

    # upload file
    tmp_file_full_path = '/tmp/' + tmp_file_name
    object_name = user_id + "/" + task_id + "/" + tmp_file_name
    success = s3util.upload_file(tmp_file_full_path, bucket["Name"], object_name)
    if not success:
        print('upload_tmp_file: Failed to upload object %s.' % object_name)
        return False

    # success
    return True


def write_task_issues(issue_table, bucket_name, task, scan_result_tar_blob):
    # get user_id, task_id, task_issues_csv
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return False

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return False

    task_issues_csv = get_task_attribute_value(task, 'task_issues_csv')
    if task_issues_csv == '':
        return False

    # write csv file header
    csv_file_name = task_issues_csv
    csv_file_full_path = '/tmp/' + csv_file_name
    success = csvfile.write_task_issues_csv_header(csv_file_full_path)
    if not success:
        print('write_task_issues: write_task_issues_csv_header failed.  Exit.')
        return False

    # initialize task issue number
    task_issue_number = 1
    print('write_task_issues: Starting task_issue_number: %d.' % task_issue_number)

    # foreach dot v file, decode, and write task issues to issue table and csv file
    with tarfile.open(fileobj = BytesIO(scan_result_tar_blob)) as tar:
        for tar_resource in tar:
            if (tar_resource.isfile()):
                # extract dot v file blob from tar resource
                dot_v_file_bytes = tar.extractfile(tar_resource).read()
                if dot_v_file_bytes is None:
                    print('write_task_issues: Empty .v file.  Next.')
                    continue

                # load convert dot v file blob to a json object
                dot_v_file_json = json.loads(dot_v_file_bytes)
                if dot_v_file_json is None:
                    print('write_task_issues: Null JSON object.  Next.')
                    continue

                # decode dot v file issues
                task_issues = dotvfile.decode_dot_v_file_issues(task_id, task_issue_number, dot_v_file_json)
                if task_issues is None:
                    print('write_task_issues: decode_dot_v_file_issues failed.  Next.')
                    continue

                # write to issue table
                for task_issue in task_issues:
                    success = write_issue_record(issue_table, task_issue)
                    if not success:
                        print('write_task_issues: write_issue_record failed.  Next.')
                        continue

                # write to csv file
                success = csvfile.append_task_issues_csv_rows(csv_file_full_path, task_issues)
                if not success:
                    print('write_task_issues: append_task_issues_csv_rows failed.  Next.')
                    continue

                # success: update task issue number
                num_task_issues = len(task_issues)
                task_issue_number += num_task_issues
                print('write_task_issues: Wrote %d issues.' % num_task_issues)
                print('write_task_issues: Next task_issue_number: %d.' % task_issue_number)


    # upload /tmp/$(task_id)_issues.csv to result data bucket
    success = upload_tmp_file(bucket_name, task, csv_file_name)
    if not success:
        print('write_task_issues: upload_tmp_file failed: %s.' % csv_file_name)
        return False

    # success
    return True

