const uuid = require('uuid');
const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = { TableName: process.env.TASK_TABLE };

// create HTTP response
function respond (err, body, cb) {
  'use strict';
  let statusCode = 200;

  body = body || {};
  if (err) {
    body.stat = 'err';
    body.err = err;
    if (err.statusCode) {
      statusCode = err.statusCode;
    } else {
      statusCode = 500;
    }
  } else {
    body.stat = 'ok';
  }

  const response = {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': true,
      statusCode: statusCode
    },
    body: JSON.stringify(body)
  };

  // debug
  console.log(response);

  cb(null, response);
}

// create
function create (event, context, cb) {
  'use strict';
  // debug
  console.log('event: ' + JSON.stringify(event));
  const data = JSON.parse(event.body);

  data.task_id = uuid.v1();
  data.submit_timestamp = new Date().getTime();
  data.update_timestamp = data.submit_timestamp;

  // debug
  console.log('create task_id: ' + data.task_id);
  const params = { ...TABLE_NAME, Item: data };
  dynamoDb.put(params, (err, data) => {
    respond(err, {data: data}, cb);
  });
}

// read
function read (event, context, cb) {
  'use strict';
  // debug
  console.log('event: ' + JSON.stringify(event));
  // debug
  console.log('read task_id: ' + event.pathParameters.id);
  const params = { ...TABLE_NAME, Key: { task_id: event.pathParameters.id } };
  dynamoDb.get(params, (err, data) => {
    respond(err, data, cb);
  });
}

// update
function update (event, context, cb) {
  'use strict';
  // debug
  console.log('event: ' + JSON.stringify(event));
  const data = JSON.parse(event.body);

  // debug
  console.log('update task_id: ' + event.pathParameters.id);
  data.task_id = event.pathParameters.id;
  data.update_timestamp = new Date().getTime();
  const params = { ...TABLE_NAME, Item: data };

  dynamoDb.put(params, (err, data) => {
    console.log(err);
    console.log(data);
    respond(err, data, cb);
  });
}

// delete
function del (event, context, cb) {
  'use strict';
  // debug
  console.log('event: ' + JSON.stringify(event));
  // debug
  console.log('del task_id: ' + event.pathParameters.id);
  const params = { ...TABLE_NAME, Key: { task_id: event.pathParameters.id } };
  dynamoDb.delete(params, (err, data) => {
    respond(err, data, cb);
  });
}

// list
function list (event, context, cb) {
  'use strict';
  const params = TABLE_NAME;
  dynamoDb.scan(params, (err, data) => {
    respond(err, data, cb);
  });
}

// entry points
module.exports = {
  create,
  read,
  update,
  del,
  list
};
