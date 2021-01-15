import requests
import datetime
import time
import glob
import pandas as pd
import numpy as np
import csv
import os

def get_daily_data(date):
    url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + date + '&type=ALL'
    print(url)
    print("Download {0} data...".format(date))
    raw_data = ""
    raw_data = requests.post(url)
    print("Download {0} data finish.".format(date))
    stock_index_table = []
    etf_table = []
    stock_table = []
    etf_header = []
    stock_header = []
    for line in raw_data.text.split('\n'):
        line = line.replace('",', '|').replace('"', '').replace(',', '').split('|')
        if(len(line) == 7 and line[0] == "指數"):
            etf_header = line[:6]
        elif(len(line) == 7 and line[1] != "收盤指數"):
            etf_table.append(line[:6])
        elif(len(line) == 17 and line[0] == "證券代號"):
            stock_header = line[:16]
        elif(len(line) == 17 and line[0] != "證券代號"):
            if(line[0] == "(元,股)"):
                continue
            elif('=' in line[0]):
                line[0] = line[0].replace('=', '').replace('"', '')
                stock_index_table.append(line[:16])
            else:
                stock_table.append(line[:16])
        else:
            continue

    filename = date + '.csv'
    dirpath = os.path.abspath(os.path.dirname(__file__))
    etf_path = os.path.join(dirpath, 'etf')
    stock_index_path = os.path.join(dirpath, 'stock_index')
    stock_path = os.path.join(dirpath, 'stock')

    print("Write data into {0}".format(filename))
    if not stock_table:
        print("Empty table. Finish")
        return
    write_csv_file(etf_path, filename, etf_header, etf_table)
    write_csv_file(stock_index_path, filename, stock_header, stock_index_table)
    write_csv_file(stock_path, filename, stock_header, stock_table)
    print("Finish")

def get_daily_indicator(date):
    url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=' + date + '&selectType=ALL'
    print(url)
    print("Download {0} data...".format(date))
    raw_data = ""
    raw_data = requests.post(url)
    print("Download {0} data finish.".format(date))
    indicator_table = []
    indicator_header = []
    for line in raw_data.text.split('\n'):
        line = line.replace('",', '|').replace('"', '').replace(',', '').split('|')
        if(len(line) == 8):
            if(line[0] == '證券代號'):
                indicator_header = [line[0], line[1], line[4], line[2], line[5]]
            else:
                indicator_table.append([line[0], line[1], line[4], line[2], line[5]])
        elif(len(line) == 6):
            if(line[0] == '證券代號'):
                indicator_header = line[:5]
            else:
                indicator_table.append(line[:5])
        else:
            continue

    filename = date + '.csv'
    dirpath = os.path.abspath(os.path.dirname(__file__))
    indicator_path = os.path.join(dirpath, 'daily_indicator')

    print("Write data into {0}".format(filename))
    if not indicator_table:
        print("Empty table. Finish")
        return
    write_csv_file(indicator_path, filename, indicator_header, indicator_table)
    print("Finish")

def get_daily_investor(date):
    url = 'http://www.tse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999'
    print(url)
    print("Download {0} data...".format(date))
    raw_data = ""
    raw_data = requests.post(url)
    print("Download {0} data finish.".format(date))
    investor_table = []
    investor_header = []
    for line in raw_data.text.split('\n'):
        line = line.replace('",', '|').replace('"', '').replace(',', '').split('|')
        if (len(line) == 20):
            if(line[0] == '證券代號'):
                investor_header = [line[0], line[1].split()[0], "外資買進股數", "外資賣出股數", "外資買賣超股數", line[5],
                                   line[6], line[7], line[8],line[9], line[10], line[11], line[12], line[13], line[14],
                                   line[15], line[16], line[17], line[18]]
            else:
                investor_table.append([line[0], line[1].split()[0], line[2], line[3], line[4], line[5], line[6], line[7],
                                       line[8], line[9], line[10], line[11], line[12], line[13], line[14],
                                       line[15], line[16], line[17], line[18]])
        elif (len(line) == 17):
            if(line[0] == '證券代號'):
                investor_header = [line[0], line[1].split()[0], line[2], line[3], line[4],
                                   "外資自營商買進股數", "外資自營商賣出股數", "外資自營商買賣超股數", line[5],
                                   line[6], line[7], line[8], line[9], line[10], line[11],
                                   line[12], line[13], line[14], line[15]]
            else:
                investor_table.append([line[0], line[1].split()[0], line[2], line[3], line[4],
                                       "0", "0", "0", line[5],
                                       line[6], line[7], line[8], line[9], line[10], line[11],
                                       line[12], line[13], line[14], line[15]])
        elif (len(line) == 13):
            if(line[0] == '證券代號'):
                investor_header = [line[0], line[1].split()[0], line[2], line[3], line[4],
                                   "外資自營商買進股數", "外資自營商賣出股數", "外資自營商買賣超股數", line[5],
                                   line[6], line[7], line[8], "自營商買進股數(自行買賣)", "自營商賣出股數(自行買賣)",
                                   "自營商買賣超股數(自行買賣)", "自營商買進股數(避險)", "自營商賣出股數(避險)",
                                   "自營商買賣超股數(避險)", line[11]]
            else:
                investor_table.append([line[0], line[1].split()[0], line[2], line[3], line[4],
                                       "0", "0", "0", line[5],
                                       line[6], line[7], line[8], line[9], line[10],
                                       line[8], "0", "0",
                                       "0", line[11]])
        else:
            continue

    filename = date + '.csv'
    dirpath = os.path.abspath(os.path.dirname(__file__))
    indicator_path = os.path.join(dirpath, 'daily_investor')

    print("Write data into {0}".format(filename))
    if not investor_table:
        print("Empty table. Finish")
        return
    write_csv_file(indicator_path, filename, investor_header, investor_table)
    print("Finish")

