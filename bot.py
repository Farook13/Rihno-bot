import asyncio
from aiohttp import web
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton  # Correct import
from config import Config
from database import Database
from utils import check_force_sub

# Preload reactions
REACTIONS = ("😘", "🥳", "🤩", "💥", "🔥", "⚡️", "✨", "💎", "💗")

# Example for Python/Telebot
print("Bot is alive and listening...")
@bot.message_handler(commands=['start'])
def handle_start(message):
    print("Received /start command!")
    bot.reply_to(message, "Hello from Rihno Bot!")

# Validate credentials at startup
if not all([Config.BOT_TOKEN, Config.API_ID, Config.API_HASH]):
    print("Critical Error: Missing Telegram API credentials (BOT_TOKEN, API_ID, or API_HASH)")
    exit(1)
print(f"Credentials loaded: BOT_TOKEN={Config.BOT_TOKEN[:5]}..., API_ID={Config.API_ID}, API_HASH={Config.API_HASH[:5]}...")

# Initialize bot and database
app = Client(
    "RihnoBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=4
)
db = Database()

# Predefine responses and markup with correct Pyrogram types
JOIN_CHANNEL_MARKUP = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{Config.AUTH_CHANNEL[4:]}")]]
)
JOIN_CHANNEL_TEXT = "Please join our channel to use this bot!"
NO_FILES_TEXT = "No files found for your query."
ADD_FILE_USAGE_TEXT = "Usage: /addfile <file_name> <file_link>"

@app.on_message(filters.command("start") & filters.private, group=0)
async def start(client, message):
    user_id = message.from_user.id
    print(f"Received /start from user {user_id}")
    try:
        if not await check_force_sub(client, user_id):
            print(f"User {user_id} not subscribed to {Config.AUTH_CHANNEL}")
            await message.reply_text(JOIN_CHANNEL_TEXT, reply_markup=JOIN_CHANNEL_MARKUP)
            return
        reaction = REACTIONS[user_id % len(REACTIONS)]
        print(f"Sending welcome to {user_id} with reaction {reaction}")
        reply = await message.reply_text(f"Welcome to Rihno Bot! Send me a query to search for files. {reaction}")
        await asyncio.gather(
            client.send_message(Config.LOG_CHANNEL, f"User {user_id} started the bot."),
            asyncio.sleep(Config.AUTO_DELETE_TIME, result=reply.delete())
        )
    except Exception as e:
        print(f"Error in start handler: {e}")

@app.on_message(filters.text & filters.private, group=1)
async def filter_handler(client, message):
    user_id = message.from_user.id
    print(f"Received text query from {user_id}: {message.text}")
    try:
        if not await check_force_sub(client, user_id):
            print(f"User {user_id} not subscribed to {Config.AUTH_CHANNEL}")
            await message.reply_text(JOIN_CHANNEL_TEXT, reply_markup=JOIN_CHANNEL_MARKUP)
            return
        query = message.text
        results = await asyncio.to_thread(db.search_files, query)
        print(f"Found {len(results)} results for '{query}'")
        reply = await message.reply_text(
            "\n".join(f"{i}. {r['file_name']} - [Link]({r['file_link']})" for i, r in enumerate(results[:10], 1)) or NO_FILES_TEXT,
            disable_web_page_preview=True
        )
        await asyncio.sleep(Config.AUTO_DELETE_TIME, result=reply.delete())
    except Exception as e:
        print(f"Error in filter handler: {e}")

@app.on_message(filters.command("addfile") & filters.user(Config.OWNER_ID), group=2)
async def add_file(client, message):
    user_id = message.from_user.id
    print(f"Received /addfile from {user_id}: {message.text}")
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.reply_text(ADD_FILE_USAGE_TEXT)
            return
        _, file_name, file_link = parts
        db.add_file(file_name, file_link)
        print(f"Added file: {file_name}")
        reply = await message.reply_text(f"Added {file_name} to the database!")
        await asyncio.sleep(Config.AUTO_DELETE_TIME, result=reply.delete())
    except Exception as e:
        print(f"Error in add_file handler: {e}")

async def health_check(request):
    return web.Response(body=b"OK", status=200)

async def run_http_server():
    try:
        app_web = web.Application()
        app_web.add_routes([web.get('/', health_check)])
        runner = web.AppRunner(app_web, handle_signals=False)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8000, reuse_address=True)
        await site.start()
        print("Health check server running on port 8000")
        return runner
    except Exception as e:
        print(f"Failed to start HTTP server: {e}")
        raise

async def main():
    print("Starting Rihno Bot...")
    http_runner = await run_http_server()
    try:
        await app.start()
        print("Bot started successfully, listening for messages...")
        await idle()
    except Exception as e:
        print(f"Failed to start bot: {e}")
    finally:
        await app.stop()
        await http_runner.cleanup()
        print("Rihno Bot stopped.")

if __name__ == "__main__":
    asyncio.run(main())