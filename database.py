import pymongo
from config import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME, LOGGER

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(DATABASE_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]
        LOGGER.info("Connected to MongoDB.")

    def insert_file(self, file_data):
        """Insert a file into MongoDB if it doesn't already exist."""
        existing = self.collection.find_one({"file_id": file_data["file_id"]})
        if not existing:
            self.collection.insert_one(file_data)
            return True
        return False

    def search_files(self, query):
        """Search files by name or caption, case-insensitive, limited to 10 results."""
        return self.collection.find({
            "$or": [
                {"file_name": {"$regex": query, "$options": "i"}},
                {"caption": {"$regex": query, "$options": "i"}}
            ]
        }).limit(10)

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()
        LOGGER.info("MongoDB connection closed.")