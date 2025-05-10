from pyrogram import Client, filters
from info import API_ID, API_HASH, BOT_TOKEN
from commands import start_command, channels_command, setchannels_command
from script import auto_download_and_upload
import asyncio

app = Client("scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def handle_start(client, message):
    await start_command(client, message)

@app.on_message(filters.command("status"))
async def handle_status(client, message):
    await message.reply("✅ Bot is running.")

@app.on_message(filters.command("scrape"))
async def handle_scrape(client, message):
    await message.reply("🔁 Starting scrape and upload...")
    await auto_download_and_upload(client)
    await message.reply("✅ Done uploading new files.")

@app.on_message(filters.command("channels"))
async def handle_channels(client, message):
    await channels_command(client, message)

@app.on_message(filters.command("setchannels"))
async def handle_setchannels(client, message):
    await setchannels_command(client, message)

if __name__ == "__main__":
    app.run()
