import './NewsCard.css'

import Auth from '../Auth/Auth';
import React from 'react';

class NewsCard extends React.Component {
  redirectToUrl(url, e) {
    e.preventDefault();
    this.sendClickLog();
    window.open(url, '_blank');
  }

  sendClickLog() {
    // news.digest is unique
    const url = "http://" + window.location.hostname + ":3000"
        + "/news/userId=" + Auth.getEmail() + "&newsId=" + this.props.news.digest;

    const request = new Request(
      // must have "Authorization" header
      // since only registed user can send log to back end
      encodeURI(url),
      {
        method: "POST",
        headers: {
          "Authorization": "bearer " + Auth.getToken()
        },
      }
    );
    // do not have response for this request
    fetch(request);
  }

  // news is passed as property from NewsPanel
  // NewsCard only does the rendering.
   render() {
     return(
        <div className="news-container" onClick={
          (e) => this.redirectToUrl(this.props.news.url, e)}>
        <div className='row'>
          <div className='col s4 fill'>
            <img src={this.props.news.urlToImage} alt='news' />
          </div>
          <div className='col s8'>
            <div className='news-intro-col'>
              <div className='news-intro-panel'>
                <h4>{this.props.news.title}</h4>
                <div className='news-description'>
                  <p>{this.props.news.description}</p>
                    <div>
                    {this.props.news.source != null && <div className='chip light-blue news-chip'>{this.props.news.source}</div>}
                    {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                    {this.props.news.time != null && <div className='chip amber news-chip'>{this.props.news.time}</div>}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
   }
}

export default NewsCard;
