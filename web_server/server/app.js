
var bodyParser = require('body-parser');
var cors = require('cors');
var config = require('./config/config.json');
var express = require('express');
var path = require('path');
var passport = require('passport');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();
// use bodyParser middleware before any handler of POST request
app.use(bodyParser.json());
// connect mongodb
require('./models/main.js').connect(config.mongoDbUrl);
// auth checker must be imported after import mongodb
var authCheckerMiddleware = require('./middleware/auth_checker');

app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
// server static files
app.use('/static',
  express.static(path.join(__dirname, "../client/build/static")));

// TODO:
app.use(cors());
//app.all('*', function(req, res, next) {
//  res.header("Access-Control-Allow-Origin", "*");
//  res.header("Access-Control-Allow-Headers", "X-Requested-With");
//  next();
//})

app.use('/', index);
console.log("=================go to auth=====================");
app.use('/auth', auth);
// authCheckerMiddleware must use before news
// otherwise, it sends the news firest then do the auth check, which does not make sence
console.log("=================go to authCheckerMiddleware=====================");
app.use('/news', authCheckerMiddleware);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;
