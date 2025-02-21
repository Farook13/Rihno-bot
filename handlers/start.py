import logging
from pyrogram import filters
from pyrogram.types import Message

logger = logging.getLogger('bot')

async def start_command(client, message: Message):
    try:
        welcome_text = (
            "Welcome to the AutoFilter Bot!\n"
            "I can help you find files quickly.\n\n"
            "Just send me a keyword to search!\n"
            f"Bot Status: {'Running' if client.is_connected else 'Not Connected'}"
        )
        await message.reply_text(welcome_text)
        logger.info(f"Start command executed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred. Please try again later.")
