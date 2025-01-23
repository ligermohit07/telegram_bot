import pymongo

def get_collection(collection_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Assuming a local MongoDB instance
    db = client["telegram_bot"]  # Database name
    collection = db[collection_name]  # Collection name
    return collection

# Example usage (assuming the code is in a different file)
# from utils.db_utils import get_collection
#
# users_collection = get_collection("users")
# # Use the collection object for database operations (insert, find, etc.)
