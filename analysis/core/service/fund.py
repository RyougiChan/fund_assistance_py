"""
fund services and tools
"""
import os

import akshare as ak
from datetime import datetime

os.chdir(os.path.dirname(__file__))

now = datetime.now()


def test():
    print(os.getcwd())
    print(os.stat('../data/raw'))


def fetch_fund_data(fund_codes: list):
    x = os.getcwd()
    y = os.path.abspath(__file__)
    """获取日净值和累计净值"""
    fund_em_fund_name_df = ak.fund_em_fund_name()
    fund_em_fund_name_df.to_csv('../data/raw/fund_em_fund_name_df.csv', index=True, sep=",")
    for code in fund_codes:
        print('开始获取数据', code)
        new_data_z = ak.fund_em_open_fund_info(fund=code, indicator="累计净值走势")
        new_data_z.to_csv('../data/raw/_' + code + '.csv', index=False, sep=",")
        new_data_t = ak.fund_em_open_fund_info(fund=code, indicator="单位净值走势")
        new_data_t.to_csv('../data/raw/__' + code + '.csv', index=False, sep=",")
    print('数据更新完毕：' + str(now))


def fetch_estimation_fund_data():
    """获取当日估算净值"""
    fund_em_value_estimation_df = ak.fund_em_value_estimation(symbol="全部")
    fund_em_value_estimation_df.to_csv('../data/raw/fund_em_value_estimation_df.csv', index=False, sep=",")
