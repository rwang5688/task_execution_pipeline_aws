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


function renderEditArea (job_id) {
  $('#edit-area').html(editTpl());
  setTimeout(function () {
    if (job_id) {
      $('#job_id').val(job_id);
      $('#job_tool').val($('#' + job_id + ' #job_tool').text());
      $('#job_source').val($('#' + job_id + ' #job_source').text());
      $('#job_status').val($('#' + job_id + ' #job_status').text());
      $('#job_logfile').val($('#' + job_id + ' #job_logfile').text());
      $('#submitter_id').val($('#' + job_id + ' #submitter_id').text());
      $('#submit_timestamp').val($('#' + job_id + ' #submit_timestamp').text());
      $('#update_timestamp').val($('#' + job_id + ' #update_timestamp').text());
    }
  }, 100);
}


function renderError (body) {
  $('#error').html(errTpl(body.err));
}

