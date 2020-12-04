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
      $('#project-name').val($('#' + id + ' #project_name').text());
      $('#task-tool').val($('#' + id + ' #task_tool').text());
      $('#task-extra-options').val($('#' + id + ' #task_extra_options').text());
      $('#task-fileinfo-json-url').val($('#' + id + ' #task_fileinfo_json_url').text());
      $('#task-preprocess-tar-url').val($('#' + id + ' #task_preprocess_tar_url').text());
      $('#task-source-code-zip-url').val($('#' + id + ' #task_source_code_zip_url').text());
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

