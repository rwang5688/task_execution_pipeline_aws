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
      $('#job_id').val(id);
      $('#job_tool').val($('#' + id + ' #job_tool').text());
      $('#job_source').val($('#' + id + ' #job_source').text());
      $('#job_status').val($('#' + id + ' #job_status').text());
      $('#job_logfile').val($('#' + id + ' #job_logfile').text());
      $('#submitter_id').val($('#' + id + ' #submitter_id').text());
      $('#submit_timestamp').val($('#' + id + ' #submit_timestamp').text());
      $('#update_timestamp').val($('#' + id + ' #update_timestamp').text());
    }
  }, 100);
}


function renderError (body) {
  $('#error').html(errTpl(body.err));
}

