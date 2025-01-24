import logging
from typing import List, Dict, Any, Optional
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils.db_utils import get_collection
from config import ADMIN_ID

logger = logging.getLogger(__name__)

def add_api(update: Update, context: CallbackContext) -> None:
    """नए API को database में जोड़ता है।

    Args:
        update: Telegram update object.
        context: CallbackContext object.
    """
    try:
        args: List[str] = context.args
        if not args or len(args) != 2:
            update.message.reply_text("कृपया API नाम और key प्रदान करें।", parse_mode=ParseMode.HTML)
            logger.warning("addapi command के लिए अमान्य arguments.")
            return

        api_name: str = args[0]
        api_key: str = args[1]

        api_collection = get_collection("apis")
        if api_collection is None:
            update.message.reply_text("Database से connect करने में error.", parse_mode=ParseMode.HTML)
            logger.error("Database connection failed in add_api")
            return

        existing_api: Optional[Dict[str, Any]] = api_collection.find_one({"name": api_name})
        if existing_api:
            update.message.reply_text("इस नाम का API पहले से मौजूद है।", parse_mode=ParseMode.HTML)
            logger.warning(f"API with name {api_name} already exists.")
            return

        api_collection.insert_one({"name": api_name, "key": api_key})
        update.message.reply_text("API सफलतापूर्वक जोड़ दिया गया।", parse_mode=ParseMode.HTML)
        logger.info(f"API key added: {api_name}")

        try:
            context.bot.send_message(chat_id=ADMIN_ID, text=f"New API added: {api_name}", parse_mode=ParseMode.HTML)
            logger.info(f"Notification sent to admin about new API: {api_name}")
        except Exception as admin_notification_error:
            logger.error(f"Failed to notify admin: {admin_notification_error}")

    except Exception as e:
        update.message.reply_text(f"एक error हुई: <code>{type(e).__name__}: {e}</code>", parse_mode=ParseMode.HTML)
        logger.exception(f"API key जोड़ते समय error: {e}")

def api_list(update: Update, context: CallbackContext) -> None:
    """Database में store सभी APIs की list दिखाता है।

    Args:
        update: Telegram update object.
        context: CallbackContext object.
    """
    try:
        api_collection = get_collection("apis")
        if api_collection is None:
            update.message.reply_text("Database से connect करने में error.", parse_mode=ParseMode.HTML)
            logger.error("Database connection failed in api_list")
            return

        apis: List[Dict[str, Any]] = list(api_collection.find())
        if apis:
            message = "<b>Stored APIs:</b>\n"
            for api in apis:
                message += f"<code>Name: {api['name']}, Key: {api['key']}</code>\n"
            update.message.reply_text(message, parse_mode=ParseMode.HTML)
            logger.info("Displayed API list.")
        else:
            update.message.reply_text("कोई API store नहीं है।", parse_mode=ParseMode.HTML)
            logger.info("No APIs found in database.")

    except Exception as e:
        update.message.reply_text(f"एक error हुई: <code>{type(e).__name__}: {e}</code>", parse_mode=ParseMode.HTML)
        logger.exception(f"API list दिखाते समय error: {e}")

def remove_api(update: Update, context: CallbackContext) -> None:
    """Database से एक API को remove करता है।

    Args:
        update: Telegram update object.
        context: CallbackContext object.
    """
    try:
        args: List[str] = context.args
        if not args:
            update.message.reply_text("कृपया remove करने के लिए API नाम प्रदान करें।", parse_mode=ParseMode.HTML)
            logger.warning(f"No API name provided for removal.")
            return

        api_name: str = args[0]

        api_collection = get_collection("apis")
        if api_collection is None:
            update.message.reply_text("Database se connect karne me error.", parse_mode=ParseMode.HTML)
            logger.error("Database connection failed in remove_api")
            return

        result = api_collection.delete_one({"name": api_name})
        if result.deleted_count > 0:
            update.message.reply_text(f"API {api_name} सफलतापूर्वक हटा दिया गया।", parse_mode=ParseMode.HTML)
            logger.info(f"API key removed: {api_name}")
            try:
                context.bot.send_message(chat_id=ADMIN_ID, text=f"API removed: {api_name}", parse_mode=ParseMode.HTML)
                logger.info(f"Notification sent to admin about removed API: {api_name}")
            except Exception as admin_notification_error:
                logger.error(f"Failed to notify admin: {admin_notification_error}")
        else:
            update.message.reply_text(f"API {api_name} नहीं मिला।", parse_mode=ParseMode.HTML)
            logger.warning(f"API {api_name} not found for removal.")

    except Exception as e:
        update.message.reply_text(f"एक error हुई: <code>{type(e).__name__}: {e}</code>", parse_mode=ParseMode.HTML)
        logger.exception(f"API key remove करते समय error: {e}")
