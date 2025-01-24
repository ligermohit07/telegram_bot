import logging
import os
from telegram import Update, ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
from config import BOT_TOKEN, ADMIN_ID, FAIL_CHANNEL_ID
from handlers import (
    general_handlers,
    channel_handlers,
    file_handlers,
    user_handlers,
    api_handlers,
)

# Logging configuration
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def error_handler(update: Update, context: CallbackContext):
    """Errors को log करता है और admin को notification send करता है."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.effective_message:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="An error occurred while processing your request. The error has been logged.",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error sending error message to user: {e}")
    try:
        await context.bot.send_message(
            chat_id=FAIL_CHANNEL_ID,
            text=f"An error occurred:\n<code>{context.error}</code>",
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logger.error(f"Error sending error message to fail channel: {e}")


def main():
    try:
        application = ApplicationBuilder().token(BOT_TOKEN).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('filenamechange', file_handlers.rename_file)],
            states={
                'WAITING_FOR_FORMAT_SELECTION': [CallbackQueryHandler(file_handlers.button)],
                'WAITING_FOR_FILE_AND_METADATA': [CommandHandler('rename_process', file_handlers.process_rename)],
            },
            fallbacks=[],
        )
        application.add_handler(conv_handler)

        application.add_handler(CommandHandler("start", general_handlers.start))
        application.add_handler(CommandHandler("getid", general_handlers.get_id))
        application.add_handler(CommandHandler("help", general_handlers.help_command))
        application.add_handler(CommandHandler("setlogchannel", channel_handlers.set_log_channel))
        application.add_handler(CommandHandler("setfailchannel", channel_handlers.set_fail_channel))
        application.add_handler(CommandHandler("viewchannels", channel_handlers.view_channels))
        application.add_handler(CommandHandler("thumbnailchange", file_handlers.set_thumbnail))
        application.add_handler(CommandHandler("setsource", file_handlers.set_source))
        application.add_handler(CommandHandler("settarget", file_handlers.set_target))
        application.add_handler(CommandHandler("work", file_handlers.work))
        application.add_handler(CommandHandler("end", file_handlers.end))
        application.add_handler(CommandHandler("processstatus", file_handlers.process_status))
        application.add_handler(CommandHandler("adduser", user_handlers.add_user))
        application.add_handler(CommandHandler("userlist", user_handlers.user_list))
        application.add_handler(CommandHandler("removeuser", user_handlers.remove_user))
        application.add_handler(CommandHandler("setlimit", user_handlers.set_limit))
        application.add_handler(CommandHandler("addapi", api_handlers.add_api))
        application.add_handler(CommandHandler("apilist", api_handlers.api_list))
        application.add_handler(CommandHandler("removeapi", api_handlers.remove_api))

        application.add_error_handler(error_handler)  # error handler add किया गया

        logger.info("Bot started.")
        application.run_polling()
        logger.info("Bot stopped.")

    except Exception as e:
        logger.critical(f"A critical error occurred during bot initialization: {e}")

if __name__ == '__main__':
    main()
