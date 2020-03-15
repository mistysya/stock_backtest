import datetime
import pickle
import os

import pandas as pd
import numpy as np

class Data():
    def __init__(self, pickle_filename='stock_data.pickle'):
        self.module_path = os.path.abspath(os.path.dirname(__file__))
        self.data = {} # key: column name, value: time series data
        self.pickle_filename = pickle_filename

    def save_data(self):
        file_path = os.path.join(self.module_path, self.pickle_filename)
        print("Save data as pickle file:", file_path)
        with open(file_path, 'wb') as f:
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Save data finish!")

    def load_data_from_pickle(self):
        file_path = os.path.join(self.module_path, self.pickle_filename)
        print("Load data from pickle file:", file_path)
        with open(file_path, 'rb') as handle:
            self.data = pickle.load(handle, encoding='UTF-8')
        print("Load data finish!")

    def load_data_from_csv(self, year_period=1):
        print("Loading data from csv file...")
        print("Loading daily stock data")
        self.daily_data = self.load_daily_data('stock', year_period)
        print("Loading daily indicator")
        self.daily_indicator_data = self.load_daily_data('daily_indicator', year_period)
        print("Loading monthly data")
        self.monthly_data = self.load_montly_data(year_period)
        print("Combine data")
        self.combine_data()
        print("Load data finish!")

    def get_data(self):
        return self.data

    def combine_data(self):
        # key:data type -> time-series pandas data
        self.data['open'] = self.get_series_data(self.daily_data, '開盤價')
        self.data['close'] = self.get_series_data(self.daily_data, '收盤價')
        self.data['high'] = self.get_series_data(self.daily_data, '最高價')
        self.data['low'] = self.get_series_data(self.daily_data, '最低價')
        self.data['volume'] = self.get_series_data(self.daily_data, '成交股數')

        self.data['PE'] = self.get_series_data(self.daily_indicator_data, '本益比') # Price / Earning ratio
        self.data['PB'] = self.get_series_data(self.daily_indicator_data, '股價淨值比') # Price / Book ratio
        self.data['dividend'] = self.get_series_data(self.daily_indicator_data, '殖利率(%)') # Price / Book ratio

        self.data['month'] = self.get_series_data(self.monthly_data, '當月營收')
        self.data['5ma'] = self.data['close'].rolling(5, min_periods=1).mean()
        self.data['20ma'] = self.data['close'].rolling(20, min_periods=1).mean()
        self.data['60ma'] = self.data['close'].rolling(60, min_periods=1).mean()
        self.data['120ma'] = self.data['close'].rolling(120, min_periods=1).mean()

    def get_series_data(self, raw_data, column_name):
        data = pd.DataFrame({k:d[column_name] for k,d in raw_data.items()}).transpose()
        data.index = pd.to_datetime(data.index)
        data = data.apply(pd.to_numeric, errors='coerce', axis=0)
        return data

    def load_daily_data(self, data_type, year_period, end_date=None):
        start_date = self.date_calculate(datetime.date.today(), years=year_period).date()
        if(end_date):
            start_date = self.date_calculate(start_date, years=year_period).date()
        else:
            end_date = datetime.date.today()

        data = {}
        date = start_date
        n_days = (end_date - start_date).days
        directory_path = os.path.join(self.module_path, data_type)
        for _ in range(0, n_days):
            try:
                csv_path = os.path.join(directory_path, date.strftime('%Y%m%d') + '.csv')
                data[date] = pd.read_csv(csv_path).set_index('證券代號')
            except FileNotFoundError:
                pass
            date += datetime.timedelta(days=1)
        return data

    def load_montly_data(self, year_period, end_date=None):
        if(end_date is None):
            end_date = datetime.date.today()
        end_year = int(end_date.strftime('%Y'))
        month = int(end_date.strftime('%m'))
        year = end_year - year_period
        total_month = year_period * 12
        data = {}
        directory_path = os.path.join(self.module_path, 'month')
        for _ in range(0, total_month):
            date = datetime.datetime.strptime("{0}-{1}-01".format(str(year), str(month)), "%Y-%m-%d").date()
            try:
                csv_path = os.path.join(directory_path, date.strftime('%Y%m') + '.csv')
                data[date] = pd.read_csv(csv_path).set_index('公司代號')
            except FileNotFoundError:
                pass
            month += 1
            if(month > 12):
                month = 1
                year += 1
        return data

    def date_calculate(self, current_date, years=None, monthes=None):
        target_date = None
        if(years):
            current_year = int(current_date.strftime('%Y'))
            target_year = current_year - years
            target_date = str(target_year) + '-' + current_date.strftime('%m-%d')
            target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d')
        return target_date

f = Data()
f.load_data_from_pickle()
print(f.get_data()['PB'])
print(f.get_data()['PE'])
