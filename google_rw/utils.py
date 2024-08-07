from django.http import HttpResponse
from .google_auth import google_auth
import time
import json
import gspread


TEMP_PATH = 'temp_files/'


def import_values(url):
    service = google_auth()

    gt = url

    client = gspread.authorize(service)
    result = client.open_by_url(gt)
    sheet = result.get_worksheet(0)
    values = sheet.get_all_records()

    response = HttpResponse(json.dumps(values, ensure_ascii=False), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="from_table.json"'

    return response


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
