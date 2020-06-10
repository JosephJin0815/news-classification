import operations

def test_getOneNewsBasic():
    news = operations.getOneNews()
    print(news)
    #assert news is not None
    print('test_get_one_news_passed')

def test_getNewsSummariesForUser_pagination():
    # Test paginated data are different
    news_page_1 = operations.getNewsSummariesForUser('test', 1)
    news_page_2 = operations.getNewsSummariesForUser('test', 2)

    # Assert that there is no dupe news in two pages
    digests_page_1_set = set([news['digest'] for news in news_page_1])
    digests_page_2_set = set([news['digest'] for news in news_page_2])

    assert len(digests_page_1_set.intersection(digests_page_2_set)) == 0
    print("test_getNewsSummariesForUser_pagination passed!")

def test_getNewsSummariesForUser_basic():
    news = operations.getNewsSummariesForUser('test_user', 1)
    assert len(news) > 0
    print(news)
    print("success")

if __name__ == "__main__":
    test_getOneNewsBasic()
    test_getNewsSummariesForUser_pagination()
