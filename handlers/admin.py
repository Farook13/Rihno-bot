import logging
from pyrogram import filters
from pyrogram.types import Message

from utils.helpers import is_admin, get_keywords_from_text

logger = logging.getLogger('bot')

async def add_file(client, message: Message):
    try:
        if not await is_admin(message.from_user.id):
            logger.warning(f"Unauthorized add attempt by {message.from_user.id}")
            await message.reply_text("You are not authorized!")
            return

        if not message.reply_to_message or not message.reply_to_message.document:
            logger.info(f"Invalid add command from {message.from_user.id}")
            await message.reply_text("Please reply to a document with keywords!\nExample: /add keyword1 keyword2")
            return

        keywords = get_keywords_from_text(message.text, "/add")
        if not keywords:
            logger.info(f"No keywords from {message.from_user.id}")
            await message.reply_text("Please provide keywords!")
            return

        db = FilterDB()
        file_id = message.reply_to_message.document.file_id
        channel_id = None
        message_id = None

        if Config.INDEX_CHANNEL:
            forwarded = await message.reply_to_message.forward(Config.INDEX_CHANNEL)
            channel_id = int(Config.INDEX_CHANNEL)
            message_id = forwarded.id
            logger.debug(f"Forwarded to index channel: {message_id}")

        await db.add_filter(file_id, " ".join(keywords), channel_id, message_id)
        logger.info(f"File added by {message.from_user.id}: {file_id} with keywords: {' '.join(keywords)}")
        await message.reply_text(f"File added successfully with keywords: {' '.join(keywords)}")
    except Exception as e:
        logger.error(f"Error in add_file: {str(e)}", exc_info=True)
        await message.reply_text("Failed to add file. Please try again.")

async def delete_file(client, message: Message):
    try:
        if not await is_admin(message.from_user.id):
            logger.warning(f"Unauthorized delete attempt by {message.from_user.id}")
            await message.reply_text("You are not authorized!")
            return

        if not message.reply_to_message or not message.reply_to_message.document:
            logger.info(f"Invalid delete command from {message.from_user.id}")
            await message.reply_text("Please reply to a document to delete it!")
            return

        db = FilterDB()
        file_id = message.reply_to_message.document.file_id
        result = await db.delete_filter(file_id)

        if result.deleted_count > 0:
            logger.info(f"File deleted by {message.from_user.id}: {file_id}")
            await message.reply_text("File deleted successfully!")
        else:
            logger.info(f"File not found for deletion by {message.from_user.id}: {file_id}")
            await message.reply_text("File not found in database!")
    except Exception as e:
        logger.error(f"Error in delete_file: {str(e)}", exc_info=True)
        await message.reply_text("Failed to delete file. Please try again.")
