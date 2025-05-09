import asyncio
from pyrogram import Client, filters
from commands import auto_scrape_and_send, status, start, set_channels_cmd, set_urls_cmd, get_urls_cmd
from info import API_ID, API_HASH, BOT_TOKEN

app = Client("scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("status"))
async def status_cmd(client, message):
    await status(client, message)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await start(client, message)

@app.on_message(filters.command("channels"))
async def channels_cmd(client, message):
    await set_channels_cmd(client, message)

@app.on_message(filters.command("urls"))
async def urls_cmd(client, message):
    await set_urls_cmd(client, message)

@app.on_message(filters.command("geturls"))
async def get_urls_cmd(client, message):
    await get_urls_cmd(client, message)

async def scheduler():
    while True:
        await auto_scrape_and_send(app)
        await asyncio.sleep(300)  # Run every 5 minutes

async def main():
    await app.start()
    asyncio.create_task(scheduler())
    print("Bot is running...")
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
