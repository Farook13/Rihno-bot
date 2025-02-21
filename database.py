from pymongo import MongoClient
from config import DATABASE_URI, DATABASE_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(DATABASE_URI, serverSelectionTimeoutMS=2000)  # 2-second timeout
        self.db = self.client[DATABASE_NAME]
        self.files_collection = self.db["files"]
        # Create an index on file_name for faster searches
        self.files_collection.create_index("file_name")

    def add_file(self, file_name: str, file_link: str):
        """Add a file to the database."""
        self.files_collection.insert_one({"file_name": file_name, "file_link": file_link})

    def search_files(self, query: str):
        """Search files in the database with regex."""
        return list(self.files_collection.find(
            {"file_name": {"$regex": query, "$options": "i"}},
            {"_id": 0}  # Exclude _id field
        ).limit(10))  # Limit results for performance
