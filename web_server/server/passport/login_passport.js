// login_passport.js
const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
// we need jwtSecret as a seed of password
const config = require('../config/config.json');
module.exports = new PassportLocalStrategy({
  // email and password should match the login form sent from client
  usernameField: 'email',
  passwordField: 'password',
  session: false,
  // default value
  passReqToCallback: true // default value
  // done: callback
  }, (req, email, password, done) => {
    const userData = {
      email: email.trim(),
      password: password
    };
    // find a user by email address
    return User.findOne({ email: userData.email }, (err, user) => {
      console.log("===================login_passport==================findOne() email" + email);
      if (err) { return done(err);
      }

      if (!user) {
        // when user not found, set error message
        const error = new Error('Incorrect email or password');
        error.name = 'IncorrectCredentialsError';

        return done(error);
      }

      // check if a hashed user's password is equal to a value saved in the database
      return user.comparePassword(userData.password, (passwordErr, isMatch) => {
        if (err) { return done(err); }

        if (!isMatch) {
          // when password not match, set error message
          const error = new Error('Incorrect email or password');
          error.name = 'IncorrectCredentialsError';

          return done(error);
        }

        const payload = {
          sub: user._id // mongodb internal id
        };
        // create a token string
        const token = jwt.sign(payload, config.jwtSecret);
        const data = {
          name: user.email
        };
        return done(null, token, null);
      });
    });
});
