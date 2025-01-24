import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

BOT_TOKEN: Optional[str] = os.getenv("BOT_TOKEN")
"""Telegram bot का token."""

API_ID: Optional[str] = os.getenv("API_ID")
"""Telegram API ID."""

API_HASH: Optional[str] = os.getenv("API_HASH")
"""Telegram API hash."""

MONGO_DB_URL: Optional[str] = os.getenv("MONGO_DB_URL")
"""MongoDB connection URL."""

DATABASE_NAME: Optional[str] = os.getenv("DATABASE_NAME")
"""MongoDB Database Name."""

ADMIN_ID: Optional[int] = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None
"""Admin user का Telegram ID."""

FAIL_CHANNEL_ID: Optional[int] = int(os.getenv("FAIL_CHANNEL_ID")) if os.getenv("FAIL_CHANNEL_ID") else None
"""Errors और exceptions के लिए Fail channel का ID."""

if not all([BOT_TOKEN, API_ID, API_HASH, MONGO_DB_URL, ADMIN_ID, FAIL_CHANNEL_ID, DATABASE_NAME]):
    raise ValueError("Missing required environment variables. Please set BOT_TOKEN, API_ID, API_HASH, MONGO_DB_URL, ADMIN_ID, FAIL_CHANNEL_ID and DATABASE_NAME in .env file.")
