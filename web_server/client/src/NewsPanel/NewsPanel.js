import './NewsPanel.css'

import NewsCard from '../NewsCard/NewsCard';
import Auth from '../Auth/Auth';
import _ from 'lodash';
import React from 'react'

// NewsPanel should maintain a state that is a dynamic list of NewsCard.
// NewsPanel cannot be a function, it should be a class to maintain a state
class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = {news:null,  pageNum:1, loadedAll:false};
  }

  componentDidMount() {
    this.loadMoreNews();
    this.loadMoreNews = _.debounce(this.loadMoreNews, 1000)
    window.addEventListener('scroll', () => this.handleScroll());
  }

  handleScroll() {
    // the height that cannot show on the screen
    let scrollY = window.scrollY || window.pageYOffset ||
    document.documentElement.scrollTop
    if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50 )) {
      console.log("Handle Scoller");
       this.loadMoreNews();
     }
   }

  renderNews() {
    // news_list is a list of HTML
    const news_list = this.state.news.map((news) => {
      return(
        <a className='list-group-item' key={news.digest} href="#">
          <NewsCard news={news} />
        </a>
      );
    });

    return (
      <div className='container-fluid'>
        <div className='list-group'>
          {news_list}
        </div>
      </div>
    );
  }

  loadMoreNews() {
    if (this.loadedAll == true) {
      return;
    }

    console.log("Load more news!!!");
    const news_url = 'http://' + window.location.hostname + ':3000' +'/news/userId=' + Auth.getEmail() + '&pageNum=' + this.state.pageNum;
    // encode url to escape special character of user email
    const request = new Request(
      encodeURI(news_url), {
      method: 'GET',
      headers: {
        'Authorization': 'bearer ' + Auth.getToken(),
      }
    });

    fetch(request)
      .then(res => res.json())
      .then(fetched_news_list => {
        if (!fetched_news_list || fetched_news_list.length == 0) {
          console.log("====newsPanel.js loadedAll====0000");
          this.setState({loadedAll: true});
        }
        console.log("====newsPanel.js print news====");
        this.setState({
          news: this.state.news ? this.state.news.concat(fetched_news_list) : fetched_news_list,
          pageNum: this.state.pageNum + 1,
        });
      });
  }

  render() {
    if (this.state.news) {
      return (
        <div>
          {this.renderNews()}
        </div>
      );
    } else {
      return (
        <div>
          Loading...
        </div>
      );
    }
  }
}

export default NewsPanel;
