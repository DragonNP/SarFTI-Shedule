from datetime import datetime
import bs4.element
from bs4 import BeautifulSoup, NavigableString
from databases import sarfti_data


def extract_weeks(soup: bs4.BeautifulSoup):
    weeks = {}
    selects = soup.find('select', attrs={'name': 'id'})

    for option in selects:
        if type(option) is NavigableString:
            continue

        name = datetime.strptime(option.text, '%Y-%m-%d').strftime('%d.%m.%Y')
        id_week = int(option.attrs['value'])

        weeks[name] = id_week

    sarfti_data.update_weeks(weeks)
    return weeks


def extract_schedule(html: str, group_name: str):
    soup = BeautifulSoup(html, "html.parser")
    schedules = {'ПН': {}, 'ВТ': {}, 'СР': {}, 'ЧТ': {}, 'ПТ': {}, 'СУБ': {}}

    all_trs = soup.find('table', class_='edit').findAll('tr')
    group_on_count = extract_groups(all_trs[0]).index(group_name) + 2

    for element in all_trs[1::]:
        day = ''
        pair_num = 0
        index_of_cell = 0
        for cell in element:
            if type(cell) == NavigableString:
                continue
            cell_text = cell.get_text(separator=' ', strip=True)

            if index_of_cell == 0:
                day = cell_text
            elif index_of_cell == 1:
                pair_num = int(cell_text)
                if pair_num not in schedules[day]:
                    schedules[day][pair_num] = []
            elif cell_text != '' and index_of_cell == group_on_count:
                schedules[day][pair_num] += [cell_text]
            index_of_cell += 1

    for day in schedules.keys():
        i = 0
        while i < len(schedules[day]):
            pair_num = list(schedules[day].keys())[i]

            if not schedules[day][pair_num]:
                del schedules[day][pair_num]
            else:
                i += 1

    extract_weeks(soup)
    return schedules


def extract_groups(tr):
    if sarfti_data.get_hash_groups() == hash(tr):
        return sarfti_data.get_groups()

    groups = []
    for td in tr:
        if type(td) == NavigableString or td.text in ['День', 'Пара']:
            continue
        groups.append(td.text)

    sarfti_data.update_all_groups(groups)
    sarfti_data.update_hash_groups(hash(tr))
    return groups
