from pymongo import MongoClient
from info import MONGODB_URL

client = MongoClient(MONGODB_URL)
db = client['scraper_bot']
files = db['uploaded_files']
channels = db['upload_channels']

def file_exists(url):
    return files.find_one({"url": url}) is not None

def store_file(url, filename):
    files.insert_one({"url": url, "filename": filename})

def get_channels():
    return [channel['channel_id'] for channel in channels.find()]

def add_channel(channel_id):
    if not channels.find_one({"channel_id": channel_id}):
        channels.insert_one({"channel_id": channel_id})
