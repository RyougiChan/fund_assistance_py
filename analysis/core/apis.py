import json
import os

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analysis.conf.yconfig import YConfig
from analysis.core.constant.fund_data import FundData
from analysis.lib.utils import get_path


def get_figure_data(request, data_name):
    name_map = {
        'simulation_trade': 'simulation_trade',
        'bollinger_bands': 'bollinger_bands'
    }
    if name_map.get(data_name) is None:
        return JsonResponse({})

    data = [d.replace('.png', '') for d in os.listdir(get_path('../data/image/{}'.format(name_map[data_name])))]
    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii': False})


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


