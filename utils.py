from pyrogram import Client

async def check_force_sub(client: Client, user_id: int) -> bool:
    """Check if the user is subscribed to the required channel."""
    from config import AUTH_CHANNEL
    try:
        member = await client.get_chat_member(int(AUTH_CHANNEL), user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False
