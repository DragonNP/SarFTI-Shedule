import requests
from . import variables
from databases import sarfti_data
import helper

logger = helper.get_logger('authorization')


class RequestMethod:
    GET = 'get'
    POST = 'post'


class Guest:
    def __init__(self):
        self._schedule_url = variables.SCHEDULE_URL
        self._login_url = variables.LOGIN_URL
        self._db = sarfti_data

        logger.debug('created Guest class instance')

    def _login(self):
        db = self._db
        url = self._login_url
        logger.info('loging in site as guest')

        response = requests.get(url)
        php_sess_id = response.cookies['PHPSESSID']
        data = {
            'login': '',
            'password': '',
            'guest': 'Войти как Гость'
        }

        requests.post(url, data=data, cookies={'PHPSESSID': php_sess_id})
        db.add_php_sess_id(php_sess_id)

        logger.debug('php_sess_id received and saved')
        return php_sess_id

    def make_get_request(self):
        logger.info('making get request as guest')
        return self._make_request(RequestMethod.GET)

    def make_post_request(self, data: dict):
        logger.info('making post request as guest')
        return self._make_request(RequestMethod.POST, data)

    def _make_request(self, method: str, data=None):
        if data is None:
            data = {}
        db = self._db
        url = self._schedule_url

        logger.debug(f'making {method} request with data={data} as guest')

        php_sess_id = db.get_php_sess_id()
        if php_sess_id == '':
            php_sess_id = self._login()

        if method == RequestMethod.POST:
            response = requests.post(url, data=data, cookies={'PHPSESSID': php_sess_id}, allow_redirects=False)
        else:
            response = requests.get(url, cookies={'PHPSESSID': php_sess_id}, allow_redirects=False)

        if response.status_code != 302:
            response.encoding = 'utf-8'
            logger.debug('success')
            return response.text

        logger.debug(f'making request again, maybe php_sess_id cookie expired')
        php_sess_id = self._login()
        if method == RequestMethod.POST:
            response = requests.post(url, data=data, cookies={'PHPSESSID': php_sess_id}, allow_redirects=False)
        else:
            response = requests.get(url, cookies={'PHPSESSID': php_sess_id}, allow_redirects=False)

        if response.status_code != 302:
            response.encoding = 'utf-8'
            logger.debug('success')
            return response.text

        logger.error(f'failed. status_code:{response.status_code} php_sess_id={php_sess_id} data={data}')
        return ''
