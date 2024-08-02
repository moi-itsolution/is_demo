from django.urls import path

from .views.loads import SIDEBAR_PATH, install, update, delete
from .views.widget import main_view


urlpatterns = [
    path(SIDEBAR_PATH, main_view, name='my_task_updater_main'),
    path('update/', update, name='my_task_updater_update'),
    path('install/', install, name='my_task_updater_install'),
    path('delete/', delete, name='my_task_updater_delete'),
]