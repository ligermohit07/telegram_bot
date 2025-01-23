from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils.db_utils import get_collection
from config import ADMIN_ID
import logging

logger = logging.getLogger(__name__)

channels_collection = get_collection("channels")

def set_log_channel(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    channels_collection.update_one({"type": "log"}, {"$set": {"chat_id": chat_id}}, upsert=True)
    update.message.reply_text("<b>✅ Log channel has been set successfully!</b>", parse_mode=ParseMode.HTML)
    try:
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Log channel set to: {chat_id}", parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error sending log message: {e}")

def set_fail_channel(update: Update, context: CallbackContext):
    # Similar logic as set_log_channel, but for fail channel
    chat_id = update.message.chat_id
    channels_collection.update_one({"type": "fail"}, {"$set": {"chat_id": chat_id}}, upsert=True)
    update.message.reply_text("<b>✅ Fail channel has been set successfully!</b>", parse_mode=ParseMode.HTML)
    try:
        context.bot.send_message(chat_id=ADMIN_ID, text=f"Fail channel set to: {chat_id}", parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Error sending log message: {e}")
