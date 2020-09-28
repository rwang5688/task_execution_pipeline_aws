'use strict';

import $ from 'jquery';
import {view} from './task-view';
const task = {activate};
export {task};

/*jshint -W101 */
const API_ROOT = `https://tasklistapi.${process.env.TASK_LIST_DOMAIN}/api/task/`;
/*jshint +W101 */

let auth;


function gather () {
  return {
    user_id: $('#user-id').val(),
    task_id: $('#task-id').val(),
    task_tool: $('#task-tool').val(),
    task_extra_options: $('#task-extra-options').val(),
    task_source_code: $('#task-source-code').val(),
    task_source_fileinfo: $('#task-source-fileinfo').val(),
    task_preprocess_tar: $('#task-preprocess-tar').val(),
    task_status: $('#task-status').val(),
    submit_timestamp: $('#submit-timestamp').val(),
    update_timestamp: $('#update-timestamp').val()
  };
}


function create (cb) {
  auth.session().then(session => {
    $.ajax(API_ROOT, {
      data: JSON.stringify(gather()),
      contentType: 'application/json',
      type: 'POST',
      headers: {
        Authorization: session.idToken.jwtToken
      },
      success: function (body) {
        if (body.stat === 'ok') {
          list(cb);
        } else {
          $('#error').html(body.err);
          cb && cb();
        }
      }
    });
  }).catch(err => view.renderError(err));
}


function update (cb) {
  auth.session().then(session => {
    $.ajax(API_ROOT + $('#task-id').val(), {
      data: JSON.stringify(gather()),
      contentType: 'application/json',
      type: 'PUT',
      headers: {
        Authorization: session.idToken.jwtToken
      },
      success: function (body) {
        if (body.stat === 'ok') {
          list(cb);
        } else {
          $('#error').html(body.err);
          cb && cb();
        }
      }
    });
  }).catch(err => view.renderError(err));
}


function del (id) {
  auth.session().then(session => {
    $.ajax(API_ROOT + id, {
      type: 'DELETE',
      headers: {
        Authorization: session.idToken.jwtToken
      },
      success: function (body) {
        if (body.stat === 'ok') {
          list();
        } else {
          $('#error').html(body.err);
        }
      }
    });
  }).catch(err => view.renderError(err));
}


function list (cb) {
  auth.session().then(session => {
    $.ajax(API_ROOT, {
      type: 'GET',
      headers: {
        Authorization: session.idToken.jwtToken
      },
      success: function (body) {
        if (body.stat === 'ok') {
          view.renderList(body);
        } else {
          view.renderError(body);
        }
        cb && cb();
      },
      fail: function (jqXHR, textStatus, errorThrown) {
        alert(textStatus);
        alert(errorThrown);
      }
    });
  }).catch(err => view.renderError(err));
}


function bindList () {
  $('.task-item-edit').unbind('click');
  $('.task-item-edit').on('click', (e) => {
    view.renderEditArea(e.currentTarget.id);
  });
  $('.task-item-delete').unbind('click');
  $('.task-item-delete').on('click', (e) => {
    del(e.currentTarget.id);
  });
}


function bindEdit () {
  $('#input-task').unbind('click');
  $('#input-task').on('click', e => {
    e.preventDefault();
    view.renderEditArea();
  });
  $('#task-save').unbind('click');
  $('#task-save').on('click', e => {
    e.preventDefault();
    if ($('#task-id').val().length > 0) {
      update(() => {
        view.renderAddButton();
      });
    } else {
      create(() => {
        view.renderAddButton();
      });
    }
  });
  $('#task-cancel').unbind('click');
  $('#task-cancel').on('click', e => {
    e.preventDefault();
    view.renderAddButton();
  });
}


function activate (authObj) {
  auth = authObj;
  list(() => {
    bindList();
    bindEdit();
  });
  $('#content').bind('DOMSubtreeModified', () => {
    bindList();
    bindEdit();
  });
}

