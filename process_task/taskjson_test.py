import copy
import taskjson


TASK={
 "task_summary_pdf": "task_summary.pdf",
 "task_source_code_zip": "source_code.zip",
 "task_dot_scan_log_tar": ".scan_log.tar.gz",
 "task_scan_result_tar": "scan_result.tar.gz",
 "task_issues_csv": "task_issues.csv",
 "task_extra_options": {
  "SCAN_EXTRA_VARIABLE_OPTION": "",
  "SCAN_EXTRA_JFE_OPTIONS": "",
  "SCAN_EXTRA_SKIP_VTABLE_OPTION": "YES",
  "SCAN_EXTRA_OPTIONS": ""
 },
 "task_id": "uuid",
 "task_tool": "xvsa_start.sh",
 "user_id": "user_id_info",
 "task_preprocess_tar": "preprocess.tar.gz",
 "task_fileinfo_json": "fileinfo.json",
 "task_status": "started"
}


def main():
    print('\nStarting testconf_test.py ...')

    print("TASK:")
    print(TASK)

    task = TASK
    task["task_status"] = "completed"

    print("task:")
    print(task)

    success = taskjson.write_task_json(task)
    if not success:
        print("write_task_json failed.  Exit.")
        return

    task_tool = task["task_tool"]
    task_status = task["task_status"]
    print("write_task_json completed for task_tool=%s with task_status=%s." % (task_tool, task_status))

    r_task = taskjson.read_task_json()
    if r_task is None:
        print("read_task_json failed.  Exit.")
        return

    print("read_task_json completed.")

    print("r_task:")
    print(r_task)


if __name__ == '__main__':
    main()

