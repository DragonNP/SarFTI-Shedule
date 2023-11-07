import logging
import os

PATH_TO_USERS_DATA_BASE = './data/users.json'
PATH_TO_GROUPS_DATA_BASE = './data/groups.json'
PATH_TO_SARFTI_DATA_BASE = './data/sarfti.json'
PATH_TO_LOG = './data/logger.log'
PATH_TO_PHOTOS = './data/photos/'
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_API', None)
GLOBAL_LOGGER_LEVEL = os.environ.get('LOGGER_LEVEL', logging.INFO)
USER_ID_ADMIN = 576476322
