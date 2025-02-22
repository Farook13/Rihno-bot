import asyncio
import random
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import Database
from utils import check_force_sub

logger = logging.getLogger(__name__)

app = Client("RihnoBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, workers=4)
db = Database()

REACTIONS = ["🔥", "✨", "😍", "🌝", "💥", "⚡️", "🎉", "🎊", "🪄", "💗", "❤️", "💞", "💛", "💖", "💙", "❤️‍🩹", "❤️‍🔥", "💎", "🧨", "💣"]

JOIN_CHANNEL_TEXT = "Please join our channel to use this bot!"
JOIN_CHANNEL_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel", url=Config.CHANNEL_URL)]])
NO_FILES_TEXT = "No files found for your query."
INDEX_USAGE_TEXT = "Usage: /index <file_name> <file_link>"
LOW_CREDITS_TEXT = "Insufficient credits! You need at least 1 credit to search."

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    if not await check_force_sub(client, user_id):
        await message.reply_text(JOIN_CHANNEL_TEXT, reply_markup=JOIN_CHANNEL_MARKUP)
        return
    
    reaction = random.choice(REACTIONS)
    welcome_text = f"*Welcome to RihnoBot!* {reaction}\nSearch files or use /credits to check your balance! _{reaction}_"
    
    await db.ensure_user(user_id)
    reply = await message.reply_text(welcome_text, parse_mode="Markdown")
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await reply.delete()

async def filter_handler(client, message):
    user_id = message.from_user.id
    # ... (force sub check)
    credits = await db.get_user_credits(user_id)
    if credits < 1:
        # ... (low credits response)
        return
    query = message.text.strip().lower()
    results = await db.search_files(query)
    response = "\n".join(f"{i}. [{r['file_name']}]({r['file_link']})" for i, r in enumerate(results[:10], 1)) if results else NO_FILES_TEXT
    if results:
        asyncio.create_task(db.update_user_credits(user_id, -1))  # Async task, non-blocking
    reply = await message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await reply.delete()
    
    query = message.text.strip().lower()
    results = await db.search_files(query)
    response = "\n".join(f"{i}. [{r['file_name']}]({r['file_link']})" for i, r in enumerate(results[:10], 1)) if results else NO_FILES_TEXT
    
    if results:
        await db.update_user_credits(user_id, -1)
    
    reply = await message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await reply.delete()

@app.on_message(filters.command("index") & filters.user(Config.ADMIN_IDS))
async def index_file(client, message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            reply = await message.reply_text(INDEX_USAGE_TEXT)
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            await reply.delete()
            return
        _, file_name, file_link = parts
        await db.add_file(file_name, file_link)
        reply = await message.reply_text(f"Indexed: *{file_name}* successfully! ✨")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await reply.delete()
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.command("credits") & filters.private)
async def check_credits(client, message):
    user_id = message.from_user.id
    credits = await db.get_user_credits(user_id)
    reply = await message.reply_text(f"Your credits: *{credits}* ⭐")
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await reply.delete()

@app.on_message(filters.command("addcredits") & filters.user(Config.ADMIN_IDS))
async def add_credits(client, message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3 or not parts[1].isdigit():
            reply = await message.reply_text("Usage: /addcredits <user_id> <amount>")
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            await reply.delete()
            return
        _, target_user_id, amount = parts
        target_user_id, amount = int(target_user_id), int(amount)
        await db.update_user_credits(target_user_id, amount)
        reply = await message.reply_text(f"Added {amount} credits to user {target_user_id}! 💰")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await reply.delete()
    except Exception as e:
        logger.error(f"Add credits error: {e}")
        await message.reply_text(f"Error: {str(e)}")