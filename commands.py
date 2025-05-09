# commands.py
from pyrogram import Client, filters
import requests
import os
import logging
from script import get_file_links
from database import (
    file_exists, store_file,
    get_private_channels, set_private_channels,
    get_target_urls, set_target_urls
)
from info import OWNER_ID

# Setting up logging
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("bot.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Auto scrape and upload to private channels
async def auto_scrape_and_send(app: Client):
    private_channels = get_private_channels()
    urls = get_target_urls()
    
    if not private_channels:
        logger.error("No private channels set. Exiting...")
        return

    for url in urls:
        try:
            links = get_file_links(url)
            if not links:
                continue

            for link in links:
                if file_exists(link):
                    continue

                filename = link.split("/")[-1]
                try:
                    response = requests.get(link, stream=True)
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                f.write(chunk)

                    for channel_id in private_channels:
                        await app.send_document(chat_id=channel_id, document=filename, caption=f"Uploaded: {filename}")

                    os.remove(filename)
                    store_file(link, filename)
                    logger.info(f"Uploaded: {filename} from {link}")
                except Exception as e:
                    logger.error(f"Error downloading {link}: {e}")
                    await app.send_message(chat_id=OWNER_ID, text=f"❌ Failed to upload: {filename}\nError: {str(e)}")
        except Exception as e:
            logger.error(f"Scrape error for {url}: {e}")
            await app.send_message(chat_id=OWNER_ID, text=f"❌ Scrape failed for URL: {url}\nError: {str(e)}")

# Command to set private channel IDs
async def set_private_channels_cmd(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ You are not authorized to change private channels.")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ Usage: /setchannels -1001234567890 -1009876543210")
        return

    raw_text = message.text.split(" ", 1)[1]
    channel_list = [ch.strip() for ch in raw_text.split() if ch.strip()]  # Space-separated
    set_private_channels(channel_list)
    await message.reply(f"✅ Updated private channels list:\n\n" + "\n".join(channel_list))

# Command to check bot status
async def status(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ You are not authorized to use this command.")
        return
    await message.reply("🤖 Bot is running and authorized.")

# Command to show bot startup message
async def start(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("🔒 This is a private bot owned by @SA_Bots. You are not authorized to use it.")
    else:
        await message.reply("👋 Welcome back! You are authorized.")

# Command to set target URLs
async def set_urls_cmd(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ You are not authorized to change URLs.")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ Usage: /urls https://site1.com https://site2.com https://site3.com")
        return

    raw_text = message.text.split(" ", 1)[1]
    url_list = [url.strip() for url in raw_text.split() if url.strip()]  # Space-separated
    set_target_urls(url_list)
    await message.reply(f"✅ Updated target URLs:\n\n" + "\n".join(url_list))

# Command to get current target URLs
async def get_urls_cmd(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ You are not authorized to view the URLs.")
        return

    urls = get_target_urls()
    if urls:
        await message.reply(f"📋 Current Target URLs:\n\n" + "\n".join(urls))
    else:
        await message.reply("⚠️ No target URLs set yet.")
