import os
from threading import Thread

import akshare as ak

from django.apps import AppConfig

from analysis.conf.yconfig import YConfig
from analysis.core.service.fund import fetch_fund_data
from analysis.core.service.pattern import get_multiple_bb_data
from analysis.core.service.simulation_trade import SimulationTrade
from analysis.lib.utils import get_path


class AnalysisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analysis'
    # 获取基本配置
    YConfig.get()
    fund_codes = YConfig.get('fund:code_list')
    SimulationTrade.init()
    # 创建资源目录
    if os.path.exists(get_path('data/raw/')) is False:
        os.makedirs(get_path('data/raw/'))
        os.makedirs(get_path('data/html/'))
        # 获取基金列表-天天基金
        fund_em_fund_name_df_path = get_path('data/raw/fund_em_fund_name_df.csv')
        if os.path.exists(fund_em_fund_name_df_path) is False:
            fetch_fund_data(fund_codes)
    if os.path.exists(get_path('data/image/')) is False:
        os.makedirs(get_path('data/html/simulation_trade/'))
        os.makedirs(get_path('data/html/bollinger_bands/'))
        os.makedirs(get_path('data/image/simulation_trade/'))
        os.makedirs(get_path('data/image/bollinger_bands/'))
        # 生成布林带数据
        get_multiple_bb_data(fund_codes)
        t = Thread(target=SimulationTrade.start_multiple_simulation_trade, args=(fund_codes,))
        t.start()
