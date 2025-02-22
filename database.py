import motor.motor_asyncio
from config import MONGO_URI, DB_NAME

class Database:
    def __init__(self):
        # Initialize async MongoDB client with MONGO_URI from config
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.files = self.db['files']  # Collection for file storage
        self.users = self.db['users']  # Collection for user credits

    async def search_files(self, query):
        # Search files by name with case-insensitive regex
        cursor = self.files.find({"file_name": {"$regex": query, "$options": "i"}}).limit(10)
        return [doc async for doc in cursor]

    async def add_file(self, file_name, file_link):
        # Add a file to the files collection
        await self.files.insert_one({"file_name": file_name, "file_link": file_link})

    async def ensure_user(self, user_id):
        # Ensure user exists in the database with initial credits
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            await self.users.insert_one({"user_id": user_id, "credits": 10})  # Default credits = 10

    async def get_user_credits(self, user_id):
        # Get user's current credits
        user = await self.users.find_one({"user_id": user_id})
        return user["credits"] if user else 0

    async def update_user_credits(self, user_id, amount):
        # Update user's credits (positive or negative amount)
        await self.users.update_one(
            {"user_id": user_id}, 
            {"$inc": {"credits": amount}}, 
            upsert=True
        )

    async def close(self):
        # Close the MongoDB client connection
        self.client.close()