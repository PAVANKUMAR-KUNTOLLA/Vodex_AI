from fastapi import FastAPI

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from decouple import config
from urllib.parse import quote_plus

# Load credentials and MongoDB URL from environment variables
username = config("USERNAME")
password = config("PASSWORD")

# URL-encode the username and password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Read the MongoDB connection URL from the environment variable
MONGO_DB_URL = config("MONGO_DB_URL")

# Construct the MongoDB URL using the encoded credentials and app name
url = MONGO_DB_URL.format(
    USERNAME=encoded_username,
    PASSWORD=encoded_password
)

# Create an AsyncIOMotorClient using the constructed URL
client = AsyncIOMotorClient(url)

# Select the database
db = client["vodex_ai"]

async def ensure_collection(db, collection_name):
    # List existing collections
    existing_collections = await db.list_collection_names()
    
    # Check if collection exists, if not, create it
    if collection_name not in existing_collections:
        await db[collection_name].insert_one({"created": True})
        await db[collection_name].delete_one({"created": True})

async def ensure_index(collection, index_name, keys):
    existing_indexes = await collection.index_information()
    if index_name not in existing_indexes:
        await collection.create_index(keys, name=index_name)

async def init_db(app: FastAPI):
    await ensure_collection(db, "items")
    items_collection = db["items"]

    await ensure_collection(db, "clock_in_records")
    clock_in_collection = db["clock_in_records"]

    await ensure_index(items_collection, "email_index", [("email", ASCENDING)])
    await ensure_index(clock_in_collection, "email_index", [("email", ASCENDING)])

    # Return collections
    return items_collection, clock_in_collection
