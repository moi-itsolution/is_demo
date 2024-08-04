from django.http import HttpResponse
from django.shortcuts import render
from settings import DOMAIN

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

APP_PATH = 'my_update_task'
SIDEBAR_PATH = 'sidebar/'
WIDGET_PATH = f'https://{DOMAIN}/{APP_PATH}/{SIDEBAR_PATH}'
WORK_PATH = WIDGET_PATH


@main_auth(on_cookies=True)
def update(request):
    # Окно выбора установки / удаления
    return render(request, 'my_task_update.html')


@main_auth(on_cookies=True)
def install(request):
    # Установка приложения на верхний тулбар окна задачи
    but = request.bitrix_user_token
    PLACEMENT = 'TASK_VIEW_TOP_PANEL'
    HANDLER = WORK_PATH
    LANG_ALL = {'ru': {'TITLE': 'Редактирование задачи', 'DESCRIPTION': 'Редактирование параметров задачи в отдельном окне'}}

    props = {'PLACEMENT': PLACEMENT,
             'HANDLER': HANDLER,
             'LANG_ALL': LANG_ALL}
    try:
        res = but.call_api_method('placement.bind', props)['result']
    except Exception as ex:
        print(ex)
        return HttpResponse('Вероятно, этот обработчик уже установлен')

    return HttpResponse('install')


@main_auth(on_cookies=True)
def delete(request):
    # Удаление приложения
    but = request.bitrix_user_token
    PLACEMENT = 'TASK_VIEW_TOP_PANEL'
    HANDLER = WORK_PATH
    props = {'PLACEMENT': PLACEMENT, 'HANDLER': HANDLER}
    try:
        res = but.call_api_method('placement.unbind', props)['result']
    except Exception as ex:
        print(ex)
        return HttpResponse(str(ex))

    return HttpResponse('delete')
