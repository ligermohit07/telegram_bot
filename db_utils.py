import pymongo
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_collection(collection_name: str) -> Optional[pymongo.collection.Collection]:
    """
    MongoDB database से एक collection प्राप्त करता है।

    Args:
        collection_name: Collection का नाम।

    Returns:
       pymongo.collection.Collection or None: यदि connection सफल है तो Collection object, अन्यथा None.
    """
    try:
        mongo_uri = os.getenv("MONGO_DB_URL")
        db_name = os.getenv("DATABASE_NAME")
        if not mongo_uri:
            logger.error("MONGO_DB_URL environment variable is not set.")
            return None
        if not db_name:
            logger.error("DATABASE_NAME environment variable is not set.")
            return None
        client = pymongo.MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        # Test the connection
        client.admin.command('ping')
        logger.info(f"Successfully connected to database {db_name} and collection {collection_name}")
        return collection
    except pymongo.errors.ConnectionFailure as e:
        logger.error(f"Database connection error: {e}")
        return None
    except pymongo.errors.ServerSelectionTimeoutError as e:
        logger.error(f"Database connection timeout error: {e}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred while getting collection: {e}")
        return None

# Example usage (in a different file):
# from utils.db_utils import get_collection
#
# users_collection = get_collection("users")
# if users_collection:
#     # Use the collection object for database operations (insert, find, etc.)
# else:
#     print("Failed to get the collection.")
