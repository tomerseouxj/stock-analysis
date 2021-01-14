#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
使用baostock库导入股票历史数据

数据单位：金额（元），成交量（股）

作者：wking [http://wkings.net]
"""

import os
import time
import pandas as pd

import baostock
import akshare

import user_config as ucfg

#变量定义
starttime_str = time.strftime("%H:%M:%S", time.localtime())
starttime_tick = time.time()


# 获取沪深 A 股股票代码和简称数据
def download_stocklist():
    """
    调用akshare库获取当前最新A股股票列表，返回列表类型的代码
    """
    df = pd.DataFrame(akshare.stock_info_a_code_name())
    stocklist = df['code'].tolist()
    return stocklist

# 切片股票列表stocklist，指定开始股票和结束股票
def update_stocklist(stocklist, start_num, end_num):
    """


    Parameters
    ----------
    start_num : str
    从哪只股票开始处理

    end_num : str
    处理到哪只股票为止

    Returns
    -------
    处理后的股票代码列表

    """
    for i in stocklist:
        if i == start_num:
            start_index = stocklist.index(i)
            stocklist = stocklist[start_index:]
        if i == end_num:
            end_index = stocklist.index(i)
            stocklist = stocklist[:end_index]

    return stocklist


# 主程序开始

# 下载最新股票代码列表
stocklist = download_stocklist()

#定义要下载的股票区间
start_stock_num = '300861'  # 留空则从头开始处理 不需要输入sh/sz
end_stock_num = ''  # 留空则处理到末尾
stocklist = update_stocklist(stocklist, start_stock_num, end_stock_num)

#### 登陆系统 ####
lg = baostock.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

for i in stocklist:
    if i[0:1] == '6':
        ii = 'sh.' + i
    elif i[0:1] == '0' or i[0:1] == '3':
        ii = 'sz.' + i

    process_info = '[' + str(stocklist.index(i) + 1) + '/' + str(len(stocklist)) + '] ' + i
    try:
        rs = baostock.query_history_k_data_plus(ii,
            "date,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pbMRQ,isST",
            start_date='1991-01-01', end_date='',
            frequency="d", adjustflag="3")
    except:
        print(process_info + ' >>>wrong<<<')
        print('query_history_k_data_plus respond error_code:' + rs.error_code)
        print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
    else:
        #### 打印结果集 ####
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())

        result = pd.DataFrame(data_list, columns=rs.fields)
        print(process_info + ' 完成 开始时间[' + starttime_str + '] 已用'
              + str(round(time.time() - starttime_tick)) + '秒')
        csv_file = ucfg.csv_path + os.sep + i + '.csv'
        result.to_csv(csv_file, index=True)

#### 登出系统 ####
baostock.logout()