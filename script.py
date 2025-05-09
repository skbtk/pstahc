import requests
from bs4 import BeautifulSoup

def get_file_links(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if any(href.endswith(ext) for ext in ['.pdf', '.zip', '.mp4', '.mp3', '.mkv']):
            links.append(href)
    return links
