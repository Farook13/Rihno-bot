import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Telegram Bot Token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram API ID and Hash from my.telegram.org
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# MongoDB Configuration
DATABASE_URI = os.getenv("DATABASE_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "AutoFilterBotDB")

# Force Subscribe Channel ID (e.g., -100123456789)
AUTH_CHANNEL = os.getenv("AUTH_CHANNEL")

# Log Channel ID for bot activities
LOG_CHANNEL = os.getenv("LOG_CHANNEL")

# Bot Owner ID
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))

# Auto-delete time in seconds (e.g., 60 seconds)
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "60"))
