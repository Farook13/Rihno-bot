import asyncio
import random
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, API_ID, API_HASH, OWNER_ID, AUTO_DELETE_TIME, AUTH_CHANNEL
from database import Database
from utils import check_force_sub

logger = logging.getLogger(__name__)

app = Client("Rihno2k_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, workers=4)
db = Database()

REACTIONS = ["🔥", "✨", "😍", "🌝", "💥", "⚡️", "🎉", "🎊", "🪄", "💗", "❤️", "💞", "💛", "💖", "💙", "❤️‍🩹", "❤️‍🔥", "💎", "🧨", "💣"]

JOIN_CHANNEL_TEXT = "Please join our channel to use this bot!"
CHANNEL_URL = "https://t.me/+your_channel"  # Replace with your actual channel invite link
JOIN_CHANNEL_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel", url=CHANNEL_URL)]])
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
    welcome_text = (
        f"*Hello! I’m Rihno2k_bot!* {reaction}\n"
        f"I’m here to help you find files with an autofilter system. "
        f"My creator is <a href='tg://user?id={OWNER_ID}'>my owner</a>, the genius behind my code! "
        f"Use me to search files, check credits, or add me to your group.\n\n"
        f"What would you like to do? _{reaction}_"
    )
    
    start_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add to Group", url="https://t.me/Rihno2k_bot?startgroup=true")],
        [InlineKeyboardButton("Support", url="https://t.me/+your_support_channel"),  # Replace with support link
         InlineKeyboardButton("Help", callback_data="help")]
    ])
    
    await db.ensure_user(user_id)
    reply = await message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=start_buttons,
        disable_web_page_preview=True
    )
    await asyncio.sleep(AUTO_DELETE_TIME)
    await reply.delete()

@app.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query):
    help_text = (
        "*Rihno2k_bot Help*\n"
        "Here’s what I can do:\n"
        "- Search files by typing a query.\n"
        "- /credits: Check your credits.\n"
        "- /index <file_name> <file_link>: Add files (admin only).\n"
        "- /addcredits <user_id> <amount>: Add credits (admin only).\n"
        "Enjoy! ✨"
    )
    await callback_query.answer()
    await callback_query.message.edit_text(help_text, parse_mode="Markdown")

@app.on_message(filters.text & filters.private)
async def filter_handler(client, message):
    user_id = message.from_user.id
    if not await check_force_sub(client, user_id):
        await message.reply_text(JOIN_CHANNEL_TEXT, reply_markup=JOIN_CHANNEL_MARKUP)
        return
    
    credits = await db.get_user_credits(user_id)
    if credits < 1:
        reply = await message.reply_text(LOW_CREDITS_TEXT)
        await asyncio.sleep(AUTO_DELETE_TIME)
        await reply.delete()
        return
    
    query = message.text.strip().lower()
    results = await db.search_files(query)
    response = "\n".join(f"{i}. [{r['file_name']}]({r['file_link']})" for i, r in enumerate(results[:10], 1)) if results else NO_FILES_TEXT
    
    if results:
        await db.update_user_credits(user_id, -1)
    
    reply = await message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)
    await asyncio.sleep(AUTO_DELETE_TIME)
    await reply.delete()

@app.on_message(filters.command("index") & filters.user(OWNER_ID))
async def index_file(client, message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            reply = await message.reply_text(INDEX_USAGE_TEXT)
            await asyncio.sleep(AUTO_DELETE_TIME)
            await reply.delete()
            return
        _, file_name, file_link = parts
        await db.add_file(file_name, file_link)
        reply = await message.reply_text(f"Indexed: *{file_name}* successfully! ✨")
        await asyncio.sleep(AUTO_DELETE_TIME)
        await reply.delete()
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.command("credits") & filters.private)
async def check_credits(client, message):
    user_id = message.from_user.id
    credits = await db.get_user_credits(user_id)
    reply = await message.reply_text(f"Your credits: *{credits}* ⭐")
    await asyncio.sleep(AUTO_DELETE_TIME)
    await reply.delete()

@app.on_message(filters.command("addcredits") & filters.user(OWNER_ID))
async def add_credits(client, message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3 or not parts[1].isdigit():
            reply = await message.reply_text("Usage: /addcredits <user_id> <amount>")
            await asyncio.sleep(AUTO_DELETE_TIME)
            await reply.delete()
            return
        _, target_user_id, amount = parts
        target_user_id, amount = int(target_user_id), int(amount)
        await db.update_user_credits(target_user_id, amount)
        reply = await message.reply_text(f"Added {amount} credits to user {target_user_id}! 💰")
        await asyncio.sleep(AUTO_DELETE_TIME)
        await reply.delete()
    except Exception as e:
        logger.error(f"Add credits error: {e}")
        await message.reply_text(f"Error: {str(e)}")
        
        
import asyncio
import logging
import logging.config
from aiohttp import web
from bot import app, db

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="OK", status=200)

async def run_http_server():
    app_web = web.Application()
    app_web.add_routes([web.get('/', health_check)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    logger.info("Health check server running on port 8000")
    return runner

async def main():
    logger.info("Starting RihnoBot...")
    http_runner = await run_http_server()
    try:
        await app.start()
        await asyncio.Future()
    finally:
        await app.stop()
        await db.close()
        await http_runner.cleanup()
        logger.info("RihnoBot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")