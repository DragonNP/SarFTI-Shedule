import json
import logging
import os
from variables import GLOBAL_LOGGER_LEVEL, PATH_TO_USERS_DATA_BASE

logger = logging.getLogger('users_db')
logger.setLevel(GLOBAL_LOGGER_LEVEL)
db = {}
location = ''


def load():
    """
    Считывает файл базы данных и загружает ее в переменную
    :return: None
    """

    global logger, db, location

    logger.debug('Загрузка бд пользователей')

    location = os.path.expanduser(PATH_TO_USERS_DATA_BASE)

    if os.path.exists(location):
        db = json.load(open(location, 'r'))


def _check_user(user_id: int):
    """
    Проверяет существование id пользователя в базе данных
    :param user_id: id пользователя, которого надо проверить
    :return: True - если id есть в базе данных, False - если нет
    """

    global logger, db

    logger.debug(f'Проверка существования пользователя. id:{user_id}')
    return str(user_id) in db.keys()


def _dump_db():
    """
    Сохраняет базу данных в текстовый файл.
    :return: None
    """
    try:
        logger.debug('Сохранение дб')

        json.dump(db, open(location, 'w+', encoding='utf8'), ensure_ascii=False)
        logger.debug('Бд сохранена')
    except Exception as e:
        logger.error('Не удалось сохранить бд', e)


def add_user(user_id: int):
    """
    Добавляет id пользователя в базу данных
    :param user_id: id пользователя
    :return: None
    """

    global logger, db

    try:
        logger.debug(f'Добавление пользователя. id:{user_id}')

        if _check_user(user_id):
            logger.debug(f'Пользователь уже добавлен. id:{user_id}')
            return

        db[str(user_id)] = {'group': ''}
        _dump_db()
        logger.debug(f'Пользователь создан. id:{user_id}')
    except Exception as e:
        logger.error(f'Не удалось сохранить пользователя. id:{user_id}', e)


def get_group(user_id: int) -> str:
    """
    Возвращает: название группы
    :param user_id: id пользователя
    :return: название группы
    """

    global logger, db

    debug_text = f'id:{user_id}'

    try:
        logger.debug(f'Запрос всех названий категорий. {debug_text}')

        if not _check_user(user_id):
            logger.debug(f'Пользователь не найден. {debug_text}')
            add_user(user_id)
            return ''

        return db[str(user_id)]['group']
    except Exception as e:
        logger.error(f'Не удалось категории пользователя. {debug_text}', e)
        return ''


def change_group(user_id: int, group_name: str) -> bool:
    """
    Изменяет группу пользователя
    :param user_id: id пользователя
    :param group_name: название новой группы
    :return: True - если успешно, False - если нет
    """

    global logger, db

    debug_text = f'id:{user_id}'

    try:
        logger.debug(f'Смена группы. {debug_text}')

        if not _check_user(user_id):
            logger.debug(f'Пользователь не найден. {debug_text}')
            add_user(user_id)

        db[str(user_id)]['group'] = group_name
        _dump_db()
        logger.debug(f'Смена группы завершено. {debug_text}')
        return True
    except Exception as e:
        logger.error(f'Не удалось сменить группу. {debug_text}', e)
        return False
