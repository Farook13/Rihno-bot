import logging
import logging.config
import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from config import *
from database import Database
from utils import get_file_size
from aiohttp import web
from plugins import web_server # Placeholder for web server (optional)

# Logging Configuration
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Initialize Bot
bot = Client(
 "MovieBot",
 api_id=API_ID,
 api_hash=API_HASH,
 bot_token=BOT_TOKEN
)

# Initialize Database
db = Database()

# Temporary storage for bot info
temp = type('Temp', (), {})()

async def start_bot():
 print('\nStarting Telegram Movie Bot...')
 bot_info = await bot.get_me()
 temp.U_NAME = bot_info.username
 temp.B_NAME = bot_info.first_name
 bot.username = f'@{bot_info.username}'

 # Web server setup (optional, for Heroku/Render compatibility)
 
 LOGGER.info(f"{temp.B_NAME} started with Pyrogram on @{temp.U_NAME}")
 LOGGER.info(LOG_STR)

# Handlers
@bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
 await message.reply_text(f"Welcome! Forward movie files to index them.\nSupport: {SUPPORT_CHAT}")

@bot.on_message(filters.forwarded & (filters.document | filters.video))
async def handle_file(client: Client, message: Message):
 file = message.document or message.video
 file_data = {
 "file_id": file.file_id,
 "file_name": file.file_name or "Unnamed",
 "caption": message.caption or "",
 "size": get_file_size(file),
 "chat_id": message.chat.id,
 "message_id": message.message_id
 }
 if db.insert_file(file_data):
 await message.reply_text(f"Indexed: {file_data['file_name']}")
 else:
 await message.reply_text("File already indexed.")

@bot.on_message(filters.command("search"))
async def search(client: Client, message: Message):
 query = " ".join(message.command[1:])
 if not query:
 await message.reply_text("Use: /search <query>")
 return

 results = db.search_files(query)
 if not results:
 await message.reply_text("No results found.")
 return

 response = "Found:\n"
 for i, r in enumerate(results, 1):
 response += f"{i}. {r['file_name']} ({r['size']})\n"
 await message.reply_text(response)

async def main():
 await bot.start()
 await start_bot()
 await idle()
 await bot.stop()
 db.close()

if __name__ == "__main__":
 try:
 asyncio.run(main())
 LOGGER.info("Bot running...")
 except KeyboardInterrupt:
 LOGGER.info("Bot stopped.")