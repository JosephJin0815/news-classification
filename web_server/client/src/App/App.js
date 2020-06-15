import './App.css';

import NewsPanel from '../NewsPanel/NewsPanel';
//import NewsPanel from './NewsPanel';
import React from 'react';
import logo from './newspaper.svg';

class App extends React.Component {
  render() {
    return (
      <div>
        <img className='logo' src={logo} alt='logo' width="140" height="180" />
        <div className='container'>
          <NewsPanel />
        </div>
      </div>
    );
  }
}

export default App;
