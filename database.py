import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")  # Your MongoDB URL
db = client["file_bot"]
files_collection = db["files"]
settings_collection = db["settings"]

def file_exists(url):
    return files_collection.find_one({"url": url}) is not None

def store_file(url, filename):
    files_collection.insert_one({"url": url, "filename": filename})

def get_channels():
    data = settings_collection.find_one({"_id": "channels"})
    return data["list"] if data else []

def set_channels(channels):
    settings_collection.update_one({"_id": "channels"}, {"$set": {"list": channels}}, upsert=True)

def get_target_urls():
    data = settings_collection.find_one({"_id": "target_urls"})
    return data["list"] if data else []

def set_target_urls(urls):
    settings_collection.update_one({"_id": "target_urls"}, {"$set": {"list": urls}}, upsert=True)
