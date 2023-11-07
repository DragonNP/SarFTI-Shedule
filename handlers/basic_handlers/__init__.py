from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.ext import Application
from . import handlers


def add_commands_handlers(application: Application):
    application.add_handler(CommandHandler('start', handlers.send_start_msg))
    application.add_handler(CommandHandler('help', handlers.send_start_msg))


def add_any_text_handler(application: Application):
    application.add_handler(MessageHandler(filters.TEXT, handlers.send_start_msg))
