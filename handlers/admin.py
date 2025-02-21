import logging
from pyrogram import filters
from pyrogram.types import Message
#from database.filter_db import FilterDB
from config import Config

logger = logging.getLogger('bot')

async def add_file(client, message: Message):
    try:
        if not message.reply_to_message or not message.reply_to_message.document:
            await message.reply_text("Reply to a movie file with: /add MovieName keyword1 keyword2")
            return

        parts = message.text.strip().split(maxsplit=2)
        if len(parts) < 2:
            await message.reply_text("Please provide at least the movie name!\nExample: /add Avatar sci-fi action")
            return
        
        movie_name = parts[1]
        keywords = parts[2] if len(parts) > 2 else movie_name

        db = FilterDB()
        file_id = message.reply_to_message.document.file_id
        await db.add_filter(file_id, movie_name, keywords)
        await message.reply_text(f"Movie '{movie_name}' added successfully!")
        logger.info(f"Movie '{movie_name}' added by {message.from_user.id}")
        if Config.LOG_CHANNEL:
            await client.send_message(Config.LOG_CHANNEL, f"Admin {message.from_user.id} added '{movie_name}'")
    except Exception as e:
        logger.error(f"Error adding movie: {str(e)}", exc_info=True)
        await message.reply_text("Failed to add movie.")

async def delete_file(client, message: Message):
    try:
        if not message.reply_to_message or not message.reply_to_message.document:
            await message.reply_text("Reply to a movie file with /delete to remove it!")
            return

        db = FilterDB()
        file_id = message.reply_to_message.document.file_id
        result = await db.delete_filter(file_id)
        
        if result.deleted_count > 0:
            await message.reply_text("Movie deleted successfully!")
            logger.info(f"Movie deleted by {message.from_user.id}: {file_id}")
            if Config.LOG_CHANNEL:
                await client.send_message(Config.LOG_CHANNEL, f"Admin {message.from_user.id} deleted movie {file_id}")
        else:
            await message.reply_text("Movie not found in database!")
    except Exception as e:
        logger.error(f"Error deleting movie: {str(e)}", exc_info=True)
        await message.reply_text("Failed to delete movie.")
