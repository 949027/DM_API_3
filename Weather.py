import requests


def get_weather(city):
    payload = {
        'nTqm': '',
        'lang': 'ru',
    }
    url_template = 'https://wttr.in/{}'
    url = url_template.format(city)
    response = requests.get(url, params=payload)
    response.raise_for_status()
    print(response.text)


get_weather('Лондон')
get_weather('Шереметьево')
get_weather('Череповец')
