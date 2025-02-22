import pymongo
import asyncio
from config import Config

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        self.files = self.db[Config.FILE_COLLECTION]
        self.users = self.db[Config.USER_COLLECTION]

    async def search_files(self, query):
        loop = asyncio.get_running_loop()
        results = await loop.run_in_executor(None, self._search_files_sync, query)
        return results

    def _search_files_sync(self, query):
        return list(self.files.find({"file_name": {"$regex": query, "$options": "i"}}).limit(10))

    async def add_file(self, file_name, file_link):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.files.insert_one, {"file_name": file_name, "file_link": file_link})

    async def ensure_user(self, user_id):
        loop = asyncio.get_running_loop()
        user = await loop.run_in_executor(None, self.users.find_one, {"user_id": user_id})
        if not user:
            await loop.run_in_executor(None, self.users.insert_one, {"user_id": user_id, "credits": Config.INITIAL_CREDITS})

    async def get_user_credits(self, user_id):
        loop = asyncio.get_running_loop()
        user = await loop.run_in_executor(None, self.users.find_one, {"user_id": user_id})
        return user["credits"] if user else 0

    async def update_user_credits(self, user_id, amount):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, self.users.update_one, {"user_id": user_id}, {"$inc": {"credits": amount}}, upsert=True
        )

    async def close(self):
        self.client.close()