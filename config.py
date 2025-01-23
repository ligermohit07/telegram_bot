import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
FAIL_CHANNEL_ID = int(os.getenv("FAIL_CHANNEL_ID"))

if not BOT_TOKEN:
    print("Error: BOT_TOKEN environment variable not set.")
    exit()
if not API_ID:
    print("Error: API_ID environment variable not set.")
    exit()
if not API_HASH:
    print("Error: API_HASH environment variable not set.")
    exit()
if not MONGO_DB_URL:
    print("Error: MONGO_DB_URL environment variable not set.")
    exit()
if not ADMIN_ID:
    print("Error: ADMIN_ID environment variable not set.")
    exit()
if not FAIL_CHANNEL_ID:
    print("Error: FAIL_CHANNEL_ID environment variable not set.")
    exit()
