import logging
from pyrogram import filters
from pyrogram.types import CallbackQuery
from config import Config
from utils.helpers import check_subscription, send_subscribe_message

logger = logging.getLogger('bot')

async def callback_handler(client, callback_query: CallbackQuery):
    try:
        if callback_query.data == "check_sub":
            user_id = callback_query.from_user.id
            if await check_subscription(client, user_id, Config.CHANNEL_ID):
                await callback_query.answer("You're subscribed! Enjoy the bot.", show_alert=True)
            else:
                await send_subscribe_message(client, callback_query.message, Config.CHANNEL_ID)
                await callback_query.answer("Please join the channel first!", show_alert=True)
            logger.info(f"Callback processed for user {user_id}")
    except Exception as e:
        logger.error(f"Error in callback: {str(e)}", exc_info=True)
        await callback_query.answer("An error occurred.", show_alert=True)
