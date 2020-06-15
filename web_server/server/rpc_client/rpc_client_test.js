var client = require('./rpc_client');

// invode add
client.add(1, 2, function(response) {
  console.assert(response == 3);
});

// invode getNewsSummariesForUser
client.getNewsSummariesForUser('test', 2, function(response) {
  console.assert(response != null);
});

// invokde "logNewsClickForUser" // use one news digest in your database
 client.logNewsClickForUser('test_user', '1b2f3b0bbd02233d90174cad804e1bd4');
// client.logNewsClickForUser('test_user', 'nmuYSK3LFDb7SY727Ibonw==\n');
