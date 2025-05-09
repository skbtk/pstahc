# database.py
from pymongo import MongoClient
from info import MONGODB_URL

client = MongoClient(MONGODB_URL)
db = client['file_bot']

# File collection (store already uploaded files)
file_collection = db['files']

# URLs collection (store target URLs)
urls_collection = db['urls']

# Channels collection (store private channels)
channels_collection = db['channels']

def file_exists(link):
    return file_collection.find_one({"link": link}) is not None

def store_file(link, filename):
    file_collection.insert_one({"link": link, "filename": filename})

def get_target_urls():
    urls = urls_collection.find()
    return [url['url'] for url in urls]

def set_target_urls(url_list):
    urls_collection.delete_many({})  # Clear the current URLs
    for url in url_list:
        urls_collection.insert_one({"url": url})

def get_private_channels():
    channels = channels_collection.find()
    return [channel['channel_id'] for channel in channels]

def set_private_channels(channel_list):
    channels_collection.delete_many({})  # Clear the current channels
    for channel in channel_list:
        channels_collection.insert_one({"channel_id": channel})
