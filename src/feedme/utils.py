import requests
from bs4 import BeautifulSoup


def url_to_soup(url):
    with requests.get(url) as response:
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    return soup