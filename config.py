import re
from os import environ
import logging

# Logging setup
logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO
)
LOGGER = logging

# Pattern for validating IDs
id_pattern = re.compile(r'^.\d+$')

# Helper function for boolean parsing
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot Information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '12618934'))
API_HASH = environ.get('API_HASH', '49aacd0bc2f8924add29fb02e20c8a16')
BOT_TOKEN = environ.get('BOT_TOKEN', '7857321740:AAHSUfjwO3w6Uffmxm9vCUMl36FtXl5-r6w')

# Bot Settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))  # Cache duration in seconds
PICS = (environ.get('PICS', 'https://envs.sh/hFY.jpg')).split()  # Start images
USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', 'False'), False)

# Admins and Channels
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5032034594').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002467149516').split()]
AUTH_CHANNEL = int(environ.get('AUTH_CHANNEL', '-1002289409354')) if environ.get('AUTH_CHANNEL') and id_pattern.search(environ.get('AUTH_CHANNEL')) else None
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002467149516'))  # Log channel
REQUEST_CHANNEL = environ.get('REQUEST_CHANNEL', 'https://t.me/subit23')  # Request channel link
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/batmanmoviehub')  # Support group link

# MongoDB Information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://saidalimuhamed88:iladias2025@cluster0.qt4dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# File Filtering Options
LANGUAGES = ["hindi", "english", "tamil", "telugu", "malayalam", "kannada"]
QUALITIES = ["360p", "480p", "720p", "1080p", "4k"]
SEASONS = [f"season {i}" for i in range(1, 11)]  # Seasons 1-10
YEARS = [str(i) for i in range(2025, 2000, -1)]  # Years from 2025 to 2000

# Bot Features
IMDB = is_enabled(environ.get('IMDB', 'True'), True)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query:</b> {query}\n\n🏷 <b>Title:</b> <a href={url}>{title}</a>\n🎭 <b>Genres:</b> {genres}\n📆 <b>Year:</b> {year}\n🌟 <b>Rating:</b> {rating}/10\n\nSupport: {SUPPORT_CHAT}")
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>{file_caption}</b>\nSize: {file_size}\nUploaded by {SUPPORT_CHAT}")
SPELL_CHECK_REPLY = is_enabled(environ.get('SPELL_CHECK_REPLY', 'True'), True)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', 'False'), False)
AUTO_DELETE = is_enabled(environ.get('AUTO_DELETE', 'True'), True)
DELETE_TIME = int(environ.get('DELETE_TIME', 600))  # Auto-delete after 10 minutes
MAX_BTN = int(environ.get('MAX_BTN', '10'))  # Max buttons in inline keyboard
REACTIONS = ["👀", "🔥", "🎉", "⚡"]

# Deployment Settings
PORT = int(environ.get('PORT', 8080))
ON_HEROKU = 'DYNO' in environ
FQDN = environ.get('FQDN', '0.0.0.0') if not ON_HEROKU else f"{environ.get('APP_NAME')}.herokuapp.com"
URL = f"https://{FQDN}/" if ON_HEROKU else f"http://localhost:{PORT}/"
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get('PING_INTERVAL', '1200'))  # 20 minutes

# Logging Info
LOG_STR = "Bot Configuration:\n"
LOG_STR += ("IMDB enabled.\n" if IMDB else "IMDB disabled.\n")
LOG_STR += (f"Custom caption: {CUSTOM_FILE_CAPTION}\n" if CUSTOM_FILE_CAPTION else "Default captions used.\n")
LOG_STR += ("Spell check enabled.\n" if SPELL_CHECK_REPLY else "Spell check disabled.\n")
LOG_STR += (f"Auto-delete after {DELETE_TIME} seconds.\n" if AUTO_DELETE else "Auto-delete disabled.\n")