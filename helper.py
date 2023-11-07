import logging
from telegram import ReplyKeyboardMarkup
from databases.db_messages import cancel_btn
from variables import GLOBAL_LOGGER_LEVEL


def get_logger(module_name: str) -> logging:
    logger = logging.getLogger(module_name)
    logger.setLevel(GLOBAL_LOGGER_LEVEL)

    return logger