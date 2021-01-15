import datetime

import numpy as np
import pandas as pd
#from .models import StockInfo, StockDailyInfo, StockMonthInfo, StockSeasonInfo

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
            'dealerNBSDays': self.dealer_nbs_days,
            'investTrustNBSDays': self.invest_trust_nbs_days,
            'foreignInvestNBSDays': self.foreign_invest_nbs_days,
            'threeInvestorNBSDays': self.three_investor_nbs_days,
            'dealerNBSThanMonthlyAvg': self.dealer_nbs_than_monthly_avg,
            'investTrustNBSThanMonthlyAvg': self.invest_trust_nbs_than_monthly_avg,
            'foreignInvestNBSThanMonthlyAvg': self.foreign_invest_nbs_than_monthly_avg,
            'threeInvestorNBSThanMonthlyAvg': self.three_investor_nbs_than_monthly_avg,
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
    
    def get_index_from_date(self, target_date, dataframe_index):
        tmp_date = target_date
        while tmp_date.strftime('%Y-%m-%d') not in dataframe_index:
            tmp_date -= datetime.timedelta(days=1)
        idx = dataframe_index.get_loc(tmp_date.strftime('%Y-%m-%d')) # must exactly match
        return idx

    def combine_constraint(self, start_date, filter_list):
        constraint_list = []
        for strategy in filter_list:
            res = self.condition_dict[strategy['name']](start_date, strategy['period'], strategy['threshold'], strategy['operator'])
            constraint_list.append(res)

        constraint = constraint_list[0]
        for i in range(1, len(constraint_list)):
            constraint = constraint & constraint_list[i]
        return constraint

    def convertToJsonFormat(self, filter_stocks):
        close = self.stock_data['close'].iloc[-1]
        volume = self.stock_data['volume'].iloc[-1]
        ma5 = self.stock_data['5ma'].iloc[-1]
        InvestTrustNBS = self.stock_data['InvestTrustNBS'].iloc[-1]
        ForeignInvestNBS = self.stock_data['ForeignInvestNBS'].iloc[-1]
        ThreeInvestorNBS = self.stock_data['ThreeInvestorNBS'].iloc[-1]
        result = []
        for stock in filter_stocks:
            data = {}
            data['stock_id'] = stock
            data['last_close'] = close[stock] if not pd.isnull(close[stock]) else None
            data['last_volume'] = volume[stock] if not pd.isnull(volume[stock]) else None
            data['5ma'] = ma5[stock] if not pd.isnull(ma5[stock]) else None
            data['InvestTrustNBS'] = InvestTrustNBS[stock] if not pd.isnull(InvestTrustNBS[stock]) else None
            data['ForeignInvestNBS'] = ForeignInvestNBS[stock] if not pd.isnull(ForeignInvestNBS[stock]) else None
            data['ThreeInvestorNBS'] = ThreeInvestorNBS[stock] if not pd.isnull(ThreeInvestorNBS[stock]) else None
            result.append(data)
        return result

    def get_result_web(self, start_date, filter_list):
        constraint = self.combine_constraint(start_date, filter_list)
        filter_stocks = constraint & self.stock_data['high'].columns
        result = self.convertToJsonFormat(filter_stocks)
        return result


# 昨日 收盤價 大於 價格
# 昨日 交易量 大於 張數
# 昨日 N日平均線 大於 收盤價
# 昨日 PE 大於 數值
# 昨日 PB 大於 數值
# 昨日 殖利率 大於 數值
# N日 法人 大於 張數

