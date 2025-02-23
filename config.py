import re
from os import environ
import logging

# Logging setup
logging.basicConfig(
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
 level=logging.INFO
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
 if value.lower() in ["true", "yes", "1", "enable", "y"]:
     return True
 elif value.lower() in ["false", "no", "0", "disable", "n"]:
     return False
 else:
     return default

# Bot Information
API_ID = int(environ.get('API_ID', '12618934'))
API_HASH = environ.get('API_HASH', '49aacd0bc2f8924add29fb02e20c8a16')
BOT_TOKEN = environ.get('BOT_TOKEN', '7857321740:AAHSUfjwO3w6Uffmxm9vCUMl36FtXl5-r6w')

# Bot Settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
PICS = (environ.get('PICS', 'https://envs.sh/hFY.jpg')).split()

# Admins and Channels
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5032034594').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002467149516').split()]
AUTH_CHANNEL = int(environ.get('AUTH_CHANNEL', '-1002289409354')) if environ.get('AUTH_CHANNEL') and id_pattern.search(environ.get('AUTH_CHANNEL')) else None
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002467149516'))
REQUEST_CHANNEL = environ.get('REQUEST_CHANNEL', 'https://t.me/subit23')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/batmanmoviehub')
# config.py
FORCE_SUB_CHANNELS = ["@YourChannel1", "@YourChannel2"]  # Your channel usernames
OMDB_API_KEY = "your_omdb_api_key_here"  # From

DATABASE_URI = environ.get ('DATABASE_URI', "mongodb+srv://saidalimuhamed88:iladias2025@cluster0.qt4dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# File Filtering Options
LANGUAGES = ["hindi", "english", "tamil", "telugu", "malayalam", "kannada"]
QUALITIES = ["360p", "480p", "720p", "1080p", "4k"]
SEASONS = [f"season {i}" for i in range(1, 11)]
YEARS = [str(i) for i in range(2025, 2000, -1)]

# Bot Features
IMDB = is_enabled(environ.get('IMDB', 'True'), True)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query:</b> {query}\n\n🏷 <b>Title:</b> <a href={url}>{title}</a>\n🎭 <b>Genres:</b> {genres}\n📆 <b>Year:</b> {year}\n🌟 <b>Rating:</b> {rating}/10\n\nSupport: {SUPPORT_CHAT}")
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>{file_caption}</b>\nSize: {file_size}\nUploaded by {SUPPORT_CHAT}")
AUTO_DELETE = is_enabled(environ.get('AUTO_DELETE', 'True'), True)
DELETE_TIME = int(environ.get('DELETE_TIME', 600))

# Deployment Settings
PORT=8000
PORT = int(environ.get('PORT', 8000))
ON_HEROKU = 'DYNO' in environ
FQDN = environ.get('FQDN', '0.0.0.0') if not ON_HEROKU else f"{environ.get('APP_NAME')}.herokuapp.com"
URL = f"https://{FQDN}/" if ON_HEROKU else f"http://localhost:{PORT}/"

LOG_STR = "Bot Configuration:\n"
LOG_STR += ("IMDB enabled.\n" if IMDB else "IMDB disabled.\n")
LOG_STR += (f"Custom caption: {CUSTOM_FILE_CAPTION}\n" if CUSTOM_FILE_CAPTION else "Default captions used.\n")
LOG_STR += (f"Auto-delete after {DELETE_TIME} seconds.\n" if AUTO_DELETE else "Auto-delete disabled.\n")