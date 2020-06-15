import LoginForm from './LoginForm';
import React from 'react';
// LoginPage.js
import Auth from '../Auth/Auth';
import PropTypes from 'prop-types';
//var PropTypes = require('prop-types'); // ES5 with npm
class LoginPage extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      errors: {},
      user: {
        email: '',
        password: ''
      }
    }
  }

  // set the initial Component state.
  processForm(event) {
    event.preventDefault();
    const email = this.state.user.email;
    const password = this.state.user.password;

    console.log('email:', email);
    console.log('password', password);

    // Post login data
    const url = 'http://'+ window.location.hostname + ':3000' + '/auth/login';
    const request = new Request (
      url,
      {
        method:'POST', headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: this.state.user.email,
          password: this.state.user.password
        })
    });

    fetch(request).then(response => {
      if (response.status === 200) {
        // may have error, after login clear the error
        this.setState({ errors: {} });
        response.json().then(json => {
          console.log(json);
          // "token" should match with server
          console.log("=======token should match with server=========");
          Auth.authenticateUser(json.token, email);
          console.log("=============redireact to root, since client already login, App component will be shown=========.=");
          // redireact to root, since client already login, App component will be shown.
          this.context.router.replace('/');
        });
      } else {
        console.log("Login failed");
        response.json().then(json => {
          const errors = json.errors ? json.errors : {};
          errors.summary = json.message;
          this.setState({errors});
        });
      }
    });
  }

  changeUser(event) {
      const field = event.target.name; // email || Password
      const user = this.state.user;
      user[field] = event.target.value;

      this.setState({user});
  }

  render() {
    return (
      <LoginForm
      onSubmit={(e) => this.processForm(e)}
      onChange={(e) => this.changeUser(e)}
      errors={this.state.errors}
      />
    );
  }
}

LoginPage.contextTypes = {
  router: PropTypes.object.isRequired
};

export default LoginPage;