# N月 月營收 創新高
# N月 月營收 連續成長

    # --------------------- Conditions ---------------------

    def dropdown(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data.cummax() - data).max()/data.max() * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def profit(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data.iloc[-1] / data.iloc[0] - 1) * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def std(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = (data / data.shift()).std()
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def close(self, start_date, period, threshold, operator): # 大/小於前 N 日收盤價
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def volume(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['volume'].index)
        data = self.stock_data['volume'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['volume'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma5(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['5ma'].index)
        data = self.stock_data['5ma'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_ma = data.iloc[-1]
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_close = data.iloc[-1]
        '''
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['5ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_ma = data.iloc[-1]
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_close = data.iloc[-1]
        '''
        result = (result_close / result_ma - 1) * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma20(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['20ma'].index)
        data = self.stock_data['20ma'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_ma = data.iloc[-1]
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_close = data.iloc[-1]
        '''
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['20ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_ma = data.iloc[-1]
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_close = data.iloc[-1]
        '''
        result = (result_close / result_ma - 1) * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma60(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['60ma'].index)
        data = self.stock_data['60ma'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_ma = data.iloc[-1]
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_close = data.iloc[-1]
        '''
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['60ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_ma = data.iloc[-1]
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_close = data.iloc[-1]
        '''
        result = (result_close / result_ma - 1) * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def ma120(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['120ma'].index)
        data = self.stock_data['120ma'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_ma = data.iloc[-1]
        idx = self.get_index_from_date(start_date, self.stock_data['close'].index)
        data = self.stock_data['close'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        result_close = data.iloc[-1]
        '''
        prev_date = start_date - datetime.timedelta(period)
        data = self.stock_data['120ma'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_ma = data.iloc[-1]
        data = self.stock_data['close'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result_close = data.iloc[-1]
        '''
        result = (result_close / result_ma - 1) * 100
        if operator < 0:
            return result[result < threshold].index
        elif operator == 0:
            return result[result == threshold].index
        else:
            return result[result > threshold].index

    def pb(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['PB'].index)
        data = self.stock_data['PB'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['PB'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index.astype(str)
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)

    def pe(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['PE'].index)
        data = self.stock_data['PE'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['PE'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index.astype(str)
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)

    def dividend(self, start_date, period, threshold, operator):
        idx = self.get_index_from_date(start_date, self.stock_data['dividend'].index)
        data = self.stock_data['dividend'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        #prev_date = start_date - datetime.timedelta(period)
        #data = self.stock_data['dividend'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        result = data.iloc[-1]
        if operator < 0:
            return result[result < threshold].index.astype(str)
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            return result[result > threshold].index.astype(str)

    def dealer_nbs_days(self, start_date, period, threshold, operator): # 自營商買賣超 N 日
        idx = self.get_index_from_date(start_date, self.stock_data['DealerNBS'].index)
        data = self.stock_data['DealerNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        stocks_list = []
        for i in range(0, period):
            stocks = data.iloc[i]
            if operator < 0:
                res = stocks[stocks < threshold].index.astype(str)
            elif operator == 0:
                res = stocks[stocks == threshold].index.astype(str)
            else:
                res = stocks[stocks > threshold].index.astype(str)
            stocks_list.append(res)
        result = stocks_list[0]
        for i in range(1, len(stocks_list)):
            result = result & stocks_list[i]
        return result

    def invest_trust_nbs_days(self, start_date, period, threshold, operator): # 投信買賣超 N 日
        idx = self.get_index_from_date(start_date, self.stock_data['InvestTrustNBS'].index)
        data = self.stock_data['InvestTrustNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        stocks_list = []
        for i in range(0, period):
            stocks = data.iloc[i]
            if operator < 0:
                res = stocks[stocks < threshold].index.astype(str)
            elif operator == 0:
                res = stocks[stocks == threshold].index.astype(str)
            else:
                res = stocks[stocks > threshold].index.astype(str)
            stocks_list.append(res)
        result = stocks_list[0]
        for i in range(1, len(stocks_list)):
            result = result & stocks_list[i]
        return result

    def foreign_invest_nbs_days(self, start_date, period, threshold, operator): # 外資買賣超 N 日
        idx = self.get_index_from_date(start_date, self.stock_data['ForeignInvestNBS'].index)
        data = self.stock_data['ForeignInvestNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        stocks_list = []
        for i in range(0, period):
            stocks = data.iloc[i]
            if operator < 0:
                res = stocks[stocks < threshold].index.astype(str)
            elif operator == 0:
                res = stocks[stocks == threshold].index.astype(str)
            else:
                res = stocks[stocks > threshold].index.astype(str)
            stocks_list.append(res)
        result = stocks_list[0]
        for i in range(1, len(stocks_list)):
            result = result & stocks_list[i]
        return result

    def three_investor_nbs_days(self, start_date, period, threshold, operator): # 三大法人買賣超 N 日
        idx = self.get_index_from_date(start_date, self.stock_data['ThreeInvestorNBS'].index)
        data = self.stock_data['ThreeInvestorNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        stocks_list = []
        for i in range(0, period):
            stocks = data.iloc[i]
            if operator < 0:
                res = stocks[stocks < threshold].index.astype(str)
            elif operator == 0:
                res = stocks[stocks == threshold].index.astype(str)
            else:
                res = stocks[stocks > threshold].index.astype(str)
            stocks_list.append(res)
        result = stocks_list[0]
        for i in range(1, len(stocks_list)):
            result = result & stocks_list[i]
        return result

    def dealer_nbs_than_monthly_avg(self, start_date, period, threshold, operator): # 自營商 N 日內買賣超大於月平均 M 倍 (period, threshold)
        idx = self.get_index_from_date(start_date, self.stock_data['DealerNBS'].index)
        data = self.stock_data['DealerNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        ndays_mean_value = data.mean(axis=0)
        prev_date = start_date - datetime.timedelta(days=30)
        data = self.stock_data['DealerNBS'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        month_mean_value = data.mean(axis=0)

        result = (ndays_mean_value / month_mean_value)
        if operator < 0:
            month = month_mean_value[month_mean_value < 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value < 0].index.astype(str)
            result = result[result > threshold].index.astype(str) # minus / minus = plus  -3/-1 = 3 > 2
            result = result & month
            result = result & ndays
            return result
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            month = month_mean_value[month_mean_value > 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value > 0].index.astype(str)
            result = result[result > threshold].index.astype(str)
            result = result & month
            result = result & ndays
            return result

    def invest_trust_nbs_than_monthly_avg(self, start_date, period, threshold, operator): # 投信 N 日內買賣超大於月平均 M 倍 (period, threshold)
        idx = self.get_index_from_date(start_date, self.stock_data['InvestTrustNBS'].index)
        data = self.stock_data['InvestTrustNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        ndays_mean_value = data.mean(axis=0)
        prev_date = start_date - datetime.timedelta(days=30)
        data = self.stock_data['InvestTrustNBS'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        month_mean_value = data.mean(axis=0)

        result = (ndays_mean_value / month_mean_value)
        if operator < 0:
            month = month_mean_value[month_mean_value < 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value < 0].index.astype(str)
            result = result[result > threshold].index.astype(str) # minus / minus = plus  -3/-1 = 3 > 2
            result = result & month
            result = result & ndays
            return result
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            month = month_mean_value[month_mean_value > 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value > 0].index.astype(str)
            result = result[result > threshold].index.astype(str)
            result = result & month
            result = result & ndays
            return result

    def foreign_invest_nbs_than_monthly_avg(self, start_date, period, threshold, operator): # 外資 N 日內買賣超大於月平均 M 倍 (period, threshold)
        idx = self.get_index_from_date(start_date, self.stock_data['ForeignInvestNBS'].index)
        data = self.stock_data['ForeignInvestNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        ndays_mean_value = data.mean(axis=0)
        prev_date = start_date - datetime.timedelta(days=30)
        data = self.stock_data['ForeignInvestNBS'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        month_mean_value = data.mean(axis=0)

        result = (ndays_mean_value / month_mean_value)
        if operator < 0:
            month = month_mean_value[month_mean_value < 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value < 0].index.astype(str)
            result = result[result > threshold].index.astype(str) # minus / minus = plus  -3/-1 = 3 > 2
            result = result & month
            result = result & ndays
            return result
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            month = month_mean_value[month_mean_value > 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value > 0].index.astype(str)
            result = result[result > threshold].index.astype(str)
            result = result & month
            result = result & ndays
            return result

    def three_investor_nbs_than_monthly_avg(self, start_date, period, threshold, operator): # 三大法人 N 日內買賣超大於月平均 M 倍 (period, threshold)
        idx = self.get_index_from_date(start_date, self.stock_data['ThreeInvestorNBS'].index)
        data = self.stock_data['ThreeInvestorNBS'].iloc[idx - period + 1: idx + 1] # because idx is index, iloc[:] doesn't include tail but head
        ndays_mean_value = data.mean(axis=0)
        prev_date = start_date - datetime.timedelta(days=30)
        data = self.stock_data['ThreeInvestorNBS'].truncate(prev_date.strftime('%Y-%m-%d'), start_date.strftime('%Y-%m-%d'))
        month_mean_value = data.mean(axis=0)

        result = (ndays_mean_value / month_mean_value)
        if operator < 0:
            month = month_mean_value[month_mean_value < 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value < 0].index.astype(str)
            result = result[result > threshold].index.astype(str) # minus / minus = plus  -3/-1 = 3 > 2
            result = result & month
            result = result & ndays
            return result
        elif operator == 0:
            return result[result == threshold].index.astype(str)
        else:
            month = month_mean_value[month_mean_value > 0].index.astype(str)
            ndays = ndays_mean_value[ndays_mean_value > 0].index.astype(str)
            result = result[result > threshold].index.astype(str)
            result = result & month
            result = result & ndays
            return result

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

