'use strict';

export { taskListTpl, editTpl, addTpl, errTpl, navBarTpl };

function taskItemTpl (item) {
  /*jshint -W101 */
  return `
    <div id="${item.task_id}" class="row list-group-item d-flex justify-content-between align-items-center">
      <div id="user_id" class="col-sm-2">${item.user_id}</div>
      <div id="task_id" class="col-sm-2">${item.task_id}</div>
      <div id="project_name" class="col-sm-2">${item.project_name}</div>
      <div id="task_tool" class="col-sm-2">${item.task_tool}</div>
      <div id="task_extra_options" class="col-sm-2">${item.task_extra_options}</div>
      <div id="task_fileinfo_json_url" class="col-sm-2"><a href=${item.task_fileinfo_json_url}>${item.task_fileinfo_json_url}</a></div>
      <div id="task_preprocess_tar_url" class="col-sm-2"><a href=${item.task_preprocess_tar_url}>${item.task_preprocess_tar_url}</a></div>
      <div id="task_source_code_zip_url" class="col-sm-2"><a href=${item.task_source_code_zip_url}>${item.task_source_code_zip_url}</a></div>
      <div id="task_status" class="col-sm-2">${item.task_status}</div>
      <div id="task_dot_scan_log_tar_url" class="col-sm-2"><a href=${item.task_dot_scan_log_tar_url}>${item.task_dot_scan_log_tar_url}</a></div>
      <div id="task_scan_result_tar_url" class="col-sm-2"><a href=${item.task_scan_result_tar_url}>${item.task_scan_result_tar_url}</a></div>
      <div id="task_summary_pdf_url" class="col-sm-2"><a href=${item.task_summary_pdf_url}>${item.task_summary_pdf_url}</a></div>
      <div id="task_issues_csv_url" class="col-sm-2"><a href=${item.task_issues_csv_url}>${item.task_issues_csv_url}</a></div>
      <div id="submit_timestamp" class="col-sm-2">${item.submit_timestamp}</div>
      <div id="update_timestamp" class="col-sm-2">${item.update_timestamp}</div>
      <div id="${item.task_id}" class="col-sm-1 badge badge-danger badge-pill task-item-delete">Delete</div>
      <div id="${item.task_id}" class="col-sm-1 badge badge-primary badge-pill task-item-edit">Edit</div>
    </div>`;
  /*jshint +W101 */
}


function taskListTpl (items) {
  let output = '';
  items.forEach(item => {
    output += taskItemTpl(item);
  });


  /*jshint -W101 */
  return `
  <div id="task-list">
    <div class="row list-group-item d-flex justify-content-between align-items-center">
      <div class="col-sm-2">User Id</div>
      <div class="col-sm-2">Task Id</div>
      <div class="col-sm-2">Project Name</div>
      <div class="col-sm-2">Tool</div>
      <div class="col-sm-2">Extra Options</div>
      <div class="col-sm-2">File Info Json URL</div>
      <div class="col-sm-2">Preprocess Tar URL</div>
      <div class="col-sm-2">Source Code Zip URL</div>
      <div class="col-sm-2">Status</div>
      <div class="col-sm-2">Dot Scan Log Tar URL</div>
      <div class="col-sm-2">Scan Result Tar URL</div>
      <div class="col-sm-2">Summary PDF URL</div>
      <div class="col-sm-2">Issues CSV URL</div>
      <div class="col-sm-2">Submit Timestamp</div>
      <div class="col-sm-2">Update Timestamp</div>
      <div class="col-sm-1"></div>
      <div class="col-sm-1"></div>
    </div>
    ${output}
  </div>
  <div id="edit-area" class="list-group">
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span id="input-task" class="badge badge-success badge-pill">new</span>
    </li>
  </div>`;
  /*jshint +W101 */
}


function editTpl () {
  /*jshint -W101 */
  return `
    <div class="row">&nbsp;</div>
    <div class="row">
      <div class="col-sm-6">
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">User Id: </div><div class="col-sm-6"><input class="w-100" type="text" id="user-id"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Project Name: </div><div class="col-sm-6"><input  class="w-100" type="text" id="project-name"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Tool: </div><div class="col-sm-6"><input  class="w-100" type="text" id="task-tool"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Extra Options: </div><div class="col-sm-6"><input  class="w-100" type="text" id="task-extra-options"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">File Info Json URL: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-fileinfo-json-url"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Preprocess Tar URL: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-preprocess-tar-url"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Source Code Zip URL: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-source-code-zip-url"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Status: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-status"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Dot Scan Log Tar URL: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-dot-scan-log-tar-url"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Scan Result Tar URL: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-scan-result-tar-url"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Summary PDF URL: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-summary-pdf-url"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Issues CSV URL: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-issues-csv-url"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Submit Timestamp: </div><div class="col-sm-6"><input class="w-100" type="text" id="submit-timestamp"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Update Timestamp: </div><div class="col-sm-6"><input class="w-100" type="text" id="update-timestamp"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div>
          <div class="col-sm-1"><button id="task-save">save</button></div>
          <div class="col-sm-1"><button id="task-cancel">cancel</button></div>
          <input type="hidden" id="task-id">
        </div>
      </div>
    </div>`;
    /*jshint +W101 */
}


function addTpl () {
  /*jshint -W101 */
  return `<li class="list-group-item d-flex justify-content-between align-items-center">
    <span id="input-task" class="badge badge-success badge-pill">new</span>
  </li>`;
  /*jshint +W101 */
}


function errTpl (err) {
  return `<div class="error">${JSON.stringify(err)}</div>`;
}


function navBarTpl (isAuth) {
  let link;

  if (isAuth) {
    link = '<a class="nav-link" href="#" id="logout">Logout</a>';
  } else {
    link = '<a class="nav-link" href="#" id="login">Login</a>';
  }

  return `
  <ul class="navbar-nav" id='navbar-list'>
    <li class="nav-item">
      ${link}
    </li>
  </ul>`;
}

