from pyrogram.errors import UserNotParticipant
from config import Config

async def check_force_sub(client, user_id):
    try:
        await client.get_chat_member(Config.FORCE_SUB_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Force sub check failed: {e}")
        return False