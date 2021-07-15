import os

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from analysis.conf.yconfig import YConfig
from analysis.core.service.fund import init_data, fetch_fund_data
from analysis.core.service.pattern import get_multiple_bb_data
from analysis.core.service.simulation_trade import SimulationTrade
from analysis.lib.utils import get_path


def index(request):
    # 是否获取数据
    fetch_data = request.GET.get('f')
    # 是否计算布林带
    bb = request.GET.get('b')
    # 是否模拟交易
    simulate_trade = request.GET.get('s')
    f = False if fetch_data is None or fetch_data == 0 else True
    s = False if simulate_trade is None or simulate_trade == 0 else True
    b = False if bb is None or bb == 0 else True
    # [1] 初始化配置
    code_list = YConfig.get('fund:code_list')
    if f is True:
        # [2] 获取基金数据
        fetch_fund_data(code_list)

    if b is True:
        # [3] 计算布林带
        get_multiple_bb_data(code_list)

    if s is True:
        # [4] 开始模拟交易
        SimulationTrade.init()
        SimulationTrade.start_multiple_simulation_trade(code_list)

    simulate_trade_data = os.listdir(get_path('data/image/simulation_trade'))
    context = {'simulate_trade_data': simulate_trade_data}

    return render(request, 'index.html', context)


def signin(request):
    return render(request, 'signin.html')
