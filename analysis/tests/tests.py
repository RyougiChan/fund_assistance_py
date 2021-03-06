from datetime import datetime
from threading import Thread

import yaml
from django.test import TestCase
import pandas as pd
import os

# Create your tests here.
from analysis.conf.yconfig import YConfig
from analysis.core.service.aliyun_oss import AliyunOss
from analysis.core.service.fund import fetch_fund_data, test_fund_path, init_data
from analysis.core.service.pattern import get_bb_data
from analysis.core.service.simulation_trade import SimulationTrade
from analysis.lib.utils import get_path, absolute_file_paths


def test_path():
    print(os.getcwd())
    print(__file__)
    print(os.path.dirname(__file__))
    # print(os.stat("~/core/data/raw"))
    test_fund_path()


def test_fetch_fund_data():
    fetch_fund_data(["000220"])


def test_generate_html():
    get_bb_data("000220")


def test_read_yml():
    with open(get_path('app_config.yml'), encoding='utf-8') as fs:
        data = yaml.safe_load(fs)
        print(data)
        print(data["fund"])


def test_init_data():
    init_data()


def test_read_config():
    print(YConfig.get('fund'))
    print(YConfig.get('fund'))


def test_start_multiple_simulation_trade():
    """测试模拟交易"""
    SimulationTrade.init()
    SimulationTrade.start_multiple_simulation_trade(YConfig.get('fund:code_list'))


def test_get_fund_data():
    """测试获取分红和拆分数据"""
    import akshare as ak
    fund_em_info_df1 = ak.fund_em_open_fund_info(fund="161028", indicator="分红送配详情")
    fund_em_info_df2 = ak.fund_em_open_fund_info(fund="161028", indicator="拆分详情")
    fund_em_info_df1.to_csv("D:\\分红送配详情.csv")
    fund_em_info_df1.to_csv("D:\\拆分详情.csv")
    print(fund_em_info_df1)
    print(fund_em_info_df2)


def test_oss_put_object():
    res = AliyunOss.put_object('test.txt', get_path('data/raw/_000220.csv'))
    print(res)


def test_getmtime():
    print(os.path.getmtime(get_path('data/raw/fund_em_fund_name_df.csv')))
    print(os.path.getmtime(get_path('data/raw/fund_em_fund_name_df.csv')) < datetime.now().timestamp())


def test_sync_oss():
    # t1 = Thread(target=AliyunOss.put_objects,
    #             args=('html/simulation_trade/', absolute_file_paths(get_path('data/html/simulation_trade')),))
    # t2 = Thread(target=AliyunOss.put_objects,
    #             args=('image/simulation_trade/', absolute_file_paths(get_path('data/image/simulation_trade')),))
    t3 = Thread(target=AliyunOss.put_objects,
                args=('html/bollinger_bands/', absolute_file_paths(get_path('data/html/bollinger_bands')),))
    t4 = Thread(target=AliyunOss.put_objects,
                args=('image/bollinger_bands/', absolute_file_paths(get_path('data/image/bollinger_bands')),))
    # t1.start()
    # t2.start()
    t3.start()
    t4.start()
