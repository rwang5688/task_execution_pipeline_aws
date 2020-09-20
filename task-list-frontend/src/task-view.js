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
      $('#user-id').val($('#' + id + ' #user_id').text());
      $('#task-id').val(id);
      $('#task-tool').val($('#' + id + ' #task_tool').text());
      $('#task-extra-options').val($('#' + id + ' #task_extra_options').text());
      $('#task-source-code').val($('#' + id + ' #task_source_code').text());
      $('#task-source-fileinfo').val($('#' + id + ' #task_source_fileinfo').text());
      $('#task-preprocessed-files').val($('#' + id + ' #task_preprocessed_files').text());
      $('#task-status').val($('#' + id + ' #task_status').text());
      $('#submit-timestamp').val($('#' + id + ' #submit_timestamp').text());
      $('#update-timestamp').val($('#' + id + ' #update_timestamp').text());
    }
  }, 100);
}


function renderError (body) {
  $('#error').html(errTpl(body.err));
}

