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
      $('#task-fileinfo-json').val($('#' + id + ' #task_fileinfo_json').text());
      $('#task-preprocess-tar').val($('#' + id + ' #task_preprocess_tar').text());
      $('#task-source-code-zip').val($('#' + id + ' #task_source_code_zip').text());
      $('#task-status').val($('#' + id + ' #task_status').text());
      $('#task-dot-scan-log-tar-url').val($('#' + id + ' #task_dot_scan_log_tar_url').text());
      $('#task-scan-result-tar-url').val($('#' + id + ' #task_scan_result_tar_url').text());
      $('#task-summary-pdf-url').val($('#' + id + ' #task_summary_pdf_url').text());
      $('#task-issues-csv-url').val($('#' + id + ' #task_issues_csv_url').text());
      $('#submit-timestamp').val($('#' + id + ' #submit_timestamp').text());
      $('#update-timestamp').val($('#' + id + ' #update_timestamp').text());
    }
  }, 100);
}


function renderError (body) {
  $('#error').html(errTpl(body.err));
}

