from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse
from fetch_spacex import fetch_spacex_last_launch
from fetch_nasa import fetch_nasa_apod, fetch_nasa_epic

import time
import os
import telegram
import requests


def get_image_extension_from_url(url):
    url_parts = urlparse(url)
    file_name = os.path.split(url_parts.path)[1]
    file_extension = os.path.splitext(file_name)[1]
    return file_extension


def download_picture(url, image_name):
    response = requests.get(url)
    response.raise_for_status()
    Path(f'images').mkdir(parents=True, exist_ok=True)
    image_extension = get_image_extension_from_url(url)
    file_path = f'images/{image_name}{image_extension}'

    with open(file_path, 'wb') as file:
        file.write(response.content)


def bulk_download_picture(urls, image_name):
    for count, url in enumerate(urls):
        download_picture(url, f'{image_name}{count}')


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    nasa_token = os.getenv('NASA_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    script_delay = int(os.getenv('SCRIPT_DELAY'))
    bot = telegram.Bot(token=telegram_token)
    while True:
        spacex_images_links = fetch_spacex_last_launch()
        nasa_apod_images_links = fetch_nasa_apod(nasa_token, 30)
        nasa_epic_images_links = fetch_nasa_epic(nasa_token)
        bulk_download_picture(spacex_images_links, 'spacex')
        bulk_download_picture(nasa_apod_images_links, 'apod')
        bulk_download_picture(nasa_epic_images_links, 'epic')
        images = os.listdir('images')
        for image in images:
            while True:
                try:
                    bot.send_document(chat_id=tg_chat_id, document=open(f'images/{image}', 'rb'))
                    break
                except telegram.error.RetryAfter as tgErrorRetryAfter:
                    time.sleep(tgErrorRetryAfter.retry_after)
        time.sleep(script_delay)

