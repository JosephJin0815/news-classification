# news_api_client.py

import news_api_client as client

def test_basic():
    # test pass with no argument
    news = client.getNewsFromSource()
    print(news)
    assert len(news) > 0
    # test pass with argument
    news = client.getNewsFromSource(sources=['cnn'], sortBy='top')
    assert len(news) > 0
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
