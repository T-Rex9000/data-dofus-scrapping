import requests
from bs4 import BeautifulSoup


def url_to_soup(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    return soup
