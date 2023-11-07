from telegram import ReplyKeyboardMarkup
from . import texts


def get_settings():
    keyboard = [[texts.CHANGE_GROUP], [texts.RETURN_TO_MAIN]]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_cancel():
    keyboard = [[texts.CANCEL]]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
