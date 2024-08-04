from django import forms
from datetime import datetime


def get_form(users, task_info):
    # получение формы для редактирования задачи

    form_users = tuple([(user['ID'], f'{user["LAST_NAME"]} {user["NAME"]}') for user in users])

    print(task_info['deadline'], task_info['endDatePlan'])

    class TaskForm(forms.Form):
        responsible = forms.ChoiceField(choices=form_users, label='Исполнитель')
        accomplices = forms.MultipleChoiceField(choices=form_users, label='Соисполнители')

        deadline = forms.DateTimeField(label='Дедлайн')
        if task_info['deadline']:
            dt = datetime.fromisoformat(task_info['deadline'])
            deadline.initial = dt.strftime('%Y-%m-%dT%H:%M')
        deadline.widget = forms.DateInput(attrs={'type': 'datetime-local'})

        end_date = forms.DateTimeField(label='Плановое завершение')
        if task_info['endDatePlan']:
            dt = datetime.fromisoformat(task_info['endDatePlan'])
            end_date.initial = dt.strftime('%Y-%m-%dT%H:%M')
        end_date.widget = forms.DateInput(attrs={'type': 'datetime-local'})

        task_id = forms.CharField(initial=task_info['id'])
        task_id.widget = forms.HiddenInput()

    return TaskForm()


def change_task(post, but):
    # Изменение задачи

    post = dict(post)
    print(post)
    responsible = post.get('responsible')[0]
    accomplices = post.get('accomplices')
    deadline = post.get('deadline')[0]
    end_date = post.get('end_date')[0]
    task_id = post.get('task_id')[0]

    try:
        but.call_api_method('tasks.task.update', {'taskId': task_id,
                                                  'fields': {'RESPONSIBLE_ID': responsible,
                                                             'ACCOMPLICES': accomplices,
                                                             'DEADLINE': deadline,
                                                             'END_DATE_PLAN': end_date}})

    except Exception as e:
        print(e)
        return 'Ошибка. Попробуте позже'

    return 'Задача отредактирована'
