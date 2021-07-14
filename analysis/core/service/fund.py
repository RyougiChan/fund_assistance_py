"""
fund services and tools
"""
import os
import re

import akshare as ak
import pandas as pd
from datetime import datetime

from analysis.conf.yconfig import YConfig
from analysis.core.service.pattern import get_multiple_bb_data
from analysis.lib.utils import get_path

now = datetime.now()


def test_fund_path():
    print(os.getcwd())
    print(os.stat(get_path('data/raw')))


def init_data(fund_codes=None):
    if fund_codes is None:
        fund_codes = YConfig.get('fund:code_list')
    if fund_codes is not None:
        # fetch fund code list from config
        fetch_fund_data(fund_codes)
        get_multiple_bb_data(fund_codes)


def fetch_fund_data(fund_codes: list):
    today_zero = datetime(now.year, now.month, now.day).timestamp()
    """获取日净值和累计净值"""
    if os.path.exists(get_path('data/raw/fund_em_fund_name_df.csv')) is False or os.path.getmtime(
            get_path('data/raw/fund_em_fund_name_df.csv')) < today_zero:
        fund_em_fund_name_df = ak.fund_em_fund_name()
        fund_em_fund_name_df.to_csv(get_path('data/raw/fund_em_fund_name_df.csv'), index=True, sep=",")
    for code in fund_codes:
        print('开始获取数据', code)
        path_1 = get_path('data/raw/_' + code + '.csv')
        path_2 = get_path('data/raw/__' + code + '.csv')
        if os.path.exists(path_1) is False or os.path.getmtime(path_1) < today_zero:
            new_data_z = ak.fund_em_open_fund_info(fund=code, indicator="累计净值走势")
            new_data_z.to_csv(get_path('data/raw/_' + code + '.csv'), index=False, sep=",")
        else:
            print('数据', path_1, '已更新过')
        if os.path.exists(path_2) is False or os.path.getmtime(path_2) < today_zero:
            new_data_t = ak.fund_em_open_fund_info(fund=code, indicator="单位净值走势")
            new_data_t.to_csv(get_path('data/raw/__' + code + '.csv'), index=False, sep=",")
        else:
            print('数据', path_2, '已更新过')
    print('数据更新完毕：' + str(now))


def fetch_estimation_fund_data():
    """获取当日估算净值"""
    fund_em_value_estimation_df = ak.fund_em_value_estimation(symbol="全部")
    fund_em_value_estimation_df.to_csv(get_path('data/raw/fund_em_value_estimation_df.csv'), index=False, sep=",")


def get_multiple_daily_operation_by_bb(codes: list, latest_datetime_str: str) -> dict:
    """获取每日操作"""
    compare_list = dict()
    date = datetime.fromisoformat(latest_datetime_str)
    for code in codes:
        df = pd.read_csv(get_path('data/raw/_{}_bb.csv'.format(code)))
        line = df.loc[df['date'] == str(date).split(' ')[0]]
        if line is not None:
            prices = line['price'].values
            if len(prices) > 0:
                price = prices[0]
                upper_band = line['upper band'].values[0]
                lower_band = line['lower band'].values[0]
                operation = '观望'
                if price > upper_band:
                    operation = '卖出{}%'.format(YConfig.get("simulation_trade:sell_out_ratio"))
                if price < lower_band:
                    operation = '买入{}%'.format(YConfig.get("simulation_trade:buy_in_ratio"))
                compare_list.update({code: operation})

    return compare_list


def get_daily_operation_by_bb(code, latest_datetime_str: str) -> str:
    """获取每日操作"""
    date = datetime.fromisoformat(latest_datetime_str)
    df = pd.read_csv(get_path('data/raw/_{}_bb.csv'.format(code)))
    line = df.loc[df['date'] == str(date).split(' ')[0]]
    operation = '看戏'
    if line is not None:
        prices = line['price'].values
        if len(prices) > 0:
            price = prices[0]
            upper_band = line['upper band'].values[0]
            lower_band = line['lower band'].values[0]
            if price > upper_band:
                operation = '卖出{}%'.format(YConfig.get("simulation_trade_params:sell_out_ratio"))
            if price < lower_band:
                operation = '买入{}%'.format(YConfig.get("simulation_trade_params:buy_in_ratio"))
    return operation


def get_buy_amount_by_bb(money: float, depot: float, operation_tip: str):
    """获取每日操作金额数值（根据get_daily_operation_by_bb返回的数据）"""
    rer1 = re.match(r'卖出(\d+)%', operation_tip)
    rer2 = re.match(r'买入(\d+)%', operation_tip)
    if rer1 is not None:
        return -depot * float(rer1.groups()[0]) / 100
    elif rer2 is not None:
        return money * float(rer2.groups()[0]) / 100
    if operation_tip == '清仓':
        return -depot
    return None
