import os
from typing import List

server_url = os.environ.get('SERVER_URL')
api_key = os.environ.get('API_KEY')

TELEGRAM_BASE_URL = 'https://api.telegram.org/bot'
WEBHOOK_BASE_URL = server_url + '/webhook'


def build_geocoding_api_url(lat_long: List[float]) -> str:

    lat = lat_long[0]
    long = lat_long[1]

    url = (
        f'https://maps.googleapis.com/maps/api/geocode/json?'
        f'latlng={lat},{long}&language=pt-BR&key={api_key}'
    )

    return url
