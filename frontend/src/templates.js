'use strict';

export { jobsListTpl, editTpl, addTpl, errTpl, navBarTpl };

function jobItemTpl (item) {
  /*jshint -W101 */
  return `
    <div id="${item.job_id}" class="row list-group-item d-flex justify-content-between align-items-center">
      <div id="job_id" class="col-sm-2">${item.job_id}</div>
      <div id="job_tool" class="col-sm-2">${item.job_tool}</div>
      <div id="job_source" class="col-sm-2">${item.job_source}</div>
      <div id="job_status" class="col-sm-2">${item.job_status}</div>
      <div id="job_logfile" class="col-sm-2">${item.job_logfile}</div>
      <div id="submitter_id" class="col-sm-2">${item.submitter_id}</div>
      <div id="submit_timestamp" class="col-sm-2">${item.submit_timestamp}</div>
      <div id="update_timestamp" class="col-sm-2">${item.update_timestamp}</div>
      <div id="${item.job_id}" class="col-sm-1 badge badge-danger badge-pill job-item-delete">Delete</div>
      <div id="${item.job_id}" class="col-sm-1 badge badge-primary badge-pill job-item-edit">Edit</div>
    </div>`;
  /*jshint +W101 */
}


function jobsListTpl (items) {
  let output = '';
  items.forEach(item => {
    output += jobItemTpl(item);
  });


  /*jshint -W101 */
  return `
  <div id="jobs-list">
    <div class="row list-group-item d-flex justify-content-between align-items-center">
      <div class="col-sm-2">Job Id</div>
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
      <span id="input-job" class="badge badge-success badge-pill">new</span>
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
          <div class="col-sm-1"></div><div class="col-sm-1">Tool: </div><div class="col-sm-6"><input  class="w-100" type="text" id="job-tool"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Source: </div><div class="col-sm-6"><input class="w-100" type="text" id="job-source"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Status: </div><div class="col-sm-6"><input class="w-100" type="text" id="job-status"></div>
        </div>
        <div class="row">&nbsp;</div>
        <div class="row">
          <div class="col-sm-1"></div><div class="col-sm-1">Logfile: </div><div class="col-sm-6"><input class="w-100" type="text" id="job-logfile"></div>
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
          <div class="col-sm-1"><button id="job-save">save</button></div>
          <div class="col-sm-1"><button id="job-cancel">cancel</button></div>
          <input type="hidden" id="job-id">
        </div>
      </div>
    </div>`;
    /*jshint +W101 */
}


function addTpl () {
  /*jshint -W101 */
  return `<li class="list-group-item d-flex justify-content-between align-items-center">
    <span id="input-job" class="badge badge-success badge-pill">new</span>
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

