from django.http import HttpResponse
from django.shortcuts import render
from settings import DOMAIN

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
#from integration_utils.its_utils.app_get_params import get_params_from_sources

APP_PATH = 'task_aggrid'
SIDEBAR_PATH = 'sidebar/'
WIDGET_PATH = f'https://{DOMAIN}/{APP_PATH}/{SIDEBAR_PATH}'
WORK_PATH = WIDGET_PATH


@main_auth(on_cookies=True)
def update(request):
	return render(request, 'my_task_aggrid.html')


@main_auth(on_cookies=True)
def install(request):
	but = request.bitrix_user_token
	PLACEMENT = 'TASK_USER_LIST_TOOLBAR'
	HANDLER = WORK_PATH
	LANG_ALL = {'ru': {'TITLE': 'отображение задач в таблице', 'DESCRIPTION': 'Удобная таблица'}}

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
	but = request.bitrix_user_token
	PLACEMENT = 'TASK_USER_LIST_TOOLBAR'
	HANDLER = WORK_PATH
	props = {'PLACEMENT': PLACEMENT, 'HANDLER': HANDLER}
	try:
		res = but.call_api_method('placement.unbind', props)['result']
	except Exception as ex:
		print(ex)
		return HttpResponse(str(ex))

	return HttpResponse('delete')
