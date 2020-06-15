const mongoose = require('mongoose');
const bcrypt = require('bcrypt'); // used for salt

const UserSchema = new mongoose.Schema({
  email: {
    type: String,
    index: { unique: true } // avoid some user name
  }, password: String,
});

UserSchema.methods.comparePassword = function comparePassword(password, callback) {
  // password: passed by client
  // this.password: hashed password after adding salt
  bcrypt.compare(password, this.password, callback);
};

UserSchema.pre('save', function saveHook(next) {
  const user = this;

  // proceed further only if the password is modified or the user is new
  if (!user.isModified('password')) return next();

  return bcrypt.genSalt((saltError, salt) => {
    if (saltError) { return next(saltError); }

    return bcrypt.hash(user.password, salt, (hashError, hash) => {
      if (hashError) { return next(hashError); } // replace the plain password with the hashed password adding salt
      user.password = hash;

      return next();
    });
  });
});

module.exports = mongoose.model('User', UserSchema);
