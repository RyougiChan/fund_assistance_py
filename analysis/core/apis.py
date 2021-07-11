import json
import os

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analysis.conf.yconfig import YConfig
from analysis.core.constant.fund_data import FundData
from analysis.core.service.fund import init_data
from analysis.core.service.simulation_trade import SimulationTrade
from analysis.lib.utils import get_path


def figure_data(request):
    if request.method == 'POST':
        if request.body is None:
            return JsonResponse({})
        request_data = json.loads(request.body)
        code_name_list = []
        print(request_data)
        if len(request_data):
            init_data(request_data)
            SimulationTrade.init()
            SimulationTrade.start_multiple_simulation_trade(request_data)
            for code in request_data:
                fund_name = FundData.fund_name_df.loc[FundData.fund_name_df['基金代码'] == code, '基金简称'].values[0]
                code_name_list.append(fund_name)
        return JsonResponse({'data': {
            'fund': {
                'code_list': request_data,
                'code_name_list': code_name_list
            }
        }})
    return JsonResponse({})


def get_config_data():
    config = YConfig.get()
    code_name_list = []
    for code in config['fund']['code_list']:
        fund_name = FundData.fund_name_df.loc[FundData.fund_name_df['基金代码'] == code, '基金简称'].values[0]
        code_name_list.append(fund_name)
    config['fund']['code_name_list'] = code_name_list
    return JsonResponse({'data': config}, json_dumps_params={'ensure_ascii': False})


handle_config_data = {
    'GET': get_config_data
}


def config_data(request):
    return handle_config_data[request.method]()


def get_simulation_trade_figure(request):
    if request.method == 'POST':
        print('post request')
        concat = request.POST
        post_body = request.body
        print(concat)
        print(type(post_body))
        print(post_body)
        json_result = json.loads(post_body)
        print(json_result)


