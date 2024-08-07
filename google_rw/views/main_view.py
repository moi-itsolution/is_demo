from django.http import HttpResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from google_rw.google_auth import google_auth
from ..forms import get_form, get_choice_form
from ..utils import import_values, export_values

import json

VALUES = {'import': 'Скачать', 'export': 'Загрузить'}
REV_VALUES = {v: k for k, v in VALUES.items()}

# url = 'https://docs.google.com/spreadsheets/d/1ZuKXEK0hwJyxFwGxoi77G0PaOh4Qg4SDZBNkHDws2iU/edit#gid=1891471437'


@main_auth(on_cookies=True)
def my_gtable_work(request):
    # получение или выгрузка данных в/из гугл таблиц

    choices = tuple(VALUES.items()) # данные для формы выбора

    if request.method == 'POST':
        if request.POST.get('choice'):  # Проверяем, была ли форма выбора
            form = get_choice_form(choices)(request.POST)
            if form.is_valid():
                data = form.cleaned_data  # Получаем то, что будем делать
                var = data['choice']
                print(var)

                form = get_form(var)
                context = {'form': form, 'work': True}
                return render(request, 'google_sheet_rw.html', context)
            else:
                return HttpResponse(f'POST method error')

        # Если мы уже работаем с загрузкой/выгрузкой
        var = request.POST.get('action')
        if var == 'import':
            # Скачиваем данные из таблицы
            response = import_values(request.POST.get('url'))

            return response
        elif var == 'export':
            # Загружаем данные в таблицу
            form = get_form('export')(request.POST, request.FILES)
            info = 'Empty result'

            if form.is_valid():
                data = form.cleaned_data

                bin_file = form.cleaned_data['json_file'].file.read()

                json_file = json.loads(bin_file)

                info = export_values(data['url'], json_file)

        else:
            info = 'Не удалось выполнить указанное действие'

        context = {'info': info, 'done': True}
        response = render(request, 'google_sheet_rw.html', context)

        return response

    else:
        # Если метод не POST, то направляем форму с выбором, что делать - загрузка/выгрузка данных
        form = get_choice_form(choices)
        context = {'form': form, 'work': False}
        return render(request, 'google_sheet_rw.html', context)
