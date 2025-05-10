import asyncio
from pyrogram import Client, idle
from aiohttp import web
import os
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# Pyrogram client
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Import handlers so they get registered
import commands  # <- this must import decorators using the same `app` instance

# Aiohttp web server for health check
async def handle(request):
    return web.Response(text="Bot is running")

async def run_web():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    logger.info("Health check server started on port 8000.")

# Main
async def main():
    await run_web()
    await app.start()
    logger.info("Bot started.")
    await idle()  # <- Keeps it running
    await app.stop()
    logger.info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot exited.")
