import logging
import logging.config
import os
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserNotParticipant
from config import *
from database import Database
from utils import get_file_size
from aiohttp import web
import aiohttp

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

# Required channels (add these to config.py)
FORCE_SUB_CHANNELS = ["@YourChannel1", "@YourChannel2"]  # Add your channel usernames

# OMDB API key (add this to config.py)
OMDB_API_KEY = "your_omdb_api_key_here"  # Get from http://www.omdbapi.com/

# Web server function with port 8000
async def web_server():
    async def hello(request):
        return web.Response(text="Telegram Movie Bot is running!")
    
    app = web.Application()
    app.router.add_get('/', hello)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    return runner

# Check if user is subscribed to required channels
async def check_subscription(client, user_id):
    for channel in FORCE_SUB_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            return channel
    return None

async def start_bot():
    print('\nStarting Telegram Movie Bot...')
    bot_info = await bot.get_me()
    temp.U_NAME = bot_info.username
    temp.B_NAME = bot_info.first_name or "Batman2"
    bot.username = f'@{bot_info.username}'
    LOGGER.info(f"{temp.B_NAME} started with Pyrogram on @{temp.U_NAME}")
    LOGGER.info("Bot Configuration:\n"
                "IMDB enabled.\n"
                "Custom caption: <b>{file_caption}</b>\n"
                "Size: {file_size}\n"
                "Uploaded by {SUPPORT_CHAT}\n"
                "Auto-delete after 600 seconds.")

@bot.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    user_id = message.from_user.id
    unsubscribed_channel = await check_subscription(client, user_id)
    if unsubscribed_channel:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{unsubscribed_channel[1:]}")]
        ])
        await message.reply_text(
            f"Please join {unsubscribed_channel} to use this bot!",
            reply_markup=keyboard
        )
        return
    await message.reply_text(f"Welcome! Send movie files to index them or use /imdb <title>.\nSupport: {SUPPORT_CHAT}")

@bot.on_message(filters.document | filters.video)
async def handle_file(client: Client, message: Message):
    user_id = message.from_user.id
    unsubscribed_channel = await check_subscription(client, user_id)
    if unsubscribed_channel:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{unsubscribed_channel[1:]}")]
        ])
        await message.reply_text(
            f"Please join {unsubscribed_channel} to use this bot!",
            reply_markup=keyboard
        )
        return
    
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
    user_id = message.from_user.id
    unsubscribed_channel = await check_subscription(client, user_id)
    if unsubscribed_channel:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{unsubscribed_channel[1:]}")]
        ])
        await message.reply_text(
            f"Please join {unsubscribed_channel} to use this bot!",
            reply_markup=keyboard
        )
        return
    
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

@bot.on_message(filters.command("imdb"))
async def imdb_search(client: Client, message: Message):
    user_id = message.from_user.id
    unsubscribed_channel = await check_subscription(client, user_id)
    if unsubscribed_channel:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{unsubscribed_channel[1:]}")]
        ])
        await message.reply_text(
            f"Please join {unsubscribed_channel} to use this bot!",
            reply_markup=keyboard
        )
        return
    
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("Use: /imdb <movie title>")
        return
    
    async with aiohttp.ClientSession() as session:
        url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
        async with session.get(url) as resp:
            data = await resp.json()
            if data["Response"] == "False":
                await message.reply_text("Movie not found on IMDb.")
                return
            response = (f"**{data['Title']} ({data['Year']})**\n"
                       f"Rating: {data['imdbRating']}/10\n"
                       f"Plot: {data['Plot']}\n"
                       f"More: https://www.imdb.com/title/{data['imdbID']}/")
            await message.reply_text(response)

@bot.on_message(filters.command("getfile"))
async def get_file(client: Client, message: Message):
    user_id = message.from_user.id
    unsubscribed_channel = await check_subscription(client, user_id)
    if unsubscribed_channel:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{unsubscribed_channel[1:]}")]
        ])
        await message.reply_text(
            f"Please join {unsubscribed_channel} to use this bot!",
            reply_markup=keyboard
        )
        return
    
    file_name = " ".join(message.command[1:])
    if not file_name:
        await message.reply_text("Use: /getfile <file_name>")
        return
    
    file = db.get_file_by_name(file_name)  # Assumes this method exists in Database
    if not file:
        await message.reply_text("File not found.")
        return
    
    await client.send_document(
        chat_id=message.chat.id,
        document=file["file_id"],
        caption=file["caption"] or file["file_name"]
    )

async def main():
    web_runner = await web_server()
    LOGGER.info("Web server started on port 8000")

    try:
        while True:
            try:
                await bot.start()
                break
            except FloodWait as e:
                wait_time = e.value
                LOGGER.warning(f"Flood wait triggered. Waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            except Exception as e:
                LOGGER.error(f"Unexpected error during start: {str(e)}", exc_info=True)
                raise

        await start_bot()
        LOGGER.info("Connected to MongoDB")
        await idle()
    except Exception as e:
        LOGGER.error(f"An error occurred: {str(e)}", exc_info=True)
    finally:
        try:
            await bot.stop()
        except Exception as e:
            LOGGER.error(f"Error stopping bot: {str(e)}", exc_info=True)
        await web_runner.cleanup()
        db.close()
        LOGGER.info("Bot stopped.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER.info("Received interrupt, shutting down...")
    except Exception as e:
        LOGGER.error(f"Main loop error: {str(e)}", exc_info=True)
    finally:
        if not loop.is_closed():
            loop.close()