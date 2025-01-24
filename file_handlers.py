import logging
import os
from typing import Optional, Dict, Any
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from utils.db_utils import get_collection
import re

# Import necessary constants from config.py
from config import ADMIN_ID, FAIL_CHANNEL_ID

logger = logging.getLogger(__name__)


def rename_file(update: Update, context: CallbackContext) -> str:
    """Prompts the user to select a renaming format."""
    keyboard = [[
        InlineKeyboardButton("Movie ", callback_data='movie'),
        InlineKeyboardButton("TV Show ", callback_data='tv_show')
    ],
    [
        InlineKeyboardButton("Music ", callback_data='music'),
        InlineKeyboardButton("Custom ✍️", callback_data='custom')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("<b>Choose a renaming format:</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return 'WAITING_FOR_FORMAT_SELECTION'


def button(update: Update, context: CallbackContext) -> str:
    """Handles the user's format selection."""
    try:
        query = update.callback_query
        query.answer()
        format_selected: str = query.data
        context.user_data['rename_format'] = format_selected
        query.edit_message_text(text=f"<b>{format_selected.capitalize()} format selected.</b> Please provide file name and metadata using /rename_process command.\nExample: /rename_process filename.mp4 '{{\"title\": \"Movie Title\", \"year\": \"2024\", \"languages\": [\"Hindi\", \"English\"]}}'", parse_mode=ParseMode.HTML)
        return 'WAITING_FOR_FILE_AND_METADATA'
    except Exception as e:
        logger.exception("Error in button handler: %s", e)
        if update.callback_query:
            update.callback_query.edit_message_text(f"An error occurred: <code>{e}</code>", parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(f"An error occurred: <code>{e}</code>", parse_mode=ParseMode.HTML)
        return ConversationHandler.END


def apply_rename_format(file_name: str, details: Dict[str, Any], format_selected: str) -> str:
    """Applies the selected renaming format to the filename."""
    try:
        title = details.get("title", "Unknown Title")
        season = details.get("season", "S01")
        episode = details.get("episode", "E01")
        year = details.get("year", "2025")
        languages = ", ".join(details.get("languages", ["Unknown"]))
        quality = details.get("quality", "HD")

        if format_selected == 'movie':
            new_name = f" {title} ({year}) [{languages}] {quality} ➢Channel ☞ @iCrunchKornBots.mp4"
        elif format_selected == 'tv_show':
            new_name = f" {title} S{season}E{episode} ({year}) [{languages}] {quality} ➢Channel ☞ @iCrunchKornBots.mp4"
        elif format_selected == 'music':
            new_name = f" {title} - {year}.mp3"
        else:
            new_name = file_name  # Default if custom or invalid format
        return new_name
    except Exception as e:
        return f"Error in renaming: {str(e)}"


def process_rename(update: Update, context: CallbackContext) -> str:
    """Processes the file renaming based on user input."""
    try:
        format_selected: Optional[str] = context.user_data.get('rename_format')
        if not format_selected:
            update.message.reply_text("Please select a renaming format first using /filenamechange", parse_mode=ParseMode.HTML)
            return ConversationHandler.END

        args: List[str] = context.args
        if not args or len(args) < 2:
            update.message.reply_text("Provide filename and metadata.", parse_mode=ParseMode.HTML
