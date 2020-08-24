'use strict';

export { taskListTpl, editTpl, addTpl, errTpl, navBarTpl };

function taskItemTpl (item) {
  /*jshint -W101 */
  return `
    <div id="${item.task_id}" class="row list-group-item d-flex justify-content-between align-items-center">
      <div id="task_id" class="col-sm-2">${item.task_id}</div>
      <div id="task_tool" class="col-sm-2">${item.task_tool}</div>
      <div id="task_source" class="col-sm-2">${item.task_source}</div>
      <div id="task_status" class="col-sm-2">${item.task_status}</div>
      <div id="task_logfile" class="col-sm-2">${item.task_logfile}</div>
      <div id="submitter_id" class="col-sm-2">${item.submitter_id}</div>
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
      <div class="col-sm-2">Task Id</div>
      <div class="col-sm-2">Tool</div>
      <div class="col-sm-2">Source</div>
      <div class="col-sm-2">Status</div>
      <div class="col-sm-2">Logfile</div>
      <div class="col-sm-2">Submitter Id</div>
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
          <div class="col-sm-1"></div><div class="col-sm-1">Tool: </div><div class="col-sm-6"><input  class="w-100" type="text" id="task-tool"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Source: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-source"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Status: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-status"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Logfile: </div><div class="col-sm-6"><input class="w-100" type="text" id="task-logfile"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Submitter Id: </div><div class="col-sm-6"><input class="w-100" type="text" id="submitter-id"></div>
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

