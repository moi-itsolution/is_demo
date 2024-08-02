from django.urls import path

from .views.task_aggrid import SIDEBAR_PATH, install, update, delete
from .views.widget import main_view


urlpatterns = [
    path(SIDEBAR_PATH, main_view, name='my_task_aggrid_main'),
    path('update/', update, name='my_task_aggrid_update'),
    path('install/', install, name='my_task_aggrid_install'),
    path('delete/', delete, name='my_task_aggrid_delete'),
]