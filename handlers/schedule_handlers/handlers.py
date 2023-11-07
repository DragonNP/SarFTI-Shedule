import helper
from databases import db_messages
from variables import GLOBAL_LOGGER_LEVEL, USER_ID_ADMIN, PATH_TO_LOG
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from SarFTI_Schedule import Schedule
from SarFTI_Schedule import visualize_schedule
from databases import users
from ..basic_handlers.keyboards import get_main as main_keyboard
from datetime import datetime

logger = helper.get_logger('schedule_handlers')


async def send_current_schedule(update: Update, _: CallbackContext) -> int:
    try:
        start_time = datetime.now()
        user_id = update.message.from_user.id

        logger.debug(f'Отправка текущего расписания. id:{user_id}')

        group_name = users.get_group(user_id)

        if group_name == '':
            await update.message.reply_text('Группа не выбрана, пожалуйста, зайдите в настройки и выберите группу',
                                            reply_markup=main_keyboard())
            return ConversationHandler.END

        file = visualize_schedule.save_schedule(Schedule().get_current_schedule(group_name))
        await update.message.reply_photo(file.get_path(), reply_markup=main_keyboard())
        file.remove()

        logger.debug(f'Заняло времени: {datetime.now() - start_time}')
        return ConversationHandler.END
    except Exception as e:
        return await error(update, e)


async def send_next_schedule(update: Update, _: CallbackContext) -> int:
    try:
        start_time = datetime.now()
        user_id = update.message.from_user.id

        logger.debug(f'Отправка расписания на следующую неделю. id:{user_id}')

        group_name = users.get_group(user_id)

        if group_name == '':
            await update.message.reply_text('Группа не выбрана, пожалуйста, зайдите в настройки и выберите группу',
                                            reply_markup=main_keyboard())
            return ConversationHandler.END

        schedule = Schedule().get_next_schedule(group_name)

        if schedule == {}:
            await update.message.reply_text('Расписание на следующую неделю еще не вышло',
                                            reply_markup=main_keyboard())
            return ConversationHandler.END

        file = visualize_schedule.save_schedule(schedule)
        await update.message.reply_photo(file.get_path(), reply_markup=main_keyboard())
        file.remove()

        logger.debug(f'Заняло времени: {datetime.now() - start_time}')
        return ConversationHandler.END
    except Exception as e:
        return await error(update, e)


async def chose_week(update: Update, _: CallbackContext) -> int:
    try:
        user_id = update.message.from_user.id

        logger.debug(f'Select week, id:{user_id}')

        if users.get_group(user_id) == '':
            await update.message.reply_text('Группа не выбрана, пожалуйста, зайдите в настройки и выберите группу',
                                            reply_markup=main_keyboard())
            return ConversationHandler.END

        weeks: dict = Schedule().get_weeks()

        keyboard = []
        flag = True

        for name in weeks.keys():
            week_id = str(weeks[name])
            if flag:
                keyboard.append([InlineKeyboardButton(name,
                                                      callback_data='week_' + week_id)])
            else:
                keyboard[-1] += [InlineKeyboardButton(name,
                                                      callback_data='week_' + week_id)]
            flag = not flag

        await update.message.reply_text('Выберите неделю:', reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    except Exception as e:
        return await error(update, e)


async def send_chosen_week(update: Update, _: CallbackContext) -> int:
    try:
        query = update.callback_query
        if 'week_' not in query.data:
            return -2

        user_id = query.from_user.id
        await query.answer()

        logger.debug(f'Send schedule on selected week, id:{user_id}')

        date_id: int = int(query.data.replace('week_', ''))
        group_name = users.get_group(user_id)

        if group_name == '':
            await query.message.reply_text('Группа не выбрана, пожалуйста, зайдите в настройки и выберите группу',
                                           reply_markup=main_keyboard())
            return ConversationHandler.END

        schedule = Schedule()

        file = visualize_schedule.save_schedule(schedule.get_schedule(id_week=date_id, group_name=group_name))
        await query.message.reply_photo(file.get_path(), reply_markup=main_keyboard())
        file.remove()
        return ConversationHandler.END
    except Exception as e:
        return await error(update, e)


async def error(update: Update, e: Exception = None) -> int:
    if not (e is None):
        logger.exception(e)

    await update.message.reply_text(db_messages.error,
                                    disable_web_page_preview=True,
                                    reply_markup=main_keyboard())

    if not (e is None) and GLOBAL_LOGGER_LEVEL == 'DEBUG':
        await update.get_bot().sendDocument(USER_ID_ADMIN, PATH_TO_LOG)

    return ConversationHandler.END
