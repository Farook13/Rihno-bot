import re
from os import environ,getenv
from Script import script

# Telegram Bot Token from @BotFather
BOT_TOKEN = environ.get('BOT_TOKEN',"7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E")

# Telegram API ID and Hash from my.telegram.org
class Config:
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

AUTO_DELETE_TIME = int(environ.get("AUTO_DELETE_TIME", "60"))




import os
from os import environ  # Assuming environ is used as in the error

# Configuration class or direct variables
class Config:  # If using a class, ensure proper indentation
    BOT_TOKEN = environ.get('7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E')
    API_ID = int(environ.get('API_ID', '17264725'))
    API_HASH = environ.get('API_HASH')
    DATABASE_URI = environ.get('DATABASE_URI')
    DATABASE_NAME = environ.get('DATABASE_NAME', 'AutoFilterBotDB')
    AUTH_CHANNEL = environ.get('AUTH_CHANNEL')
    LOG_CHANNEL = environ.get('LOG_CHANNEL')
    OWNER_ID = int(environ.get('OWNER_ID', '123456789'))
    AUTO_DELETE_TIME = int(environ.get('AUTO_DELETE_TIME', '60'))

# If not using a class, ensure no stray block starters
BOT_TOKEN = environ.get('7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E')
API_ID = int(environ.get('API_ID', '17264725'))
API_HASH = environ.get('API_HASH')
DATABASE_URI = environ.get('DATABASE_URI')
DATABASE_NAME = environ.get('DATABASE_NAME', 'AutoFilterBotDB')
AUTH_CHANNEL = environ.get('AUTH_CHANNEL')
LOG_CHANNEL = environ.get('LOG_CHANNEL')
OWNER_ID = int(environ.get('OWNER_ID', '123456789'))
AUTO_DELETE_TIME = int(environ.get('AUTO_DELETE_TIME', '60'))
