import asyncio
import logging
import random
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import Database

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot client
app = Client(
    "RihnoBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=4
)

# Initialize database
db = Database()

# Reaction emojis
REACTIONS = [
    "🔥", "✨", "😍", "🌝", "💥", "⚡️", "🎉", "🎊", "🪄", "💗",
    "❤️", "💞", "💛", "💖", "💙", "❤️‍🩹", "❤️‍🔥", "💎", "🧨", "💣"
]

# Predefined responses
JOIN_CHANNEL_TEXT = "Please join our channel to use this bot!"
JOIN_CHANNEL_MARKUP = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Join Channel", url=Config.CHANNEL_URL)]]
)
NO_FILES_TEXT = "No files found for your query."
INDEX_USAGE_TEXT = "Usage: /index <file_name> <file_link>"
LOW_CREDITS_TEXT = "Insufficient credits! You need at least 1 credit to search."

# Start command with random reaction
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    if not await check_force_sub(client, user_id):
        await message.reply_text(JOIN_CHANNEL_TEXT, reply_markup=JOIN_CHANNEL_MARKUP)
        return
    
    reaction = random.choice(REACTIONS)
    welcome_text = (
        f"*Welcome to RihnoBot!* {reaction}\n"
        f"Search files, check credits with /credits, or index files if you're an admin! _{reaction}_"
    )
    
    await db.ensure_user(user_id)  # Ensure user exists in DB
    reply = await message.reply_text(welcome_text, parse_mode="Markdown")
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await reply.delete()

# Autofilter handler with credit check
@app.on_message(filters.text & filters.private)
async def filter_handler(client, message):
    user_id = message.from_user.id
    if not await check_force_sub(client, user_id):
        await message.reply_text(JOIN_CHANNEL_TEXT, reply_markup=JOIN_CHANNEL_MARKUP)
        return
    
    credits = await db.get_user_credits(user_id)
    if credits < 1:
        reply = await message.reply_text(LOW_CREDITS_TEXT)
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await reply.delete()
        return
    
    query = message.text.strip().lower()
    results = await db.search_files(query)
    
    if results:
        response = "\n".join(
            f"{i}. [{r['file_name']}]({r['file_link']})" 
            for i, r in enumerate(results[:10], 1)
        )
        await db.update_user_credits(user_id, -1)  # Deduct 1 credit
    else:
        response = NO_FILES_TEXT
    
    reply = await message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await reply.delete()

# Index files (admin only)
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

# Check user credits
@app.on_message(filters.command("credits") & filters.private)
async def check_credits(client, message):
    user_id = message.from_user.id
    credits = await db.get_user_credits(user_id)
    reply = await message.reply_text(f"Your credits: *{credits}* ⭐")
    await asyncio.sleep(Config.AUTO_DELETE_TIME)
    await reply.delete()

# Admin command to add credits
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
        target_user_id = int(target_user_id)
        amount = int(amount)
        
        await db.update_user_credits(target_user_id, amount)
        reply = await message.reply_text(f"Added {amount} credits to user {target_user_id}! 💰")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await reply.delete()
    except Exception as e:
        logger.error(f"Add credits error: {e}")
        await message.reply_text(f"Error: {str(e)}")

# Force subscription check (placeholder)
async def check_force_sub(client, user_id):
    return True  # Replace with real logic if needed

async def main():
    logger.info("Starting RihnoBot...")
    await app.start()
    await idle()
    await app.stop()
    await db.close()
    logger.info("RihnoBot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")