import asyncio
from pyrogram import filters
from config import Config
from database import Database

db = Database()

def register(app):
    @app.on_message(filters.command("addfile") & filters.user(Config.OWNER_ID))
    async def add_file_handler(client, message):
        try:
            _, file_name, file_link = message.text.split(maxsplit=2)
            db.add_file(file_name, file_link)
            reply = await message.reply_text(f"Added {file_name} to the database!")
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            await reply.delete()
        except ValueError:
            await message.reply_text("Usage: /addfile <file_name> <file_link>")