import logging
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from pyrogram.errors import ChatForbidden, BadRequest

logger = logging.getLogger('bot')

async def check_subscription(client: Client, user_id: int, channel_id: int) -> bool:
    try:
        chat_member = await client.get_chat_member(channel_id, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except (ChatForbidden, BadRequest) as e:
        logger.warning(f"Subscription check failed for {user_id} in {channel_id}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error checking subscription: {str(e)}", exc_info=True)
        return False

async def send_subscribe_message(client: Client, message: Message, channel_id: int) -> None:
    try:
        chat = await client.get_chat(channel_id)
        username = chat.username or str(channel_id)
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{username}")]
        ])
        await message.reply_text(
            "Join our channel to use this bot!",
            reply_markup=join_button
        )
    except Exception as e:
        logger.error(f"Error sending subscribe message: {str(e)}", exc_info=True)
        await message.reply_text("Please join the channel manually!")
