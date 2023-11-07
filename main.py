from variables import GLOBAL_LOGGER_LEVEL, USER_ID_ADMIN, PATH_TO_LOG, TELEGRAM_BOT_TOKEN
import helper
from databases import users, db_messages, sarfti_data
import logging
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
    Application, CallbackQueryHandler, CallbackContext,
)
from handlers import basic_handlers
from handlers.basic_handlers import keyboards as basic_keyboards
from handlers import settings_handlers
from handlers import schedule_handlers


async def route_callback_handler(update: Update, context: CallbackContext) -> int:
    result = await schedule_handlers.callback_handler(update, context)
    if result != -2:
        return result


async def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Callback on unexpected errors
    :param update:
    :param context:
    :return:
    """

    error: Exception = context.error

    logger = helper.get_logger('main_error')
    logger.exception(error)
    if str(error) != 'httpx.ReadError':
        await update.message.reply_text(db_messages.error,
                                        disable_web_page_preview=True,
                                        reply_markup=basic_keyboards.get_main())

    if GLOBAL_LOGGER_LEVEL == 'DEBUG':
        await update.get_bot().sendDocument(USER_ID_ADMIN, PATH_TO_LOG)

    return ConversationHandler.END


def main() -> None:
    """
    Entrypoint in this program
    :return: None
    """

    # Initializing global level for logger and setting save logs in file
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        handlers=[
                            logging.FileHandler(PATH_TO_LOG),
                            logging.StreamHandler()
                        ])

    # Initializing application for Telegram Bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Adding basic handlers (/start, /help commands)
    basic_handlers.add_commands_handlers(application)
    # Adding text handlers related schedules and weeks
    schedule_handlers.add_message_handlers(application)
    # Adding text handlers related user settings
    settings_handlers.add_handlers(application)
    # Adding handler on any other text
    basic_handlers.add_any_text_handler(application)

    application.add_handler(CallbackQueryHandler(route_callback_handler))

    # Handler for unexpected errors
    application.add_error_handler(error_callback)

    users.load()
    sarfti_data.load()

    logger = helper.get_logger('main')
    logger.info('telegram bot started')

    # Run bot
    application.run_polling()


if __name__ == '__main__':
    main()
