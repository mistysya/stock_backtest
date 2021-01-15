import datetime
import math

import numpy as np
import pandas as pd

class Strategy():
    def __init__(self, sotck_data):
        self.stock_data = sotck_data
        self.strategy_list = []
        self.constraint = []
        self.call_dict = {}
        self.set_func_dict()
        self.load_strategy_data()
    
    def set_func_dict(self):
        self.call_dict = {
            'dropdown': self.dropdown,
            'profit': self.profit,
            'std': self.std,
            'ma20': self.ma20,
            'pe': self.pe,
            'pb': self.pb,
            'dividend': self.dividend,
            'than60ma': self.than60ma,
            'than120ma': self.than120ma,
            'than_month': self.than_month,
            'than_volume': self.than_volume
        }

    def load_strategy_data(self):
        # json file loading
        # create test data
        self.strategy_list = []
        a = {
            'name': 'dropdown',
            'period': 365 * 3,
            'threshold': 50,
            'operation': -1
        }
        b = {
            'name': 'profit',
            'period': 365 * 3,
            'threshold': 10,
            'operation': 1
        }
        c = {
            'name': 'std',
            'period': 365 * 3,
            'threshold': 0.02,
            'operation': -1
        }
        d = {
            'name': 'ma20',
            'period': 15,
            'threshold': 100,
            'operation': -1
        }
        e = {
            'name': 'ma20',
            'period': 15,
            'threshold': 10,
            'operation': 1
        }
        f = {
            'name': 'pb',
            'period': 15,
            'threshold': 2,
            'operation': -1
        }
        g = {
            'name': 'pe',
            'period': 15,
            'threshold': 15,
            'operation': -1
        }
        h = {
            'name': 'pe',
            'period': 15,
            'threshold': 10,
            'operation': 1
        }
        i = {
            'name': 'than60ma',
            'period': 15,
            'threshold': 0,
            'operation': 1
        }
        j = {
            'name': 'than120ma',
            'period': 15,
            'threshold': 0,
            'operation': 1
        }
        k = {
            'name': 'dividend',
            'period': 15,
            'threshold': 4,
            'operation': 1
        }
        l = {
            'name': 'than_month',
            'period': 15,
            'threshold': 12,
            'operation': 1
        }
        m = {
            'name': 'than_volume',
            'period': 15,
            'threshold': 50,
            'operation': 1
        }
        
        #self.strategy_list.append(a)
        #self.strategy_list.append(b)
        #self.strategy_list.append(c)
        #self.strategy_list.append(d)
        #self.strategy_list.append(e)
        self.strategy_list.append(f)
        self.strategy_list.append(g)
        #self.strategy_list.append(h)
        self.strategy_list.append(i)
        self.strategy_list.append(j)
        self.strategy_list.append(k)
        self.strategy_list.append(l)
        self.strategy_list.append(m)

    def combine_constraint(self, start_date):
        constraint_list = []
        for strategy in self.strategy_list:
            res = self.call_dict[strategy['name']](start_date, strategy['period'], strategy['threshold'], strategy['operation'])
            constraint_list.append(res)
        self.constraint = constraint_list[0]
        for i in range(1, len(constraint_list)):
            self.constraint = self.constraint & constraint_list[i]

    def get_constraint(self, start_date):
        self.combine_constraint(start_date)
        return self.constraint

    def dropdown(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data.cummax() - data).max()/data.max() * 100
        if operation < 0:
            return result[result < threshold].index
        elif operation == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def profit(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data.iloc[-1] / data.iloc[0] - 1) * 100
        if operation < 0:
            return result[result < threshold].index
        elif operation == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def std(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data / data.shift()).std()
        if operation < 0:
            return result[result < threshold].index
        elif operation == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma20(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['20ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operation < 0:
            return result[result < threshold].index
        elif operation == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def pb(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['PB'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operation < 0:
            return result[result < threshold].index.astype(str)
        elif operation == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)

    def pe(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['PE'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operation < 0:
            return result[result < threshold].index.astype(str)
        elif operation == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)

    def dividend(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['dividend'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operation < 0:
            return result[result < threshold].index.astype(str)
        elif operation == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)
    
    def than60ma(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        close = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        ma60 = self.stock_data['60ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        close = close.iloc[-1]
        ma60 = ma60.iloc[-1]
        if operation < 0:
            res = np.where(close < ma60, True, False)
        else:
            res = np.where(close > ma60, True, False)
        result = pd.Series(res, index=close.index)
        return result[result == True].index.astype(str)

    def than120ma(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        close = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        ma120 = self.stock_data['120ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        close = close.iloc[-1]
        ma120 = ma120.iloc[-1]
        if operation < 0:
            res = np.where(close < ma120, True, False)
        else:
            res = np.where(close > ma120, True, False)
        result = pd.Series(res, index=close.index)
        return result[result == True].index.astype(str)

    def than_month(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(600)
        month = self.stock_data['month'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        if len(month.index) <= 2 or len(month.index) <= threshold + 1:
            cur_month = month.iloc[-1]
            prev_month = month.iloc[-1]
        else:
            cur_month = month.iloc[-2]
            prev_month = month.iloc[-(threshold+1)]
        if operation < 0:
            res = np.where(cur_month < prev_month, True, False)
        else:
            res = np.where(cur_month > prev_month, True, False)
        result = pd.Series(res, index=cur_month.index)
        return result[result == True].index.astype(str)

    def than_volume(self, start_date, period, threshold, operation):
        prev_date = start_date - datetime.timedelta(period)
        volume = self.stock_data['volume'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))

        result = ((volume.iloc[-1] - volume.iloc[-2]) / volume.iloc[-2]) * 100
        if operation < 0:
            return result[result < threshold].index
        elif operation == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

