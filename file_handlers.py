import logging
import os
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from utils.db_utils import get_collection
from config import ADMIN_ID, FAIL_CHANNEL_ID
import re

logger = logging.getLogger(__name__)

def rename_file(update: Update, context: CallbackContext):
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

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    format_selected = query.data
    context.user_data['rename_format'] = format_selected
    query.edit_message_text(text=f"<b>{format_selected.capitalize()} format selected.</b> Please provide file name and metadata using /rename_process command.\nExample: /rename_process filename.mp4 '{{\"title\": \"Movie Title\", \"year\": \"2024\", \"languages\": [\"Hindi\", \"English\"]}}'", parse_mode=ParseMode.HTML)
    return 'WAITING_FOR_FILE_AND_METADATA'

def apply_rename_format(file_name, details, format_selected):
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

def process_rename(update: Update, context: CallbackContext):
    try:
        format_selected = context.user_data.get('rename_format')
        if not format_selected:
            update.message.reply_text("Please select a renaming format first using /filenamechange", parse_mode=ParseMode.HTML)
            return ConversationHandler.END

        args = context.args
        if not args or len(args) < 2:
            update.message.reply_text("Provide filename and metadata.", parse_mode=ParseMode.HTML)
            return ConversationHandler.END

        file_name = args[0]
        try:
            metadata = eval(args[1])
        except (SyntaxError, NameError, TypeError, ValueError):
            update.message.reply_text("Invalid metadata format. Please provide metadata as a valid Python dictionary string.", parse_mode=ParseMode.HTML)
            return ConversationHandler.END

        new_name = apply_rename_format(file_name, metadata, format_selected)

        log_message = f"⚙️ <b>File Renamed</b>\nOld: <code>{file_name}</code>\nNew: <code>{new_name}</code>"
        context.bot.send_message(chat_id=ADMIN_ID, text=log_message, parse_mode=ParseMode.HTML)

        update.message.reply_text(f"<b>File renamed successfully!</b> ✅\nOld Name: <code>{file_name}</code> ➡️\nNew Name: <code>{new_name}</code>", parse_mode=ParseMode.HTML)
        del context.user_data['rename_format']
        return ConversationHandler.END

    except Exception as e:
        update.message.reply_text(f"<b>Error during renaming!</b> ⚠️\n<code>{type(e).__name__}: {e}</code>", parse_mode=ParseMode.HTML)
        logger.exception("An error occurred during renaming")
        return ConversationHandler.END


def set_thumbnail(update: Update, context: CallbackContext):
    try:
        # Placeholder for thumbnail setting logic. Replace with your actual code.
        file_name = "example_file.mp4" # Replace with actual filename
        log_message = f" <b>Thumbnail Changed</b>\nFile: <code>{file_name}</code>"
        context.bot.send_message(chat_id=ADMIN_ID, text=log_message, parse_mode=ParseMode.HTML)
        update.message.reply_text("<b>Thumbnail changed successfully!</b> ✅", parse_mode=ParseMode.HTML)

    except Exception as e:
        update.message.reply_text(f"<b>Error changing thumbnail!</b> ⚠️\n<code>{type(e).__name__}: {e}</code>", parse_mode=ParseMode.HTML)
        logger.exception("An error occurred during thumbnail change")

def set_source(update: Update, context: CallbackContext):
    try:
        args = context.args
        if not args:
            update.message.reply_text("Please provide source path.", parse_mode=ParseMode.HTML)
            return
        source_path = args[0]
        context.user_data['source_path'] = source_path
        update.message.reply_text(f"<b>Source path set to:</b> <code>{source_path}</code>", parse_mode=ParseMode.HTML)

    except Exception as e:
        update.message.reply_text(f"<b>Error setting source path!</b> ⚠️\n<code>{type(e).__name__}: {e}</code>", parse_mode=ParseMode.HTML)
        logger.exception("An error occurred while setting source path")

def set_target(update: Update, context: CallbackContext):
    try:
        args = context.args
        if not args:
            update.message.reply_text("Please provide target path.", parse_mode=ParseMode.HTML)
            return
        target_path = args[0]
        context.user_data['target_path'] = target_path
        update.message.reply_text(f"<b>Target path set to:</b> <code>{target_path}</code>", parse_mode=ParseMode.HTML)
    except Exception as e:
        update.message.reply_text(f"<b>Error setting target path!</b> ⚠️\n<code>{type(e).__name__}: {e}</code>", parse_mode=ParseMode.HTML)
        logger.exception("An error occurred while setting target path")



def work(update: Update, context: CallbackContext):
    try:
        source_path = context.user_data.get('source_path')
        target_path = context.user_data.get('target_path')

        if not source_path or not target_path:
            update.message.reply_text("Please set source and target paths first using /setsource and /settarget.", parse_mode=ParseMode.HTML)
            return

        args = context.args
        if args:
            try:
                start, end = map(int, args[0].split('-'))
                update.message.reply_text(f"Processing messages from {start} to {end}", parse_mode=ParseMode.HTML)
                # This part needs actual implementation using Telegram API to get messages
                # and process them using source and target paths
                #Example
                #for message_id in range(start, end+1):
                #   #get message by id from channel
                #   #download file from message
                #   #rename file
                #   #send renamed file to target channel
                #   #log activity
            except ValueError:
                update.message.reply_text("Invalid range format. Use /work start-end (e.g., /work 10-20)", parse_mode=ParseMode.HTML)
