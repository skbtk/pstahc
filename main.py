from pyrogram import Client, filters
from info import API_ID, API_HASH, BOT_TOKEN
from commands import (
    start, status,
    set_private_channels_cmd, set_urls_cmd,
    get_urls_cmd
)

app = Client("file_scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def handle_start(client, message):
    await start(client, message)

@app.on_message(filters.command("status"))
async def handle_status(client, message):
    await status(client, message)

@app.on_message(filters.command("setchannels"))
async def handle_set_channels(client, message):
    await set_private_channels_cmd(client, message)

@app.on_message(filters.command("urls"))
async def handle_set_urls(client, message):
    await set_urls_cmd(client, message)

@app.on_message(filters.command("geturls"))
async def handle_get_urls(client, message):
    await get_urls_cmd(client, message)

if __name__ == "__main__":
    app.run()
