import requests
import datetime


def fetch_nasa_apod(token, count=1):
    params = {
        'api_key': token,
        'count': count,
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params).json()
    images_links = []
    for item in response:
        try:
            images_links.append(item['hdurl'])
        except KeyError:
            continue

    return images_links


def fetch_nasa_epic(token):
    params = {
        'api_key': token,
    }
    response = requests.get('https://api.nasa.gov/EPIC/api/natural/', params=params).json()
    images_links = []
    for item in response:
        image_date = datetime.datetime.fromisoformat(item['date'])
        source_url = f'https://epic.gsfc.nasa.gov/archive/natural/{image_date.year}/{image_date.month}/' \
                     f'{image_date.day}/png/{item["image"]}.png'
        images_links.append(source_url)

    return images_links

