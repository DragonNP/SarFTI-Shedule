from telegram import ReplyKeyboardMarkup
from . import texts


def get_main():
    keyboard = [[texts.CURRENT_WEEK, texts.NEXT_WEEK],
                [texts.SELECT_WEEK],
                [texts.SETTINGS]]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
