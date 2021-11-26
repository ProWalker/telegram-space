from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
from os import path

import requests
import datetime
import os
import telegram


def download_picture(url, image_name):
    response = requests.get(url)
    response.raise_for_status()
    Path(f'images').mkdir(parents=True, exist_ok=True)
    file_path = f'images/{image_name}'

    with open(file_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v4/launches/5eb87ce3ffd86e000604b336')
    response.raise_for_status()
    images_links = response.json()['links']['flickr']['original']
    for image_number, url in enumerate(images_links, start=1):
        download_picture(url, f'spacex{image_number}.jpg')


def get_image_extension_from_url(url):
    url_parts = urlparse(url)
    file_name = path.split(url_parts.path)[1]
    file_extension = path.splitext(file_name)[1]
    return file_extension


def fetch_nasa_apod(token, count=1):
    params = {
        'api_key': token,
        'count': count,
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params).json()
    for count, item in enumerate(response, start=1):
        try:
            image_extension = get_image_extension_from_url(item['hdurl'])
        except KeyError:
            continue
        download_picture(item['hdurl'], f'apod{count}{image_extension}')


def fetch_nasa_epic(token):
    params = {
        'api_key': token,
    }
    response = requests.get('https://api.nasa.gov/EPIC/api/natural/', params=params).json()
    for count, item in enumerate(response, start=1):
        image_date = datetime.datetime.fromisoformat(item['date'])
        source_url = f'https://epic.gsfc.nasa.gov/archive/natural/{image_date.year}/{image_date.month}/' \
                     f'{image_date.day}/png/{item["image"]}.png'
        download_picture(source_url, f'epic{count}.png')


if __name__ == '__main__':
    load_dotenv()
    # telegram_token = os.getenv('TELEGRAM_TOKEN')
    # bot = telegram.Bot(token=telegram_token)
    # bot.send_message(chat_id='@space_in_place', text='Hi! Message from bot!')
    nasa_token = os.getenv('NASA_TOKEN')
    fetch_spacex_last_launch()
    fetch_nasa_apod(nasa_token, 30)
    fetch_nasa_epic(nasa_token)

