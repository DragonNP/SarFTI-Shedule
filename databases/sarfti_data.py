import json
import logging
import os
from variables import GLOBAL_LOGGER_LEVEL, PATH_TO_SARFTI_DATA_BASE

logger = logging.getLogger('sarfti_data')
logger.setLevel(GLOBAL_LOGGER_LEVEL)
db = {}
location = ''


def load() -> None:
    """
    Load database from file and save her to variable
    :return: None
    """

    global logger, db, location
    logger.info('loading database')

    location = os.path.expanduser(PATH_TO_SARFTI_DATA_BASE)

    if os.path.exists(location):
        db = json.load(open(location, 'r'))

    logger.debug('loaded database')


def _dump_db() -> None:
    """
    Save database to file
    :return: None
    """
    global logger, db, location
    try:
        logger.info('saving database')

        json.dump(db, open(location, 'w+', encoding='utf8'), ensure_ascii=False)
        logger.debug('saved database')
    except Exception as e:
        logger.error('failed to save database', e)


def update_weeks(weeks_ids: dict):
    """
    Update weeks ids
    :param weeks_ids: dict of weeks ids
    :return: None
    """
    global logger, db
    try:
        logger.info('updating weeks ids')

        if 'weeks' in db and db['weeks'] == weeks_ids:
            logger.debug('new weeks id equal old')
            return

        db['weeks'] = weeks_ids
        _dump_db()
        logger.debug('weeks updated')
    except Exception as e:
        logger.error(f'failed to save weeks weeks_ids={weeks_ids}', e)


def get_weeks() -> dict:
    """
    Returning dict of weeks. Key str format date, value id week
    :return: dict of weeks
    """
    global logger, db
    logger.info('getting weeks')

    if 'weeks' in db:
        return db['weeks']
    logger.debug('weeks empty')
    return {}


def update_all_groups(groups: list):
    """
    Update all names groups
    :param groups: list of groups name
    :return: None
    """
    global logger, db
    try:
        logger.info('updating groups')

        if 'groups' in db and db['groups']['data'] == groups:
            logger.debug('new groups names equal old')
            return

        if 'groups' not in db:
            db['groups'] = {'data': [], 'hash': -1}

        db['groups']['data'] = groups
        _dump_db()
        logger.debug('groups updated')
    except Exception as e:
        logger.error(f'failed to save groups name groups={groups}', e)


def get_groups() -> list:
    """
    Returning list of groups name
    :return: list of groups name
    """
    global logger, db
    logger.info('getting groups')

    if 'groups' in db:
        return db['groups']['data']
    logger.debug('groups name empty')
    return []


def update_hash_groups(new_hash: int) -> None:
    """
    Update hash weeks
    :param new_hash: hash of weeks
    :return: None
    """
    global logger, db
    try:
        logger.info('updating hash weeks')

        if 'groups' in db and db['groups']['hash'] == new_hash:
            logger.debug('new hash groups equal old')
            return

        if 'groups' not in db:
            db['groups'] = {'data': [], 'hash': -1}

        db['groups']['hash'] = new_hash
        _dump_db()
        logger.debug('hash groups updated')
    except Exception as e:
        logger.error(f'failed to save hash groups new_hash={new_hash}', e)


def get_hash_groups() -> int:
    """
    Returning hash of groups.
    :return: hash of groups
    """
    global logger, db
    logger.info('getting hash groups')

    if 'groups' in db:
        return db['groups']['hash']
    logger.debug('hash groups empty')
    return -1


def add_php_sess_id(php_sess_id: str) -> None:
    """
    Adding PHPSESSID to database
    :param php_sess_id: PHPSESSID
    :return: None
    """
    global logger, db
    try:
        logger.info('adding php_sess_id')

        db['PHP_SESS_ID'] = php_sess_id
        _dump_db()
        logger.debug(f'added php_sess_id={php_sess_id}')
    except Exception as e:
        logger.error(f'failed to save php_sess_id={php_sess_id}', e)


def get_php_sess_id() -> str:
    """
    Returning PHPSESSID
    :return: PHPSESSID
    """
    global logger, db

    logger.info('getting php_sess_id')
    if 'PHP_SESS_ID' in db:
        return db['PHP_SESS_ID']
    logger.debug('php_sess_id dont saved')
    return ''
