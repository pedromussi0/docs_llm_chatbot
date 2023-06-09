import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.conf import settings


def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = []

    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            absolute_url = urljoin(url, href)  # Convert relative URL to absolute URL
            links.append(absolute_url)

    return links
