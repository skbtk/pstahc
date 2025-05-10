from pyrogram import Client, filters
from info import OWNER_ID
from database import add_channel, get_channels, remove_channel

async def start_command(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🔒 This is a private bot owned by @SA_Bots.")
    await message.reply("✅ Bot is active and ready.")

async def channels_command(client, message):
    channels = get_channels()
    if not channels:
        await message.reply("❌ No channels are currently set.")
        return
    await message.reply("✅ Current channels:\n" + "\n".join([str(ch) for ch in channels]))

async def setchannels_command(client, message):
    channels = message.text.split()[1:]
    if not channels:
        return await message.reply("❌ You need to provide at least one channel ID.")
    
    for ch in channels:
        try:
            channel_id = int(ch)
            add_channel(channel_id)
            await message.reply(f"✅ Added channel ID: {channel_id}")
        except ValueError:
            await message.reply(f"❌ Invalid channel ID: {ch}")
