from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

import json


FIELDS = ['ID', 'TITLE', 'STATUS', 'PRIORITY']  # , 'DEADLINE']  # for select

LOW_FIELDS = ['id', 'title', 'status', 'priority']  # , 'deadline']  # for work
NAMES = ['ID', 'Наименование', 'Статус', 'Приоритет']  # , 'Дедлайн']  # for table

HEADERS = list(zip(LOW_FIELDS, NAMES))

PRIORITY = {'2': 'Высокий', '1': 'Средний', '0': 'Низкий'}
STATUS = {'2': 'Ждет выполнения',
          '3': 'Выполняется',
          '4': 'Ожидает контроля',
          '5': 'Завершена',
          '6': 'Отложена',}


@main_auth(on_cookies=True)
def main_view(request):
    but = request.bitrix_user_token
    user_id = str(request.bitrix_user.bitrix_id)
    tasks = but.call_list_method('tasks.task.list', {'filter': {'RESPONSIBLE_ID': user_id}, 'select': FIELDS})['tasks']
    statuses = '234'
    render_tasks = []

    # Оставляем только актуальные задачи, попутно меняем цифры на слова (статус, приоритет)
    for task in tasks:
        if task['status'] not in statuses:
            continue
        temp = {}
        for field in LOW_FIELDS:
            if field == 'priority':
                temp[field] = PRIORITY[task[field]]
            elif field == 'status':
                temp[field] = STATUS[task[field]]
            else:
                temp[field] = task[field]
        render_tasks.append(temp)

    # формируем опции для aggrid
    option_name = 'my_task_grid'
    s1 = f'const {option_name} = ' + '{\n'

    # формируем данные
    s2 = f'rowData: {render_tasks},\n'

    # формируем опции для столбцов
    s3 = f'columnDefs: {get_defs()}' + '};'

    full_option = s1 + s2 + s3

    # selector, div_id for template
    div_id = 'my_task_grid'

    selector = f'const eDiv = document.querySelector("#{div_id}");'
    # api = f'const gridApi = agGrid.createGrid(eDiv, {option_name});'
    api = f'const gridApi = agGrid.createGrid(eDiv, {option_name});'

    script = '\n'.join(('<script>', full_option, selector, api, '</script>'))

    context = {'div_id': div_id,
               'ag_script': script}

    print(script)

    return render(request, 'tasks_ag_grid.html', context)


def get_defs():
    defs = []
    for column in HEADERS:
        temp = {
            'field': column[0],
            'headerName': column[1] if column[1] else column[0]
        }
        defs.append(temp)

    return json.dumps(defs, ensure_ascii=False)