def write_csv_file(path, filename, header, data):
    with open(os.path.join(path, filename), 'w', newline='', encoding = "UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        # 寫入二維表格
        writer.writerows(data)

def get_month_data(year, month):
    from io import StringIO
    filename = str(year) + str(month).zfill(2) + '.csv'
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911

    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'

    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # 下載該年月的網站，並用pandas轉換成 dataframe
    print("Download...")
    #html_df = pd.read_html(url)           

    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    print("Finish")

    html_df = pd.read_html(StringIO(r.text), encoding='big-5')
    # Step3. 篩選出個股月營收資訊

    # 3.1 剃除行數錯誤的表格,並將表格合併
    df = pd.concat([df for df in html_df if df.shape[1] == 11]) 
    # 3.2 設定表格的header
    try:
        df = df.drop(df.columns[10], axis = 1)
    except:
        print("There is not column 10")
    df.columns = df.columns.get_level_values(1)

    # 3.3 剃除重複的欄位
    df = df[df['公司代號'] != '合計']

    # 3.4 重新排序索引值
    df = df.set_index(['公司代號'])
    try:
        df = df.drop(['全部國內上市公司合計'], axis = 0)
    except:
        print("There is not 全部國內上市公司合計")
    print("Save...")

    dirpath = os.path.abspath(os.path.dirname(__file__))
    month_path = os.path.join(dirpath, 'month')
    month_path = os.path.join(month_path, filename)
    df.to_csv(month_path)
    print("Save Finish")
    # 偽停頓
    time.sleep(5)

def get_period_month_data(start_date, end_date):
    start_year = int(start_date[:4])
    start_month = int(start_date[4:])
    end_year = int(end_date[:4])
    end_month = int(end_date[4:])
    years = end_year - start_year
    total_month = years * 12
    print(total_month)
    if(end_month < start_month):
        total_month -= (start_month - end_month)
    else:
        total_month += (end_month - start_month)
    print(total_month)
    for _ in range(0, total_month):
        print(end_year, end_month)
        try:
            get_month_data(end_year, end_month)
        except Exception as e:
            print(e)
        end_month -= 1
        if(end_month == 0):
            end_month = 12
            end_year -= 1
        time.sleep(6)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def get_period_data(start_date, end_date, data_type=0):

    start = datetime.datetime.strptime(start_date, "%Y%m%d").date()
    end = datetime.datetime.strptime(end_date, "%Y%m%d").date()
    if (end < start):
        tmp = start
        start = end
        end = tmp

    for single_date in daterange(start, end):
        date = single_date.strftime("%Y%m%d")
        try:
            if(data_type == 1):
                get_daily_data(date)
            elif(data_type == 2):
                get_daily_indicator(date)
            elif(data_type == 3):
                get_daily_investor(date)
            else:
                None
        except Exception as e:
            print(e)
            print("Download {0} data fail! Abandon this date".format(date))
        time.sleep(5)

def get_today_data(data_type=0):
    date = datetime.date.today().strftime("%Y%m%d")
    if(data_type == 1):
        get_daily_data(date)
    elif(data_type == 2):
        get_daily_indicator(date)
    elif(data_type == 3):
        get_daily_investor(date)
    else:
        None

def convert_encode(src_dir, des_dir):
    file_list = [file_name.split('\\')[-1] for file_name in glob.glob(src_dir + '/*.csv')]
    cur_directory = os.getcwd()
    source_path = os.path.join(cur_directory, src_dir)
    destination_path = os.path.join(cur_directory, des_dir)
    for i in range(len(file_list)):
        with open(os.path.join(source_path, file_list[i]), "r", encoding = "Big5", errors='ignore') as inFile, open(os.path.join(destination_path, file_list[i]), "w", encoding = "UTF-8") as outFile:
            outFile.write(inFile.read())

def remove_duplicate(src_dir):
    cur_directory = os.path.abspath(os.path.dirname(__file__))
    source_path = os.path.join(cur_directory, src_dir)
    print(source_path)
    file_list = [file_name.split('\\')[-1] for file_name in glob.glob(source_path + '/*.csv')]
    print(len(file_list))

    for i in range(len(file_list)):
        modify_data = []
        with open(os.path.join(source_path, file_list[i]), newline='', encoding = "UTF-8") as infile:
            rows = csv.reader(infile)
            index = []
            for row in rows:
                if row[0] not in index:
                    index.append(row[0])
                    modify_data.append(row)
        with open(os.path.join(source_path, file_list[i]), 'w', newline='', encoding = "UTF-8") as outfile:
            writer = csv.writer(outfile)
            for row in modify_data:
                writer.writerow(row)

def remove_etf_in_investor(src_dir):
    cur_directory = os.path.abspath(os.path.dirname(__file__))
    source_path = os.path.join(cur_directory, src_dir)
    print(source_path)
    file_list = [file_name.split('\\')[-1] for file_name in glob.glob(source_path + '/*.csv')]
    print(len(file_list))

    for i in range(len(file_list)):
        modify_data = []
        with open(os.path.join(source_path, file_list[i]), newline='', encoding = "UTF-8") as infile:
            rows = csv.reader(infile)
            for row in rows:
                if '=' in row[0]: # mean etf
                    continue
                else:
                    modify_data.append(row)
        with open(os.path.join(source_path, file_list[i]), 'w', newline='', encoding = "UTF-8") as outfile:
            writer = csv.writer(outfile)
            for row in modify_data:
                writer.writerow(row)

def fix_investor_header(src_dir):
    cur_directory = os.path.abspath(os.path.dirname(__file__))
    source_path = os.path.join(cur_directory, src_dir)
    print(source_path)
    file_list = [file_name.split('\\')[-1] for file_name in glob.glob(source_path + '/*.csv')]
    print(len(file_list))

    for i in range(len(file_list)):
        modify_data = []
        with open(os.path.join(source_path, file_list[i]), newline='', encoding = "UTF-8") as infile:
            rows = csv.reader(infile)
            for row in rows:
                if (row[0] == '證券代號'):
                    row = [row[0], row[1].split()[0], row[2], row[3], row[4],
                            "外資自營商買進股數", "外資自營商賣出股數", "外資自營商買賣超股數", row[5],
                            row[6], row[7], row[8], row[9], row[10], row[11],
                            row[12], row[13], row[14], row[15]]
                    modify_data.append(row)
                else:
                    modify_data.append(row)
        with open(os.path.join(source_path, file_list[i]), 'w', newline='', encoding = "UTF-8") as outfile:
            writer = csv.writer(outfile)
            for row in modify_data:
                writer.writerow(row)

if __name__ == '__main__':
    #get_period_data("20200909", "20200910", data_type=1)
    #get_period_data("20200909", "20200910", data_type=2)
    get_period_data("20200909", "20200910", data_type=3)
    #get_today_data(3)
    #convert_encode('daily_indicator_big5', 'daily_indicator')
    #get_period_month_data("202007", "202009")
    #remove_duplicate('month')
    #remove_etf_in_investor("daily_investor")
    #fix_investor_header("daily_investor")

    # For test pandas
    '''
    with open("daily_investor\\20191112.csv", newline='', encoding = "UTF-8") as infile:
        rows = csv.reader(infile)
        for row in rows:
            if len(row) != 16:
                print(row)
    tmp = pd.read_csv("daily_investor\\20191112.csv")
    print(tmp.head(5))
    '''
