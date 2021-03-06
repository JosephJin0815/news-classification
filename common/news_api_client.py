
import requests

from json import loads

NEWS_API_ENDPOINT = "https://newsapi.org/v1/"
NEWS_API_KEY = "65d421d86f664806af7d326cd9d6b9da"
ARTICLES_API = "articles"

# define constant
CNN = 'cnn'
DEFAULT_SOURCE =[CNN]
SORT_BY_TOP = 'top'

def buildUrl(endPoint=NEWS_API_ENDPOINT, apiName=ARTICLES_API):
    return endPoint + apiName

def getNewsFromSource(sources=DEFAULT_SOURCE, sortBy=SORT_BY_TOP):
    articles = []
    # get news from each getNewsFromSource
    for source in sources:
        payload = {
            'apiKey':NEWS_API_KEY,
            'source':source,
            'sortBy':sortBy
        }
        response = requests.get(buildUrl(), params=payload)
        # response.content is a binary
        res_json = loads(response.content.decode('utf-8'))

        # Extract info from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):

            # populate news source in each articles
            for news in res_json['articles']:
                news['source'] = res_json['source']
            # join two list into one list
            articles.extend(res_json['articles'])
    return articles
