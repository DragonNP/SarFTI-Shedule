import helper
from databases import db_messages, users
from telegram import Update
from telegram.ext import (
    CallbackContext,
)
from . import keyboards

logger = helper.get_logger('basic_handlers')


async def send_start_msg(update: Update, _: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logger.info(f'New message: /start, /help or any other text')

    users.add_user(user_id)

    await update.message.reply_text(db_messages.start_msg,
                                    disable_web_page_preview=True,
                                    reply_markup=keyboards.get_main())
