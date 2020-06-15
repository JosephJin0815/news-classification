var jayson = require('jayson');

// create a client
var client = jayson.client.http({
  port: 4040,
  hostname: 'localhost'
});


// Test RPC method
function add(a, b, callback) {
  // 'add' should mach the name that exposed by server
  // [a, b] has order
  client.request('add', [a, b], function(err, error, response){
    // err is the error from jayson which we cannot handle so throw err
    // error is from RPC server
    // for example, a or b is invalid number to add
    if (err) throw err;
    console.log(response);
    callback(response);
  })
}

// get news summaries for a user from RPC server
function getNewsSummariesForUser(user_id, page_num, callback) {
  client.request('getNewsSummariesForUser', [user_id, page_num], function(err, response) {
    if (err) throw err;
    console.log(response);
    callback(response.result);
  });
}

function logNewsClickForUser(user_id, news_id) {
  client.request('logNewsClickForUser', [user_id, news_id], function(err, response) {
    if (err) throw err;
    // do not need to handle the response
    console.log(response);
  });
}

module.exports = {
  add: add,
  getNewsSummariesForUser : getNewsSummariesForUser,
  logNewsClickForUser : logNewsClickForUser
};
