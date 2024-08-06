from django.urls import path
from .views.main_view import my_gtable_work

urlpatterns = [
    path('', my_gtable_work, name="my_gtable_work")
]
