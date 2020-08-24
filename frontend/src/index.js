'use strict';

import $ from 'jquery';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'webpack-jquery-ui/css';
import Amplify from 'aws-amplify';
import {auth} from './auth';
import {task} from './task';


const oauth = {
  domain: process.env.TASK_LIST_COGNITO_DOMAIN,
  scope: ['email'],
  /*jshint -W101 */
  redirectSignIn: `https://s3-${process.env.TARGET_REGION}.amazonaws.com/${process.env.TASK_LIST_APPS_BUCKET}/index.html`,
  redirectSignOut: `https://s3-${process.env.TARGET_REGION}.amazonaws.com/${process.env.TASK_LIST_APPS_BUCKET}/index.html`,
  /*jshint +W101 */
  responseType: 'token'
};

Amplify.configure({
  Auth: {
    region: process.env.TARGET_REGION,
    userPoolId: process.env.TASK_LIST_USER_POOL_ID,
    userPoolWebClientId: process.env.TASK_LIST_USER_POOL_CLIENT_ID,
    identityPoolId: process.env.TASK_LIST_ID_POOL_ID,
    mandatorySignIn: false,
    oauth: oauth
  }
});


$(function () {
  auth.activate().then((user) => {
    if (user) {
      task.activate(auth);
    }
  });
});

