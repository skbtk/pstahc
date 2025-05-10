import requests, re, time, os
from bs4 import BeautifulSoup as BS
from database import file_exists, store_file, get_channels, add_channel
from info import CHANNELS
import logging

logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("bot.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def safe_get(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=10).text
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

def scrape_tamilblasters():
    base_url = "https://www.1tamilblasters.moi/"
    html = safe_get(base_url)
    if not html:
        return []
    
    soup = BS(html, 'html.parser')
    topic_links = [a['href'] for a in soup.find_all('a', href=True) if re.match(r'https://www\.1tamilblasters\.moi/index\.php\?/forums/topic/\d+', a['href'])]
    download_links = []

    for link in topic_links:
        topic_html = safe_get(link)
        if not topic_html:
            continue
        topic_soup = BS(topic_html, 'html.parser')
        matches = topic_soup.find_all('a', href=re.compile(r"magnet.*|.*\.torrent|.*\.mkv"))
        for a in matches:
            url = a['href']
            if not file_exists(url):
                download_links.append(url)
    return download_links

def scrape_filmyfly():
    page_url = "https://filmyfly.win/page-download/5342/Samajavaragamana-2023-South-Hindi-Dubbed-Movie-HD-ESub.html"
    c = safe_get(page_url)
    if not c:
        return []

    download_links = []
    for l in re.findall(r'https://linkmake\.in/view/\w+', c):
        t = safe_get(l)
        if not t: continue
        for f in re.findall(r'https://new1\.filesdl\.in/cloud/\w+', t):
            d = safe_get(f)
            if not d: continue
            soup = BS(d, 'html.parser')
            for a in soup.find_all('a', href=True):
                if a['href'].startswith('http') and not file_exists(a['href']):
                    download_links.append(a['href'])
    return download_links

async def auto_download_and_upload(client):
    links = scrape_tamilblasters() + scrape_filmyfly()
    for link in links:
        try:
            filename = link.split("/")[-1].split("?")[0]
            r = requests.get(link, stream=True, headers=HEADERS)
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)

            # Get current channels from MongoDB
            channels = get_channels()
            for channel_id in channels:
                await client.send_document(chat_id=channel_id, document=filename, caption=filename)

            store_file(link, filename)
            os.remove(filename)
            logger.info(f"Uploaded: {filename}")
        except Exception as e:
            logger.error(f"Failed to upload {link}: {e}")
