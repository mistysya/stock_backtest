import datetime
import math
import matplotlib

import numpy as np
import pandas as pd

from data import Data
from strategy import Strategy

class Backtest():
    def __init__(self, stock_data, strategy, origin_cash, hold_period, ideal_test, start_date, end_date):
        #self.stock_data = Data().get_data()
        #self.strategy = Strategy(self.stock_data)
        self.stock_data = stock_data.get_data()
        self.strategy = strategy
        self.origin_cash = origin_cash
        self.hold_period = hold_period
        self.ideal_test = ideal_test
        self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        self.return_rate = []
        self.time_index = []
        self.return_pd = pd.Series()
        self.cash = origin_cash

    def run(self):
        end_date = self.end_date
        start_date = self.start_date
        period_close = self.stock_data['close'].truncate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) # get all time index
        self.time_index = period_close.index
        while((end_date - start_date).days > 0):
            next_date = start_date + datetime.timedelta(self.hold_period)
            print("================================================")
            print("\n開始日期: {0} \n結束日期: {1}".format(start_date, next_date))
            period_high = self.stock_data['high'].truncate(start_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
            period_low = self.stock_data['low'].truncate(start_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
            select_stocks = self.get_select_stocks(period_high, start_date)
            init_price = period_high[select_stocks].iloc[0]
            final_price = list(period_low[select_stocks].iloc[-1])
            # num_stocks = len(select_stocks)

            stocks_unit = self.loop_init(init_price)
            last_price = self.loop_run(period_low[select_stocks], init_price, stocks_unit)
            self.loop_end(final_price, last_price, stocks_unit)

            start_date = next_date
        print("Finish")
        print("Fianl return rate:", self.return_rate[-1])

    def loop_init(self, init_price):
        print("Current cash:", self.cash)
        # select stocks which would be baught
        # need better algorithm
        num_stocks = len(init_price)
        if num_stocks > 0:
            each_stock = [(self.cash / num_stocks)] * num_stocks
        stocks_unit = []
        for i in range(0, num_stocks):
            if(self.ideal_test == True):
                number = each_stock[i] / (init_price[i]) # need better algorithm
                stocks_unit.append(number)
                self.cash -= each_stock[i]
            else:
                number = int(each_stock[i] // (init_price[i])) # need better algorithm
                stocks_unit.append(number)
                self.cash -= init_price[i] * number * (1 + 0.1425 * 0.01 * 0.6)
        print("Buy {0} sotcks.\n".format(len([i for i in stocks_unit if i > 0])))
        return stocks_unit

    def loop_run(self, period_low, init_price, stocks_unit):
        last_price = init_price
        deal_days = len(period_low.index)
        return_rate = [0] * deal_days

        cur_value = 0
        for i in range(0, len(stocks_unit)):
            cur_value += init_price[i] * stocks_unit[i]
        return_rate[0] = (self.cash + cur_value) / self.origin_cash

        for i in range(1, deal_days):
            cur_price = list(period_low.iloc[i])
            cur_value = 0
            for j in range(0, len(cur_price)):
                if math.isnan(cur_price[j]):
                    cur_value += last_price[j] * stocks_unit[j]
                else:
                    cur_value += cur_price[j] * stocks_unit[j]
                    last_price[j] = cur_price[j]
            return_rate[i] = (self.cash + cur_value) / self.origin_cash
        print("Return rate:", return_rate[-1])
        self.return_rate = self.return_rate + return_rate
        self.return_pd = pd.concat([self.return_pd, pd.Series(return_rate, index = period_low.index)], axis=0)
        return last_price

    def loop_end(self, final_price, last_price, stocks_unit):
        final_value = 0
        for i in range(0, len(final_price)):
            if math.isnan(final_price[i]):
                final_price[i] = last_price[i]
            if self.ideal_test == True:
                final_value += final_price[i] * stocks_unit[i]
            else:
                final_value += final_price[i] * stocks_unit[i] * (1 - 0.1425 * 0.01 * 0.6 - 0.3 * 0.01)
        self.cash += final_value
        print("Final cash:", self.cash)

    def get_select_stocks(self, period_high, start_date):
        constraint = self.strategy.get_constraint(start_date)
        select_stocks = constraint & period_high.columns
        select_stocks = [s for s in select_stocks if not math.isnan(period_high[s].iloc[0])]
        print(len(constraint))
        #if len(constraint) < 50:
        #    select_stocks = []
        #select_stocks = [s for s in select_stocks if not math.isnan(period_high[s].iloc[0]) and not np.isnan(period_high[s].iloc[0])]
        print("Select {0} stocks".format(len(select_stocks)))
        return select_stocks

    def draw_plot(self, line_color='red'):
        self.return_pd.plot(color=line_color)

print("Prepare stock data...")
stock_data = Data()
#stock_data.load_data_from_csv(year_period=6)
stock_data.load_data_from_pickle()
print("Prepare strategy...")
strategy = Strategy(stock_data.get_data())
cash = 2000000 / 1000
period = 60
print("Prepare backtest...")
backtest = Backtest(stock_data, strategy, cash, period, False, '2006-10-2', '2020-3-13')
print("Run...")
backtest.run()
backtest.draw_plot(line_color='red')
backtest2 = Backtest(stock_data, strategy, cash, period, True, '2006-10-2', '2020-3-13')
print("Run...")
backtest2.run()
backtest2.draw_plot(line_color='blue')
matplotlib.pyplot.show()
