from django.http import HttpResponse, JsonResponse
from django.template import loader
from pandas_datareader import data
import fix_yahoo_finance as yf
import pandas as pd
import datetime as datetime

yf.pdr_override()

def index(request):
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': '',
    }
    return HttpResponse(template.render(context,request))

def getData(request):

    data_request = request.POST.copy()

    datareturn = {}
    symbol = data_request['company']
    data_source = 'yahoo'

    start_date = datetime.datetime.strptime(data_request['data_from'], "%m/%d/%Y").strftime('%Y-%m-%d')
    end_date = datetime.datetime.strptime(data_request['data_to'], "%m/%d/%Y").strftime('%Y-%m-%d')
    try:
        df_ = data.get_data_yahoo(symbol, start=start_date, end=end_date)
        df = df_.reset_index()
        datareturn['smallest'] = min(df['Open'].min(), df['Close'].min())
        datareturn['biggest'] = max(df['Open'].max(), df['Close'].max())

        datareturn['Open'] = df['Open'].to_json(orient='values')
        datareturn['Close'] = df['Close'].to_json(orient='values')
        datareturn['High'] = df['High'].to_json(orient='values')
        datareturn['Low'] = df['Low'].to_json(orient='values')

        date_ = df['Date'].astype(str)
        t = []
        for n in date_:
            t.append(n)
        datareturn['Date'] = t
        return JsonResponse(datareturn, safe=False)
    except ValueError:  # raised if `y` is empty.
        return JsonResponse('error', safe=False)
