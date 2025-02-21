import re
from os import environ,getenv
from Script import script

# Telegram Bot Token from @BotFather
BOT_TOKEN = environ.get('BOT_TOKEN',"7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E")

# Telegram API ID and Hash from my.telegram.org
API_ID = int(environ.get('API_ID', '17264725'))
API_HASH = environ.get('API_HASH', 'e7c6c1e727962d2ade50bald7f4fac8a')
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