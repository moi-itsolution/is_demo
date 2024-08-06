import gspread
from .google_auth import google_auth
import time
import json

TEMP_PATH = 'temp_files/'


def import_values(url):
    service = google_auth()

    gt = url

    client = gspread.authorize(service)
    result = client.open_by_url(gt)
    sheet = result.get_worksheet(0)
    values = sheet.get_all_records()

    name = str(time.time()).replace('.', '') + '.json'

    with open(TEMP_PATH + name, 'w') as f:
        json.dump(values, f)

    return f'Файл {name} сохранен в папке {TEMP_PATH}'


def export_values(url, json_values: dict):

    service = google_auth()

    gt = url

    # Получаем лист
    client = gspread.authorize(service)
    result = client.open_by_url(gt)
    sheet = result.get_worksheet(0)
    sheet.clear()

    # Заполняем таблицу
    headers = list(json_values[0].keys())
    sheet.append_row(headers)

    for row in json_values:
        sheet.append_row(list(row.values()))

    return 'Файлы успешно загружены'
