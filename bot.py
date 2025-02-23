import logging
import logging.config
import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from config import *
from database import Database
from utils import get_file_size
from aiohttp import web

# Logging Configuration
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

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

# Web server function with port 8000
async def web_server():
    async def hello(request):
        return web.Response(text="Telegram Movie Bot is running!")
    
    app = web.Application()
    app.router.add_get('/', hello)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)  # Hardcoded port 8000
    await site.start()
    return runner

async def start_bot():
    print('\nStarting Telegram Movie Bot...')
    bot_info = await bot.get_me()
    temp.U_NAME = bot_info.username
    temp.B_NAME = bot_info.first_name
    bot.username = f'@{bot_info.username}'
    LOGGER.info(f"{temp.B_NAME} started with Pyrogram on @{temp.U_NAME}")
    LOGGER.info(LOG_STR)

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
    if not results or results.count() == 0:
        await message.reply_text("No results found.")
        return

    response = "Found:\n"
    for i, r in enumerate(results, 1):
        response += f"{i}. {r['file_name']} ({r['size']})\n"
    await message.reply_text(response)

async def main():
    # Start web server if on Heroku/Koyeb
    web_runner = None
    if ON_HEROKU:  # Assuming ON_HEROKU is in your config
        web_runner = await web_server()
        LOGGER.info("Web server started on port 8000")  # Updated log message

    try:
        # Attempt to start bot with flood wait handling
        while True:
            try:
                await bot.start()
                break  # Exit loop if successful
            except FloodWait as e:
                wait_time = e.value  # Get wait time in seconds
                LOGGER.warning(f"Flood wait triggered. Waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            except Exception as e:
                LOGGER.error(f"Unexpected error during start: {str(e)}", exc_info=True)
                raise

        await start_bot()
        LOGGER.info("Connected to MongoDB")  # Assuming this is logged by Database
        await idle()  # Keeps bot running
    except Exception as e:
        LOGGER.error(f"An error occurred: {str(e)}", exc_info=True)
    finally:
        # Check if bot is still running before stopping
        if bot.is_initialized and not bot.is_stopped:
            await bot.stop()
        if web_runner:
            await web_runner.cleanup()
        db.close()
        LOGGER.info("Bot stopped.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER.info("Received interrupt, shutting down...")
    finally:
        if not loop.is_closed():
            loop.close()