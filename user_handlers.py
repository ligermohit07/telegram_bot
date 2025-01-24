from typing import Optional, Dict, Any
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils.db_utils import get_collection

users_collection = get_collection("users")


def add_user(update: Update, context: CallbackContext) -> None:
    """Adds a new user to the database."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username
    user_data: Dict[str, Any] = {"chat_id": chat_id, "username": username, "limit": None}
    users_collection.insert_one(user_data)
    update.message.reply_text(f"✅ User has been added! Chat ID: {chat_id}", parse_mode=ParseMode.HTML)


def user_list(update: Update, context: CallbackContext) -> None:
    """Provides a list of all users in the database."""
    users = users_collection.find()
    msg = "**User List:**\n"
    for user in users:
        chat_id = user["chat_id"]
        username = user.get("username", "NA")
        limit = user.get("limit", "NA")
        msg += f"- Chat ID: `{chat_id}`\n  Username: @{username}\n  Limit: {limit}\n"
    update.message.reply_text(msg, parse_mode=ParseMode.HTML)


def remove_user(update: Update, context: CallbackContext) -> None:
    """Removes a user from the database."""
    chat_id = update.effective_chat.id
    users_collection.delete_one({"chat_id": chat_id})
    update.message.reply_text("✅ User has been removed!", parse_mode=ParseMode.HTML)


def set_limit(update: Update, context: CallbackContext) -> None:
    """Sets a download limit for the user."""
    chat_id = update.effective_chat.id
    args = context.args
    if not args or len(args) != 1:
        update.message.reply_text("Invalid usage. Provide a limit value.", parse_mode=ParseMode.HTML)
        return
    try:
        limit = int(args[0])
        users_collection.update_one({"chat_id": chat_id}, {"$set": {"limit": limit}})
        update.message.reply_text(f"✅ User limit has been set to {limit}!", parse_mode=ParseMode.HTML)
    except ValueError:
        update.message.reply_text("Invalid limit value. Please provide an integer.", parse_mode=ParseMode.HTML)
