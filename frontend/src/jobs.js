'use strict';

import $ from 'jquery';
import {view} from './jobs-view';
const todo = {activate};
export {todo};

/*jshint -W101 */
const API_ROOT = `https://jobslistapi.${process.env.JOBS_LIST_DOMAIN}/api/jobs/`;
/*jshint +W101 */

let auth;


function gather () {
  return {
    job_id: $('#job_id').val(),
    job_tool: $('#job_tool').val(),
    job_source: $('#job_source').val(),
    job_status: $('#job_status').val(),
    job_logfile: $('#job_logfile').val(),
    submitter_id: $('#submitter_id').val(),
    submit_timestamp: $('submit_timestamp').val(),
    update_timestamp: $('update_timestamp').val()
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
    $.ajax(API_ROOT + $('#job_id').val(), {
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
  $('.job-item-edit').unbind('click');
  $('.job-item-edit').on('click', (e) => {
    view.renderEditArea(e.currentTarget.id);
  });
  $('.job-item-delete').unbind('click');
  $('.job-item-delete').on('click', (e) => {
    del(e.currentTarget.id);
  });
}


function bindEdit () {
  $('#input-job').unbind('click');
  $('#input-job').on('click', e => {
    e.preventDefault();
    view.renderEditArea();
  });
  $('#job-save').unbind('click');
  $('#job-save').on('click', e => {
    e.preventDefault();
    if ($('#job_id').val().length > 0) {
      update(() => {
        view.renderAddButton();
      });
    } else {
      create(() => {
        view.renderAddButton();
      });
    }
  });
  $('#todo-cancel').unbind('click');
  $('#todo-cancel').on('click', e => {
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

