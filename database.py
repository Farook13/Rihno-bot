from pymongo import MongoClient
from config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.DATABASE_URI, serverSelectionTimeoutMS=2000)
        self.db = self.client[Config.DATABASE_NAME]
        self.files_collection = self.db["files"]
        self.files_collection.create_index("file_name")

    def add_file(self, file_name: str, file_link: str):
        """Add a file to the database."""
        self.files_collection.insert_one({"file_name": file_name, "file_link": file_link})

    def search_files(self, query: str):
        """Search files in the database with regex."""
        return list(self.files_collection.find(
            {"file_name": {"$regex": query, "$options": "i"}},
            {"_id": 0}
        ).limit(10))
