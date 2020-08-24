'use strict';

import $ from 'jquery';
import 'webpack-jquery-ui/datepicker';
import { taskListTpl, addTpl, editTpl, errTpl } from './templates';

const view = { renderList, renderAddButton, renderEditArea, renderError };
export { view };


function renderList (body) {
  $('#content').html(taskListTpl(body.Items));
}


function renderAddButton () {
  $('#edit-area').html(addTpl());
}


function renderEditArea (id) {
  $('#edit-area').html(editTpl());
  setTimeout(function () {
    if (id) {
      $('#task-id').val(id);
      $('#task-tool').val($('#' + id + ' #task_tool').text());
      $('#task-source').val($('#' + id + ' #task_source').text());
      $('#task-status').val($('#' + id + ' #task_status').text());
      $('#task-logfile').val($('#' + id + ' #task_logfile').text());
      $('#submitter-id').val($('#' + id + ' #submitter_id').text());
      $('#submit-timestamp').val($('#' + id + ' #submit_timestamp').text());
      $('#update-timestamp').val($('#' + id + ' #update_timestamp').text());
    }
  }, 100);
}


function renderError (body) {
  $('#error').html(errTpl(body.err));
}

