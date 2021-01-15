import datetime
import json
import csv
import os

stock_name = {}
file_list = ['stock/20200909.csv', 'stock/20200908.csv', 'stock/20200817.csv',
             'daily_indicator/20200902.csv', 'daily_indicator/20200903.csv', 'daily_indicator/20200826.csv',
             'daily_investor/20200907.csv', 'daily_investor/20200901.csv', 'daily_investor/20200814.csv']
for file_name in file_list:
    with open(file_name, newline='', encoding = "UTF-8") as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        ignore_first_line = False
        # 以迴圈輸出每一列
        for row in rows:
            if ignore_first_line:
                stock_name[row[0]] = row[1]
            else:
                ignore_first_line = True

with open("stock_name.json", "w") as outfile:
    print(stock_name)
    print(len(stock_name.keys()))
    json.dump(stock_name, outfile)
