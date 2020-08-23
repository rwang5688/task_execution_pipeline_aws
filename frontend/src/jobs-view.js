'use strict';

import $ from 'jquery';
import 'webpack-jquery-ui/datepicker';
import { jobsListTpl, addTpl, editTpl, errTpl } from './templates';

const view = { renderList, renderAddButton, renderEditArea, renderError };
export { view };


function renderList (body) {
  $('#content').html(jobsListTpl(body.Items));
}


function renderAddButton () {
  $('#edit-area').html(addTpl());
}


function renderEditArea (id) {
  $('#edit-area').html(editTpl());
  setTimeout(function () {
    if (id) {
      $('#job-id').val(id);
      $('#job-tool').val($('#' + id + ' #job_tool').text());
      $('#job-source').val($('#' + id + ' #job_source').text());
      $('#job-status').val($('#' + id + ' #job_status').text());
      $('#job-logfile').val($('#' + id + ' #job_logfile').text());
      $('#submitter-id').val($('#' + id + ' #submitter_id').text());
      $('#submit-timestamp').val($('#' + id + ' #submit_timestamp').text());
      $('#update-timestamp').val($('#' + id + ' #update_timestamp').text());
    }
  }, 100);
}


function renderError (body) {
  $('#error').html(errTpl(body.err));
}

