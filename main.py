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