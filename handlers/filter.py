import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import Database
from utils import check_force_sub

db = Database()

def register(app):
    @app.on_message(filters.text & filters.private)
    async def filter_handler(client, message):
        user_id = message.from_user.id
        if not await check_force_sub(client, user_id):
            await message.reply_text(
                "Please join our channel to use this bot!",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{Config.AUTH_CHANNEL[4:]}")]]
                )
            )
            return
        query = message.text
        results = await asyncio.to_thread(db.search_files, query)
        if results:
            response = "Here are the files I found:\n\n"
            for idx, result in enumerate(results[:10], 1):
                response += f"{idx}. {result['file_name']} - [Link]({result['file_link']})\n"
            reply = await message.reply_text(response, disable_web_page_preview=True)
        else:
            reply = await message.reply_text("No files found for your query.")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await reply.delete()