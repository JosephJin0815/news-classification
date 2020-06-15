import '../NewsPanel/NewsPanel.css'
import NewsCard from '../NewsCard/NewsCard';

import React from 'react'
import _ from 'lodash';

class NewsPanel extends React.Component {
  constructor() {
    super();
    this.state = {news:null };
  }

  renderNews() {
    // news_list is a list of HTML
    const news_card_list = this.state.news.map(one_news => {
      return(
        <a className='list-group-item' key={one_news.digest} href="#">
          <NewsCard news={one_news} />
          </a>
        );
      });

    return (
      <div className='container-fluid'>
        <div className='list-group'>
          {news_card_list}
        </div>
      </div>
    )
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
  // For now, we hard code news list. Once we finish the back-end,
  // we will load news from back-end;
  loadMoreNews() {
    console.log("Load more new!");
      // copy news into the news list
      const mock_news =   [{
        "source": "The Wall Street Journal0",
        "title": "Berkshire Hathway Benefits From US Tax Plan",
        "description": "Warren Buffett has one man to thank for Berkshire Hathaway Inc.’s $29 billion windfall in 2017: President Donald Trump.",
        "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
        "urlToImage": "https://wangsongpublicimages.s3-us-west-1.amazonaws.com/john-o-nolan-228109-unsplash.jpg",
        "publishshedAt": "2018-02-23T23:26:30Z",
        "digest": "xxx\n",
        "reason": "Recommend"
      },
      {
        "source": "The Wall Street Journal1",
        "title": "Berkshire Hathway Benefits From US Tax Plan1",
        "description": "Omaha conglomerate posted $29 billion gain in 2017 and cash pile, mostly invested in Treasury bills, grew to $116 billion at year-end",
        "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
        "urlToImage": "https://wangsongtest.s3-us-west-1.amazonaws.com/791c72e3f7ef4a0ca415e16ab5d3a394.jpeg",
        "publishshedAt": "2018-02-23T23:26:30Z",
        "digest": "xxx\n",
        "reason": "Recommend"
      },
      {
        "source": "The Wall Street Journal2",
        "title": "Berkshire Hathway Benefits From US Tax Plan",
        "description": "Warren Buffett has one man to thank for Berkshire Hathaway Inc.’s $29 billion windfall in 2017: President Donald Trump.",
        "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
        "urlToImage": "https://wangsongpublicimages.s3-us-west-1.amazonaws.com/john-o-nolan-228109-unsplash.jpg",
        "publishshedAt": "2018-02-23T23:26:30Z",
        "digest": "xxx\n",
        "reason": "Recommend"
      },
      {
        "source": "The Wall Street Journal3",
        "title": "Berkshire Hathway Benefits From US Tax Plan",
        "description": "Warren Buffett has one man to thank for Berkshire Hathaway Inc.’s $29 billion windfall in 2017: President Donald Trump.",
        "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
        "urlToImage": "https://wangsongpublicimages.s3-us-west-1.amazonaws.com/john-o-nolan-228109-unsplash.jpg",
        "publishshedAt": "2018-02-23T23:26:30Z",
        "digest": "xxx\n",
        "reason": "Recommend"
      },
      {
        "source": "The Wall Street Journal4",
        "title": "Berkshire Hathway Benefits From US Tax Plan",
        "description": "Warren Buffett has one man to thank for Berkshire Hathaway Inc.’s $29 billion windfall in 2017: President Donald Trump.",
        "url": "https://www.wsj.com/articles/berkshire-hathaway-posted-29-billion-gain-in-2017-from-u-s-tax-plan-1519480047",
        "urlToImage": "https://wangsongpublicimages.s3-us-west-1.amazonaws.com/john-o-nolan-228109-unsplash.jpg",
        "publishshedAt": "2018-02-23T23:26:30Z",
        "digest": "xxx\n",
        "reason": "Recommend"
      }];
      // it will update UI to show more news
      this.setState({news: mock_news})
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
          <div id='msg-app-loading'>
            Loading...
          </div>
        )
      }
    }
}

export default NewsPanel;
