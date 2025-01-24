import logging
from typing import Optional
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils.db_utils import get_collection
from config import ADMIN_ID


logger = logging.getLogger(__name__)

# Use a dictionary to store channel information (type and chat ID)
channels: dict[str, Optional[int]] = {
    "log": None,
    "fail": None,
}


def update_channel(update: Update, context: CallbackContext, channel_type: str) -> None:
    """
    Updates the specified channel (log or fail) in the database and sends a notification to the admin.

    Args:
        update: Telegram update object.
        context: CallbackContext object.
        channel_type: The type of channel to update ("log" or "fail").
    """

    chat_id = update.message.chat_id
    if channels[channel_type] is not None:
        # Update the existing channel document
        get_collection("channels").update_one(
            {"type": channel_type}, {"$set": {"chat_id": chat_id}}
        )
        update.message.reply_text(
            f"<b>✅ {channel_type.capitalize()} channel updated successfully!</b>",
            parse_mode=ParseMode.HTML,
        )
    else:
        # Insert a new document for the channel
        get_collection("channels").insert_one({"type": channel_type, "chat_id": chat_id})
        update.message.reply_text(
            f"<b>✅ New {channel_type} channel set successfully!</b>",
            parse_mode=ParseMode.HTML,
        )
    channels[channel_type] = chat_id

    try:
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"{channel_type.capitalize()} channel set to: {chat_id}",
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logger.error(f"Error sending notification about {channel_type} channel: {e}")


def set_log_channel(update: Update, context: CallbackContext) -> None:
    """Sets the log channel."""
    update_channel(update, context, channel_type="log")


def set_fail_channel(update: Update, context: CallbackContext) -> None:
    """Sets the fail channel."""
    update_channel(update, context, channel_type="fail")
