import datetime
import math

import numpy as np
import pandas as pd

class Filter():
    def __init__(self, stock_data):
        self.stock_data = stock_data
        #self.strategy_list = []
        #self.constraint = []
        self.condition_dict = {}
        self.set_dict_to_func()
        self.load_strategy_data()

    def set_dict_to_func(self):
        self.condition_dict = {
            'dropdown': self.dropdown,
            'profit': self.profit,
            'std': self.std,
            'close': self.close,
            'volume': self.volume,
            'ma5': self.ma5,
            'ma20': self.ma20,
            'ma60': self.ma60,
            'ma120': self.ma120,
            'pe': self.pe,
            'pb': self.pb,
            'dividend': self.dividend,
            'than60ma': self.than60ma,
            'than120ma': self.than120ma,
            'than_month': self.than_month,
            'than_volume': self.than_volume
        }

    def load_strategy_data(self, strategy_filepath=""):
        # json file loading
        # create test data
        strategy_list = []
        a = {
            'name': 'dropdown',
            'period': 365 * 3,
            'threshold': 50,
            'operator': -1
        }
        strategy_list.append(a)
        return strategy_list

    def combine_constraint(self, start_date, filter_list):
        constraint_list = []
        for strategy in filter_list:
            res = self.condition_dict[strategy['name']](start_date, strategy['period'], strategy['threshold'], strategy['operator'])
            constraint_list.append(res)

        constraint = constraint_list[0]
        for i in range(1, len(constraint_list)):
            constraint = constraint & constraint_list[i]
        return constraint

    '''
    #def get_constraint(self, start_date):
    #    self.combine_constraint(start_date)
    #    return self.constraint
    '''

    def convertToJsonFormat(self, filter_stocks):
        close = self.stock_data['close'].iloc[-1]
        volume = self.stock_data['volume'].iloc[-1]
        ma5 = self.stock_data['5ma'].iloc[-1]
        ma20 = self.stock_data['20ma'].iloc[-1]
        ma60 = self.stock_data['60ma'].iloc[-1]
        ma120 = self.stock_data['120ma'].iloc[-1]
        pe = self.stock_data['PE'].iloc[-1]
        dividend = self.stock_data['dividend'].iloc[-1]
        pb = self.stock_data['PB'].iloc[-1]
        result = []
        for stock in filter_stocks:
            data = {}
            data['stock_id'] = stock
            data['last_close'] = close[stock]
            data['last_volume'] = volume[stock]
            data['5ma'] = ma5[stock]
            data['20ma'] = ma20[stock]
            data['60ma'] = ma60[stock]
            data['120ma'] = ma120[stock]
            #data['PE'] = pe[int(stock)]
            #data['dividend'] = dividend[int(stock)]
            #data['PB'] = pb[int(stock)]
            result.append(data)
        return result

    def get_result_web(self, start_date, filter_list):
        constraint = self.combine_constraint(start_date, filter_list)
        filter_stocks = constraint & self.stock_data['high'].columns
        result = self.convertToJsonFormat(filter_stocks)
        return result

    def get_result_backtest(self, start_date, strategy_filepath=""):
        strategy_list = self.load_strategy_data(strategy_filepath)
        constraint = self.combine_constraint(start_date, strategy_list)
        filter_stocks = constraint & self.stock_data['high'].columns
        return filter_stocks

    # --------------------- Conditions ---------------------

    def dropdown(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data.cummax() - data).max()/data.max() * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def profit(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data.iloc[-1] / data.iloc[0] - 1) * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def std(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data / data.shift()).std()
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def close(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def volume(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['volume'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma5(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['5ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma20(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['20ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma60(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['60ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma120(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['120ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def pb(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['PB'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index.astype(str)
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)

    def pe(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['PE'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index.astype(str)
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)

    def dividend(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['dividend'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index.astype(str)
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)
    
    def than60ma(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        close = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        ma60 = self.stock_data['60ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        close = close.iloc[-1]
        ma60 = ma60.iloc[-1]
        if operator < 0:
            res = np.where(close < ma60, True, False)
        else:
            res = np.where(close > ma60, True, False)
        result = pd.Series(res, index=close.index)
        return result[result == True].index.astype(str)

    def than120ma(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        close = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        ma120 = self.stock_data['120ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        close = close.iloc[-1]
        ma120 = ma120.iloc[-1]
        if operator < 0:
            res = np.where(close < ma120, True, False)
        else:
            res = np.where(close > ma120, True, False)
        result = pd.Series(res, index=close.index)
        return result[result == True].index.astype(str)

    def than_month(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(600)
        month = self.stock_data['month'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        if len(month.index) <= 2 or len(month.index) <= threshold + 1:
            cur_month = month.iloc[-1]
            prev_month = month.iloc[-1]
        else:
            cur_month = month.iloc[-2]
            prev_month = month.iloc[-(threshold+1)]
        if operator < 0:
            res = np.where(cur_month < prev_month, True, False)
        else:
            res = np.where(cur_month > prev_month, True, False)
        result = pd.Series(res, index=cur_month.index)
        return result[result == True].index.astype(str)

    def than_volume(self, start_date, period, threshold, operator):
        prev_date = start_date - datetime.timedelta(period)
        volume = self.stock_data['volume'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))

        result = ((volume.iloc[-1] - volume.iloc[-2]) / volume.iloc[-2]) * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

