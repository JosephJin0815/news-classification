import os
import random
# get random user agents
import requests
from lxml import html

# if the website change the html, this xpath may not work
GET_CNN_NEWS_XPATH = "//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"

# use absolute path, we may move the file to other directory
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

# read user agent file
with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            # remove "
            #USER_AGENTS.append(ua.strip()[1:-1])
            USER_AGENTS.append(ua.strip())

random.shuffle(USER_AGENTS)

def _get_header():
    # get random user agent
    ua = random.choice(USER_AGENTS)
    # case sensitive
    headers = {
        "Connection" : "close",
        "User-Agent" : ua
        }
    return headers

def extract_news(news_url):
    # use session to imitate to be a human
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=_get_header())
    news = {}

    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
        # join into a string
    except Exception as e:
        return {}

    return news
