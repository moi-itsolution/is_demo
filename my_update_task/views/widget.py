from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

import json


@main_auth(on_cookies=True)
def main_view(request):
    # Позволяет редактировать задачу

    but = request.bitrix_user_token
    user_id = str(request.bitrix_user.bitrix_id)
    task_id = request.POST.get('PLACEMENT_OPTIONS')
    task_id = json.loads(task_id).get('TASK_ID')

    # получаем информацию по задаче
    try:
        task_info = but.call_api_method('tasks.task.get', {'taskId': task_id})['result']['task']
    except Exception as e:
        print(e)
        return HttpResponse(f'Произошла ошибка приложения. Возможно, задача не найдена в базе данных')

    # получаем список юзеров
    users = but.call_list_method('user.get')
    print(users)

    '''RESPONSIBLE_ID - Исполнитель
    ACCOMPLICES - Соисполнители
    DEADLINE - Крайний срок
    END_DATE_PLAN - Плановое завершение'''

    return HttpResponse(f'Hello update task {user_id}')
