from pyrogram import Client

async def check_force_sub(client: Client, user_id: int) -> bool:
    """Check if the user is subscribed to the required channel."""
    from config import AUTH_CHANNEL
    try:
        member = await client.get_chat_member(int(AUTH_CHANNEL), user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

async def check_subscription(client: Client, user_id: int, channel_id: str) -> bool:
    """Check if a user is subscribed to a channel."""
    try:
        chat_member = await client.get_chat_member(channel_id, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

async def send_subscribe_message(client: Client, message: Message, channel_id: str) -> None:
    """Send a force subscribe message with join button."""
    chat = await client.get_chat(channel_id)
    username = chat.username
    if not username:
        await message.reply_text("Please join the required channel first!")
        return
    
    join_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{username}")]
    ])
    await message.reply_text(
        "Please join our channel first to use this bot!",
        reply_markup=join_button
    )

def format_file_result(result: dict, query: str) -> str:
    """Format a database result into a readable message."""
    if "channel_id" in result and "message_id" in result:
        return f"Found file matching '{query}' in index: Message ID {result['message_id']}"
    return f"Found file matching: {query}"

async def is_admin(user_id: int) -> bool:
    """Check if a user is an admin."""
    return user_id in Config.ADMIN_IDS

def get_keywords_from_text(text: str, command: str) -> list:
    """Extract keywords from a command message."""
    parts = text.split()
    if len(parts) > 1 and parts[0] == command:
        return parts[1:]
    return []
