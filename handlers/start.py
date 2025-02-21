import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from utils import check_force_sub

REACTIONS = ["😘", "🥳", "🤩", "💥", "🔥", "⚡️", "✨", "💎", "💗"]

def register(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message):
        user_id = message.from_user.id
        if not await check_force_sub(client, user_id):
            await message.reply_text(
                "Please join our channel to use this bot!",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{Config.AUTH_CHANNEL[4:]}")]]
                )
            )
            return
        reaction = random.choice(REACTIONS)
        reply = await message.reply_text(f"Welcome to Rihno Bot! Send me a query to search for files. {reaction}")
        await client.send_message(Config.LOG_CHANNEL, f"User {user_id} started the bot.")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await reply.delete()