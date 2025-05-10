from pymongo import MongoClient
from info import MONGODB_URL

client = MongoClient(MONGODB_URL)
db = client['scraper_bot']
files = db['uploaded_files']
channels = db['upload_channels']

def file_exists(url):
    """Check if the file URL has already been uploaded"""
    return files.find_one({"url": url}) is not None

def store_file(url, filename):
    """Store the uploaded file's URL and filename"""
    files.insert_one({"url": url, "filename": filename})

def get_channels():
    """Fetches all channels from the database"""
    return [channel['channel_id'] for channel in channels.find()]

def add_channel(channel_id):
    """Adds a new channel to the database"""
    if not channels.find_one({"channel_id": channel_id}):
        channels.insert_one({"channel_id": channel_id})

def remove_channel(channel_id):
    """Removes a channel from the database"""
    channels.delete_one({"channel_id": channel_id})
