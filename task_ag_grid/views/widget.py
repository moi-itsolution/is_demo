
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from datetime import datetime
import json


FIELDS = ['ID', 'TITLE', 'STATUS', 'PRIORITY', 'DEADLINE']  # for select

LOW_FIELDS = ['id', 'title', 'status', 'priority', 'deadline']  # for work
NAMES = ['ID', 'Наименование', 'Статус', 'Приоритет', 'Дедлайн']  # for table

HEADERS = list(zip(LOW_FIELDS, NAMES))

PRIORITY = {'2': 'Высокий', '1': 'Средний', '0': 'Низкий'}
STATUS = {'2': 'Ждет выполнения',
          '3': 'Выполняется',
          '4': 'Ожидает контроля',
          '5': 'Завершена',
          '6': 'Отложена'}

COMMANDS = {'priority': lambda x: PRIORITY[x],
            'status': lambda x: STATUS[x],
            'deadline': lambda x: datetime.fromisoformat(x).strftime('%d.%m.%Y %H:%M') if x else '---',
            }


@main_auth(on_cookies=True)
def main_view(request):
    # Формирование ag-grid таблицы
    but = request.bitrix_user_token
    user_id = str(request.bitrix_user.bitrix_id)
    tasks = but.call_list_method('tasks.task.list', {'filter': {'RESPONSIBLE_ID': user_id}, 'select': FIELDS})['tasks']

    render_tasks = []

    # Оставляем только актуальные задачи, попутно меняем цифры на слова (статус, приоритет)
    for task in tasks:
        if task['status'] == '5':  # не показываем завершенные
            continue
        temp = {}
        for field in LOW_FIELDS:
            if COMMANDS.get(field):
                temp[field] = COMMANDS[field](task[field])
            else:
                temp[field] = task[field]
            temp['user_id'] = user_id
            temp['domain'] = request.GET.get("DOMAIN")
        render_tasks.append(temp)

    render_tasks = json.dumps(render_tasks)
    coll_defs = get_defs()
    div_id = 'my_task_grid'

    context = {'div_id': div_id,
               'render_tasks': render_tasks,
               'coll_defs': coll_defs}

    return render(request, 'tasks_ag_grid.html', context)


def get_defs():
    # получение базовых настроек для колонок ag-grid
    # в шаблоне при желании можно поставить, будет самая обычная таблица
    defs = []
    for column in HEADERS:
        temp = {
            'field': column[0],
            'headerName': column[1] if column[1] else column[0],
            'rowGroup': False,
            'resizable': True,
            'autoHeight': True,
        }
        defs.append(temp)
    result = json.dumps(defs, ensure_ascii=False)
    return result
