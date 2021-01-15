from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import datetime
import json
import sys
#sys.path.append('..')
from .stockfilter import Filter
# from data import Data
from stock_site import settings

# Create your views here.
def index(request):
    return render(request, 'filter/index.html')

def get_filter_data(request):
    raw_data = json.loads(request.body)
    start_date, filter_list = convertToFilterFormat(raw_data)
    if not filter_list:
        result = {"data": []}
        return JsonResponse(result, safe=False)


    #stock_database = Data(pickle_filename="stock_data.pickle")
    #stock_database.load_data_from_pickle()
    #stock_data = stock_database.get_data()
    stock_data = settings.stock_data

    #datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    #start_date = datetime.datetime.strptime('2020-09-09', "%Y-%m-%d").date()
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    # start_date = datetime.datetime.today().date()
    stock_filter = Filter(stock_data)
    result = stock_filter.get_result_web(start_date, filter_list)
    result = {"data": result}
    print("Get result")
    return JsonResponse(result, safe=False)

def convertToFilterFormat(raw_data):
    start_date = raw_data['date']
    raw_conditions = raw_data['conditions'] # {'conditions': []}
    filter_list = []
    for condition in raw_conditions: # {'name': string, 'threshold': float, 'operator': string, 'period': ?int}
        data = {
            'name': condition['name'],
            'threshold': float(condition['threshold']),
            'operator': 1 if condition['operator'] == 'gt' else -1, # maybe change in future, if there is any other compare condition
            'period': 3 if 'period' not in condition else int(condition['period'])
        }
        filter_list.append(data)
    print(filter_list)
    return start_date, filter_list
