from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

import json

from .utils import get_form, change_task



@main_auth(on_cookies=True)
def main_view(request):
    # Позволяет редактировать задачу

    but = request.bitrix_user_token

    if 'accomplices' in request.POST:
        result = change_task(request.POST, but)

        context = {'done': True, 'info': result}
        return render(request, 'redactor.html', context)

    # user_id = str(request.bitrix_user.bitrix_id)
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
    form = get_form(users, task_info)

    context = {'form': form, 'done': False, 'info': ''}

    return render(request, 'redactor.html', context)
