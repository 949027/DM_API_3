import os
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv


def shorten_link(token, url):
    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        json={'long_url': url},
        headers={'Authorization': token},
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, url):
    parse = urlparse(url)
    url_tamplate = 'https://api-ssl.bitly.com/v4/bitlinks/{}/{}/clicks/summary'
    url = url_tamplate.format(parse.netloc, parse.path)
    payload = {'units': -1}
    response = requests.get(url, headers={'Authorization': token}, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, url):
    url_tamplate = 'https://api-ssl.bitly.com/v4/bitlinks/{}/{}'
    parse = urlparse(url)
    url = url_tamplate.format(parse.netloc, parse.path)
    response = requests.get(url, headers={'Authorization': token})
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    url = input('Input URL or bitlink\n=> ')
    if is_bitlink(token, url):
        try:
            print(count_clicks(token, url))
        except requests.exceptions.HTTPError:
            print('Incorrect bitlink')
    else:
        try:
            print('Bitlink:', shorten_link(token, url))
        except requests.exceptions.HTTPError:
            print('Incorrect URL')