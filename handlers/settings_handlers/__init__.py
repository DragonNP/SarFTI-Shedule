from databases import db_messages
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.ext import Application
from . import handlers
from .conversation_states import *
from . import texts
from ..basic_handlers.texts import SETTINGS as TEXT_SETTINGS


def add_handlers(application: Application):
    application.add_handler(MessageHandler(filters.Text([TEXT_SETTINGS]), handlers.send_settings))
    application.add_handler(MessageHandler(filters.Text([texts.RETURN_TO_MAIN]), handlers.main_page))

    application.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Text([texts.CHANGE_GROUP]), handlers.start_change_group)],
        states={
            CHANGE_GROUP_STATE_GROUP: [
                MessageHandler(filters.TEXT & (~filters.Text([db_messages.cancel_btn])), handlers.end_change_group)],
        },
        fallbacks=[MessageHandler(filters.Text([db_messages.cancel_btn]), handlers.send_settings)]
    ))
