import requests
from django.conf import settings
from urllib.parse import urlparse




def shorten_link(url: str):
    token = settings.VK_API_TOKEN
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {'access_token': token, 'v': '5.199',
              'p1': 'v1',
              'url': url,
              'private': '0', }

    response = requests.post(url=api_url, params=params)
    response.raise_for_status()
    short_url = response.json()['response']['short_url']
    return short_url


def count_clicks(short_url: str):
    token = settings.VK_API_TOKEN
    short_url_key = is_shorten_link(short_url)
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {'access_token': token, 'v': '5.199',
              'p1': 'v1',
              'key': short_url_key,
              'interval': 'forever',
              'extended': '0', }
    response = requests.post(url=api_url, params=params)
    response.raise_for_status()
    if response.json().get('response') and len(response.json()['response']['stats']) > 0:
        click_count = response.json()['response']['stats'][0]['views']
    else:
        click_count = 0
    return click_count


def is_shorten_link(url):
    parser_url = urlparse(url)
    if parser_url.netloc == 'vk.cc' and parser_url.path != '':
        short_url_key = parser_url.path.lstrip('/')
        return short_url_key
    return False

