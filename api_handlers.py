import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from config import BOT_TOKEN, ADMIN_ID, FAIL_CHANNEL_ID
from handlers.general_handlers import start, get_id, help_command  # अगर आपके पास ये handlers हैं
from handlers.channel_handlers import set_log_channel, set_fail_channel, view_channels
from handlers.file_handlers import set_thumbnail, rename_file, button, process_rename, set_source, set_target, work, end, process_status
from handlers.user_handlers import add_user, user_list, remove_user, set_limit
from handlers.api_handlers import add_api, api_list, remove_api

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('filenamechange', rename_file)],
        states={
            'WAITING_FOR_FORMAT_SELECTION': [CallbackQueryHandler(button)],
            'WAITING_FOR_FILE_AND_METADATA': [CommandHandler('rename_process', process_rename)],
        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("getid", get_id))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("setlogchannel", set_log_channel))
    dp.add_handler(CommandHandler("setfailchannel", set_fail_channel))
    dp.add_handler(CommandHandler("viewchannels", view_channels))
    dp.add_handler(CommandHandler("thumbnailchange", set_thumbnail))
    dp.add_handler(CommandHandler("setsource", set_source))
    dp.add_handler(CommandHandler("settarget", set_target))
    dp.add_handler(CommandHandler("work", work))
    dp.add_handler(CommandHandler("end", end))
    dp.add_handler(CommandHandler("processstatus", process_status))
    dp.add_handler(CommandHandler("adduser", add_user))
    dp.add_handler(CommandHandler("userlist", user_list))
    dp.add_handler(CommandHandler("removeuser", remove_user))
    dp.add_handler(CommandHandler("setlimit", set_limit))
    dp.add_handler(CommandHandler("addapi", add_api))
    dp.add_handler(CommandHandler("apilist", api_list))
    dp.add_handler(CommandHandler("removeapi", remove_api))

    updater.start_polling()
    updater.idle()  # Fix indentation here

if __name__ == '__main__':
    main()
