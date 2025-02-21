import logging
from pyrogram import filters
from pyrogram.types import Message
#rom database.filter_db import FilterDB
from config import Config
from utils.helpers import check_subscription, send_subscribe_message

logger = logging.getLogger('bot')

async def filter_handler(client, message: Message):
    try:
        db = FilterDB()
        if Config.AUTH_CHANNEL:
            if not await check_subscription(client, message.from_user.id, Config.AUTH_CHANNEL):
                logger.warning(f"User {message.from_user.id} not subscribed")
                await send_subscribe_message(client, message, Config.AUTH_CHANNEL)
                return

        query = message.text.strip()
        if not query:
            await message.reply_text("Please provide a movie name!")
            return

        results = await db.get_file(query)
        if not results:
            await message.reply_text(f"No movies found for '{query}'!")
            logger.info(f"No results for '{query}' by {message.from_user.id}")
            return

        response = f"Found {len(results)} movie(s) for '{query}':\n\n"
        for result in results:
            movie_name = result.get("movie_name", "Unknown Movie")
            response += f"🎬 {movie_name}\n"
            await message.reply_document(
                document=result["file_id"],
                caption=f"Movie: {movie_name}"
            )
        logger.info(f"Sent {len(results)} movies for '{query}' to {message.from_user.id}")
        if Config.LOG_CHANNEL:
            await client.send_message(Config.LOG_CHANNEL, f"User {message.from_user.id} searched '{query}' - {len(results)} results")
    except Exception as e:
        logger.error(f"Error in filter for '{message.text}': {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while searching for movies.")
