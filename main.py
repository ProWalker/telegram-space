from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlparse
from fetch_spacex import fetch_spacex_last_launch
from fetch_nasa import fetch_nasa_apod, fetch_nasa_epic

import time
import os
import telegram
import requests


load_dotenv()
NASA_TOKEN = os.getenv('NASA_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
SCRIPT_DELAY = int(os.getenv('SCRIPT_DELAY'))
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
IMAGES_PATH = 'images'


def get_image_extension_from_url(url):
    url_parts = urlparse(url)
    file_name = os.path.split(url_parts.path)[1]
    file_extension = os.path.splitext(file_name)[1]
    return file_extension


def download_picture(url, image_name):
    response = requests.get(url)
    response.raise_for_status()
    image_extension = get_image_extension_from_url(url)
    file_path = f'{IMAGES_PATH}/{image_name}{image_extension}'

    with open(file_path, 'wb') as file:
        file.write(response.content)


def bulk_download_picture(urls, image_name):
    for count, url in enumerate(urls):
        download_picture(url, f'{image_name}{count}')


def main():
    Path(IMAGES_PATH).mkdir(parents=True, exist_ok=True)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    while True:
        spacex_images_links = fetch_spacex_last_launch()
        nasa_apod_images_links = fetch_nasa_apod(NASA_TOKEN, 30)
        nasa_epic_images_links = fetch_nasa_epic(NASA_TOKEN)
        bulk_download_picture(spacex_images_links, 'spacex')
        bulk_download_picture(nasa_apod_images_links, 'apod')
        bulk_download_picture(nasa_epic_images_links, 'epic')
        images = os.listdir(IMAGES_PATH)
        for image in images:
            with open(f'{IMAGES_PATH}/{image}', 'rb') as image_file:
                bot.send_document(chat_id=TG_CHAT_ID, document=image_file)
            time.sleep(SCRIPT_DELAY)


if __name__ == '__main__':
    main()

