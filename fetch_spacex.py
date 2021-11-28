import requests


def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v4/launches/5eb87ce3ffd86e000604b336')
    response.raise_for_status()
    images_links = response.json()['links']['flickr']['original']
    return images_links

