# cnn_news_scraper_test.py

import cnn_news_scraper as scraper

EXPECTED_NEWS = "She went down in the trenches and was killed by the enemy on the front line"
CNN_NEWS_URL = "https://edition.cnn.com/2020/04/28/us/er-doctor-coronavirus-help-death-by-suicide-trnd/index.html"
def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)


    print(news)
    assert EXPECTED_NEWS in news
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
