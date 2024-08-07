from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import datetime

import yfinance as yf

TIME_DELTA = datetime.timedelta(days=31)

@main_auth(on_cookies=True)
def dollar_rate(request):
    tiker = 'USDRUB=X'

    end = datetime.datetime.now()
    start = end - TIME_DELTA

    start = start.strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')
    data = yf.download(tiker, start, end, interval='1d')  # yfinance возвращает 22 значения
    data = data.to_dict()

    values = data['Open']
    values = [(str(k.date()), round(v, 1)) for k, v in values.items()]

    context = {'values': values}

    return render(request, 'dollar_rate.html', context)
