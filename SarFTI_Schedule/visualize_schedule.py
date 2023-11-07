import os
import pandas as pd
from datetime import datetime
from variables import PATH_TO_PHOTOS
import imgkit


class File:
    def __init__(self, path: str):
        self._path = path

    def get_path(self):
        return self._path

    def remove(self):
        os.remove(self._path)


def save_schedule(schedule: dict) -> File:
    html = ''
    for i in [0, 1, 2]:
        if i >= len(schedule):
            break

        day = list(schedule.keys())[i]
        pairs = schedule[day]

        if len(pairs) != 0:
            max_count_pair = int(list(pairs.keys())[-1])
        else:
            max_count_pair = 0

        if i + 3 < len(schedule):
            day_3 = list(schedule.keys())[i + 3]
            pairs_3 = schedule[day_3]

            if len(pairs_3) != 0:
                max_count_pair = max(max_count_pair, int(list(pairs_3.keys())[-1]))

        frame = {'Пара': []}
        for number in range(1, max_count_pair + 1):
            frame['Пара'] += [number]

        # Пн
        frame[day] = []
        for index in range(max_count_pair):
            if (index + 1) in pairs:
                lessons = pairs[index + 1]
                text = ''
                for index_lesson in range(len(lessons)):
                    text += lessons[index_lesson]
                    if index_lesson + 1 != len(lessons):
                        text += '<br>'
                frame[day].append(text)
            else:
                frame[day].append('')

        if i + 3 < len(schedule):
            day_3 = list(schedule.keys())[i + 3]
            pairs_3 = schedule[day_3]
            frame[day_3] = []
            for index in range(max_count_pair):
                if (index + 1) in pairs_3:
                    text = ''
                    lessons = pairs_3[index + 1]
                    for index_lesson in range(len(lessons)):
                        text += lessons[index_lesson]
                        if index_lesson + 1 != len(lessons):
                            text += '<br>'
                    frame[day_3].append(text)
                else:
                    frame[day_3].append('')

        df = pd.DataFrame(frame)
        html += df.to_html(escape=False, index=False)

    path_to_file = PATH_TO_PHOTOS + str(datetime.now()) + '.png'
    imgkit.from_string(html, path_to_file, css='table.css')

    return File(path_to_file)
