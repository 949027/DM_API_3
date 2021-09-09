import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


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
    url_tamplate = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
    url = url_tamplate.format(parse.netloc + parse.path)
    payload = {'units': -1}
    response = requests.get(url, headers={'Authorization': token}, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url):
    parse = urlparse(url)
    return parse.netloc == 'bit.ly'


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')
    url = input('Input URL or bitlink\n=> ')
    if is_bitlink(url):
        try:
            print(count_clicks(token, url))
        except requests.exceptions.HTTPError:
            print('Incorrect bitlinks')
    else:
        try:
            print('Bitlink:', shorten_link(token, url))
        except requests.exceptions.HTTPError:
            print('Incorrect URL')