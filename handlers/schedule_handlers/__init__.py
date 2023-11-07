from telegram import Update
from telegram.ext import (
    MessageHandler,
    filters,
    CallbackContext,
)
from telegram.ext import Application
from ..basic_handlers import texts as basic_texts
from . import handlers


def add_message_handlers(application: Application):
    application.add_handler(MessageHandler(filters.Text([basic_texts.CURRENT_WEEK]), handlers.send_current_schedule))
    application.add_handler(MessageHandler(filters.Text([basic_texts.NEXT_WEEK]), handlers.send_next_schedule))
    application.add_handler(MessageHandler(filters.Text([basic_texts.SELECT_WEEK]), handlers.chose_week))


async def callback_handler(update: Update, _: CallbackContext) -> int:
    return await handlers.send_chosen_week(update, _)
