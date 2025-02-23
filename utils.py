from pyrogram import Client
from config import Config

async def check_force_sub(client: Client, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(int(Config.AUTH_CHANNEL), user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False