from django.http import HttpResponse
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
            'deadline': lambda x: datetime.fromisoformat(x).strftime('%d.%m.%Y %H:%M'),
            }


@main_auth(on_cookies=True)
def main_view(request):
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
            elif field == 'title':
                # 'title': lambda x: f'<a href="https://b24-qzb8tw.bitrix24.ru/company/personal/user/1/tasks/task/view/5/"'
                # link = f'https://{request.GET.get("DOMAIN")}/company/personal/user/{user_id}/tasks/task/view/{task["id"]}/'
                # print(link)
                # temp[field] = f'<a href="{link}">{task["title"]}</a>'
                temp[field] = task[field]
            else:
                temp[field] = task[field]
        render_tasks.append(temp)

    # формируем опции для aggrid

    option_name = 'my_task_grid'
    s1 = f'const {option_name} = ' + '{\n'

    # формируем данные
    s2 = f'rowData: {render_tasks},\n'

    s3 = '''defaultColDef: {
                        floatingFilter: true,
                        resizable: true,
                        sortable: true,
                        filter: true,
                    },'''

    s4 = '''onGridReady: function(params) {
                        params.columnApi.autoSizeAllColumns();
                    },'''

    s5 = f'columnDefs: {get_defs()}' + '};'

    full_option = s1 + s2 + s3 + s4 + s5

    # selector, div_id for template
    div_id = 'my_task_grid'

    selector = f'const eDiv = document.querySelector("#{div_id}");'
    # api = f'const gridApi = agGrid.createGrid(eDiv, {option_name});'
    api = f'const gridApi = agGrid.createGrid(eDiv, {option_name});'

    script = '\n'.join(('<script>', full_option, selector, api, '</script>'))

    context = {'div_id': div_id,
               'ag_script': script}

    print(script)

    # https://b24-qzb8tw.bitrix24.ru/company/personal/user/1/tasks/task/view/5/

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
