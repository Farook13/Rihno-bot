import logging
from pyrogram import filters
from pyrogram.types import Message
from database.filter_db import FilterDB
from config import Config
from utils.helpers import check_subscription, send_subscribe_message, format_file_result

logger = logging.getLogger('bot')

async def filter_handler(client, message: Message):
    try:
        db = FilterDB()  # Move inside to ensure fresh connection
        if Config.CHANNEL_ID:
            if not await check_subscription(client, message.from_user.id, Config.CHANNEL_ID):
                logger.warning(f"User {message.from_user.id} not subscribed to {Config.CHANNEL_ID}")
                await send_subscribe_message(client, message, Config.CHANNEL_ID)
                return

        query = message.text.strip()
        if not query:
            await message.reply_text("Please provide a search query!")
            return

        results = await db.get_file(query)
        if not results:
            logger.info(f"No results for query: {query} by user {message.from_user.id}")
            await message.reply_text("No files found!")
            return

        for result in results:
            if "channel_id" in result and "message_id" in result:
                chat = await client.get_chat(result["channel_id"])
                link = f"https://t.me/{chat.username}/{result['message_id']}" if chat.username else "Indexed file"
                await message.reply_text(f"{format_file_result(result, query)}\nLink: {link}")
                logger.debug(f"Sent link for query: {query}")
            else:
                await message.reply_document(
                    document=result["file_id"],
                    caption=format_file_result(result, query)
                )
                logger.debug(f"Sent file for query: {query}")
    except Exception as e:
        logger.error(f"Error in filter handler for query {message.text}: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while processing your request.")
