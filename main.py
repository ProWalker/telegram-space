from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

import requests


def download_picture(url, image_name):
    response = requests.get(url)
    response.raise_for_status()
    Path('images').mkdir(parents=True, exist_ok=True)
    file_path = f'images/{image_name}'

    with open(file_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v4/launches/5eb87ce3ffd86e000604b336')
    response.raise_for_status()
    images_links = response.json()['links']['flickr']['original']
    for image_number, url in enumerate(images_links):
        download_picture(url, f'spacex{image_number}.jpg')


def get_image_extension_from_url(url):
    pass

if __name__ == '__main__':
    load_dotenv()
    # fetch_spacex_last_launch()
    image_extension = get_image_extension_from_url('https://example.com/txt/hello%20world.txt?v=9#python')
    print(image_extension)