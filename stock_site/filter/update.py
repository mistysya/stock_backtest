import os
import csv
import glob
import datetime

from .models import StockInfo, StockDailyInfo, StockMonthInfo, StockSeasonInfo
#from filter import models

def get_stock_data(date):
    directory_path = os.path.join('..', 'stock')
    filename = date + '.csv'
    rows = []
    with open(os.path.join(directory_path, filename), newline='', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            rows.append(row)
    return rows[1:]

def get_indicator_data(date):
    directory_path = os.path.join('..', 'daily_indicator')
    filename = date + '.csv'
    rows = []
    with open(os.path.join(directory_path, filename), newline='', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            rows.append(row)
    return rows[1:]

def get_investor_data(date):
    directory_path = os.path.join('..', 'daily_investor')
    filename = date + '.csv'
    rows = []
    with open(os.path.join(directory_path, filename), newline='', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            rows.append(row)
    return rows[1:]

def get_ma_data(date, day_num, close):
    start_date = date - datetime.timedelta(days=day_num-1)
    stock_data = StockDailyInfo.objects.filter(exchange_date__gte=start_date, exchange_date__lt=date)
    keys = close.keys()
    ma_list = {k:v for k, v in close.items()}

    for data in stock_data:
        if data.stock_symbol in keys:
            if data.close_price is not None:
                ma_list[data.stock_symbol].append(data.close_price)
    rows = []
    for k, v in ma_list.items():
        ma_value = 0
        for c in v:
            if c is not None:
                ma_value += c
        ma_value = ma_value / len(v)
        row = [k, ma_value]
        rows.append(row)
    return rows

def combine_daily_data(date):
    date_str = date.strftime("%Y%m%d")
    stock_data = get_stock_data(date_str)
    indicator_data = get_indicator_data(date_str)
    investor_data = get_investor_data(date_str)
    data = {}
    close = {}
    for row in stock_data:
        symbol = row[0]
        row[2] = int(row[2]) if row[2] != '--' else None
        row[5] = float(row[5]) if row[5] != '--' else None
        row[6] = float(row[6]) if row[6] != '--' else None
        row[7] = float(row[7]) if row[7] != '--' else None
        row[8] = float(row[8]) if row[8] != '--' else None
        close[symbol] = [row[8]]
        # volume, open, close, high, low
        data[symbol] = [symbol, date, row[2], row[5], row[6], row[7], row[8]]

    for row in indicator_data:
        symbol = row[0]
        if symbol in data.keys():
            row[2] = float(row[2]) if row[2] != '-' else None
            row[3] = float(row[3]) if row[3] != '-' else None
            row[4] = float(row[4]) if row[4] != '-' else None
            indicator_list = [row[2], row[3], row[4]]
            # pe, pb, dividend
            data[symbol] = data[symbol] + indicator_list
    for k, v in data.items():
        if len(v) < 10:
            investor_list = [None, None, None, None]
            data[k] = data[k] + investor_list

    for row in investor_data:
        symbol = row[0]
        if symbol in data.keys():
            # foreign_invest, invest_trust, dealer, investors(three)
            investor_list = [int(row[4]), int(row[7]), int(row[8]), int(row[15])]
            data[symbol] = data[symbol] + investor_list
    for k, v in data.items():
        if len(v) < 14:
            investor_list = [None, None, None, None]
            data[k] = data[k] + investor_list

    ma5_data = get_ma_data(date, 5, close)
    ma10_data = get_ma_data(date, 10, close)
    ma20_data = get_ma_data(date, 20, close)
    ma60_data = get_ma_data(date, 60, close)
    ma120_data = get_ma_data(date, 120, close)
    for row in ma5_data:
        symbol = row[0]
        data[symbol].append(row[1])

    for row in ma10_data:
        symbol = row[0]
        data[symbol].append(row[1])

    for row in ma20_data:
        symbol = row[0]
        data[symbol].append(row[1])

    for row in ma60_data:
        symbol = row[0]
        data[symbol].append(row[1])
    
    for row in ma120_data:
        symbol = row[0]
        data[symbol].append(row[1])
    return data

def convertToDailyInfoFormat(data):
    instances = []
    for r in list(data.values()):
        print(r)
        instance = StockDailyInfo(stock_symbol=r[0], exchange_date=r[1],
                                  volume=r[2], open_price=r[3], close_price=r[4], high_price=r[5], low_price=r[6],
                                  pe=r[7], pb=r[8], dividend=r[9],
                                  foreign_invest=r[10], invest_trust=r[11], dealer=r[12], investors=r[13],
                                  ma5=r[14], ma10=r[15], ma20=r[16], ma60=r[17], ma120=r[18])
        instances.append(instance)
    return instances

def insert_daily_info(date_str):
    date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    #date = datetime.date.today().strftime("%Y%m%d")

    #date = datetime.date(2012, 5, 2)
    data = combine_daily_data(date)
    instances = convertToDailyInfoFormat(data)
    StockDailyInfo.objects.bulk_create(instances)

def insert_daily_info_from_directory(start_date):
    directory_path = os.path.join('..', 'daily_investor')
    date_list = [file_name.split('\\')[-1].split('.')[0] for file_name in glob.glob(directory_path + '/*.csv')]
    start_index = date_list.index(start_date)
    print(start_index)
    for date in date_list[start_index:]:
        insert_daily_info(date)

def get_stock_info(start_date):
    directory_path = os.path.join('..', 'daily_investor')
    date_list = [file_name.split('\\')[-1].split('.')[0] for file_name in glob.glob(directory_path + '/*.csv')]
    start_index = date_list.index(start_date)

    stock_symbol_dict = {}
    for date in date_list[start_index:]:
        stock_data = get_stock_data(date)
        for row in stock_data:
            stock_symbol = row[0]
            stock_name = row[1]
            stock_symbol_dict[stock_symbol] = stock_name

        investor_data = get_investor_data(date)
        for row in investor_data:
            stock_symbol = row[0]
            stock_name = row[1]
            stock_symbol_dict[stock_symbol] = stock_name
    return stock_symbol_dict

def insert_stock_info(start_date):
    stock_symbol_dict = get_stock_info(start_date)
    instances = []
    for k, v in stock_symbol_dict.items():
        print(v)
        instance = StockInfo(stock_symbol=k, stock_name=v)
        instances.append(instance)
    StockInfo.objects.bulk_create(instances)

def get_month_data(date):
    directory_path = os.path.join('..', 'month')
    filename = date + '.csv'
    rows = []
    with open(os.path.join(directory_path, filename), newline='', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            rows.append(row)
    return rows[1:]

def insert_month_info(date_str):
    date = datetime.datetime.strptime(date_str + '01', "%Y%m%d").date()
    data = get_month_data(date_str)
    instances = []
    for row in data:
        instance = StockMonthInfo(stock_symbol=row[0], exchange_date=date, revenue=row[2])
        instances.append(instance)
    StockMonthInfo.objects.bulk_create(instances)

def insert_month_info_from_directory(start_date):
    directory_path = os.path.join('..', 'month')
    date_list = [file_name.split('\\')[-1].split('.')[0] for file_name in glob.glob(directory_path + '/*.csv')]
    start_index = date_list.index(start_date)
    print(start_index)
    for date in date_list[start_index:]:
        insert_month_info(date)
