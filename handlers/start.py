import logging
from pyrogram import filters
from pyrogram.types import Message
from config import Config

logger = logging.getLogger('bot')

async def start_command(client, message: Message):
    try:
        welcome_text = (
            "Welcome to the Movie AutoFilter Bot!\n"
            "Search for movies by typing their names.\n"
            "Example: 'Avatar' or 'The Dark Knight'"
        )
        await message.reply_text(welcome_text)
        logger.info(f"Start command by {message.from_user.id}")
        if Config.LOG_CHANNEL:
            await client.send_message(Config.LOG_CHANNEL, f"User {message.from_user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred. Try again later.")
