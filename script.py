import asyncio
import random
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, API_ID, API_HASH, AUTH_CHANNEL, LOG_CHANNEL, OWNER_ID, AUTO_DELETE_TIME
from database import Database
from utils import check_force_sub

# Initialize the bot
app = Client("AutoFilterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# MongoDB instance
db = Database()

# List of reaction emojis
REACTIONS = ["😘", "🥳", "🤩", "💥", "🔥", "⚡️", "✨", "💎", "💗"]

# Start command with random reaction
@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    user_id = message.from_user.id
    if not await check_force_sub(client, user_id):
        await message.reply_text(
            "Please join our channel to use this bot!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{AUTH_CHANNEL[4:]}")]]
            )
        )
        return
    
    # Pick a random reaction emoji
    reaction = random.choice(REACTIONS)
    reply = await message.reply_text(
        f"Welcome to the AutoFilter Bot! Send me a query to search for files. {reaction}"
    )
    # Log user activity
    await client.send_message(LOG_CHANNEL, f"User {user_id} started the bot.")
    # Auto-delete the welcome message after AUTO_DELETE_TIME seconds
    await asyncio.sleep(AUTO_DELETE_TIME)
    await reply.delete()

# Autofilter functionality
@app.on_message(filters.text & filters.private)
async def autofilter(client: Client, message: Message):
    user_id = message.from_user.id
    if not await check_force_sub(client, user_id):
        await message.reply_text(
            "Please join our channel to use this bot!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{AUTH_CHANNEL[4:]}")]]
            )
        )
        return
    
    query = message.text
    results = await asyncio.to_thread(db.search_files, query)
    if results:
        response = "Here
if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) > 1 and sys.argv[1].lower() == "help":
        print_help()
        sys.exit(0)
    
    # Default behavior: run the bot
app.run()
