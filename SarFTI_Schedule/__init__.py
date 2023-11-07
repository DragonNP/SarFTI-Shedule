from bs4 import BeautifulSoup

from databases import sarfti_data
from . import variables
from .authorization import Guest
from . import weektime
from . import parser


class Schedule:
    def __init__(self):
        self._user = Guest()

    def get_weeks(self):
        weeks = sarfti_data.get_weeks()

        if weeks != {}:
            return weeks
        return self.update_weeks()

    def update_weeks(self):
        user = self._user
        html = user.make_get_request()
        weeks = parser.extract_weeks(BeautifulSoup(html, "html.parser"))
        return weeks

    def get_groups(self):
        return sarfti_data.get_groups()

    def get_schedule(self, id_week: int, group_name):
        user = self._user
        data = {
            'id': str(id_week),
            'show': 'Распечатать',
            'compact': 'compact'
        }

        html = user.make_post_request(data)
        schedule = parser.extract_schedule(html, group_name)
        return schedule

    def get_current_schedule(self, group_name):
        week_name = weektime.get_current_week()
        week_id = self.get_weeks()
        if week_name not in week_id:
            week_id = self.update_weeks()[week_name]
        else:
            week_id = week_id[week_name]

        return self.get_schedule(week_id, group_name)

    def get_next_schedule(self, group_name):
        week_name = weektime.get_next_week()

        all_weeks = self.get_weeks()
        if week_name in all_weeks:
            week_id = all_weeks[week_name]
            return self.get_schedule(week_id, group_name)
        return {}
