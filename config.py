import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Telegram Bot Token from @BotFather

# Telegram API ID and Hash from my.telegram.org
API_ID = int(environ.get("12618934"))
API_HASH = os.getenv("49aacd0bc2f8924add29fb02e20c8a16")

BOT_TOKEN = environ.get('BOT_TOKEN', '7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E')
# MongoDB Configuration
DATABASE_URI = environ.get("mongodb+srv: //farook:farook@cluster0.dmaou.mongodb.net/")
DATABASE_NAME = environ.get("DATABASE_NAME", "Farook")

# Force Subscribe Channel ID (e.g., -100123456789)
AUTH_CHANNEL = environ.get("-1002256041072")

# Log Channel ID for bot activities
LOG_CHANNEL = environ.get("-1002467149516")

# Bot Owner ID
OWNER_ID = int(environ.get("OWNER_ID", "5032034594"))
# Auto-delete time in seconds (e.g., 60 seconds)
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "30"))
