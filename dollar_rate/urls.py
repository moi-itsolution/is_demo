from django.urls import path

from .views.dollar_rate import dollar_rate


urlpatterns = [
    path('', dollar_rate, name='my_dollar_rate'),
]
