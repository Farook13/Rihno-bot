import asyncio
import random
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import Database
from utils import check_force_sub

# Initialize the bot
app = Client("RihnoBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
db = Database()
REACTIONS = ["😘", "🥳", "🤩", "💥", "🔥", "⚡️", "✨", "💎", "💗"]

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
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

# Autofilter
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

# Admin command
@app.on_message(filters.command("addfile") & filters.user(Config.OWNER_ID))
async def add_file(client, message):
    try:
        _, file_name, file_link = message.text.split(maxsplit=2)
        db.add_file(file_name, file_link)
        reply = await message.reply_text(f"Added {file_name} to the database!")
        await asyncio.sleep(Config.AUTO_DELETE_TIME)
        await reply.delete()
    except ValueError:
        await message.reply_text("Usage: /addfile <file_name> <file_link>")

if __name__ == "__main__":
    print("Starting Rihno Bot...")
    app.start()
    idle()
    app.stop()
    print("Rihno Bot stopped.")


from pyrogram import Client, idle
from config import Config
from handlers import start, filter, admin  # Import handler modules

# Initialize the bot with config values
app = Client(
    "RihnoBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Register handlers (assuming they define their own message handlers)
start.register(app)
filter.register(app)
admin.register(app)

if __name__ == "__main__":
    print("Starting Rihno Bot...")
    app.start()
    idle()  # Keep the bot running
    app.stop()
    print("Rihno Bot stopped.")