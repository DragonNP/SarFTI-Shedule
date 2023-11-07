from SarFTI_Schedule import Schedule
import helper
from databases import db_messages, users
from variables import GLOBAL_LOGGER_LEVEL, USER_ID_ADMIN, PATH_TO_LOG
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from . import keyboards
from ..basic_handlers import keyboards as main_keyboards
from .conversation_states import *

logger = helper.get_logger('settings_handlers')


async def start_change_group(update: Update, _: CallbackContext) -> int:
    try:
        await update.message.reply_text('Введите вашу группу', reply_markup=keyboards.get_settings())
        return CHANGE_GROUP_STATE_GROUP
    except Exception as e:
        return await error(update, e)


async def main_page(update: Update, _: CallbackContext) -> int:
    try:
        await update.message.reply_text('Главное меню', reply_markup=main_keyboards.get_main())
        return ConversationHandler.END
    except Exception as e:
        return await error(update, e)


async def end_change_group(update: Update, _: CallbackContext) -> int:
    try:
        groups = Schedule().get_groups()
        user_group = update.message.text
        user_id = update.message.from_user.id

        if user_group not in groups:
            await update.message.reply_text('Группа не найдена, попробуйте еще раз',
                                            reply_markup=keyboards.get_cancel())
            return CHANGE_GROUP_STATE_GROUP

        users.change_group(user_id, user_group)
        await update.message.reply_text(f'Группа изменена на: {user_group}',
                                        reply_markup=keyboards.get_settings())

        return ConversationHandler.END
    except Exception as e:
        return await error(update, e)


async def send_settings(update: Update, _: CallbackContext) -> int:
    try:
        user_id = update.message.from_user.id
        groups = Schedule().get_groups()

        text = 'Настройки:\n'
        if users.get_group(user_id) in groups:
            text += 'Группа: ' + users.get_group(user_id)
        else:
            text += 'У вас нет группы'

        await update.message.reply_text(text, reply_markup=keyboards.get_settings())
        return ConversationHandler.END
    except Exception as e:
        return await error(update, e)


async def error(update: Update, e: Exception = None) -> int:
    if not (e is None):
        logger.exception(e)

    await update.message.reply_text(db_messages.error,
                                    disable_web_page_preview=True,
                                    reply_markup=keyboards.get_settings())

    if not (e is None) and GLOBAL_LOGGER_LEVEL == 'DEBUG':
        await update.get_bot().sendDocument(USER_ID_ADMIN, PATH_TO_LOG)

    return ConversationHandler.END
