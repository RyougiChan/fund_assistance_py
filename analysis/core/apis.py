import json
import sys
from datetime import datetime, timedelta

import jwt
from django.http import JsonResponse, HttpResponseBadRequest

from analysis.conf.yconfig import YConfig
from analysis.core.chives import add_chives
from analysis.core.constant.fund_data import FundData
from analysis.core.errors import Errors
from analysis.core.service.aliyun_oss import AliyunOss
from analysis.core.service.fund import init_data
from analysis.core.service.simulation_trade import SimulationTrade
from analysis.models import Chives


def figure_data(request):
    if request.method == 'POST':
        if request.body is None:
            return JsonResponse({})
        request_data = json.loads(request.body)
        code_name_list = []
        if len(request_data):
            init_data(request_data)
            SimulationTrade.init()
            SimulationTrade.start_multiple_simulation_trade(request_data)
            for code in request_data:
                fund_name = FundData.fund_name_df.loc[FundData.fund_name_df['基金代码'] == code, '基金简称'].values[0]
                code_name_list.append(fund_name)
        resp = Errors.SUCCESS.__dict__
        resp['data'] = {
            'fund': {
                'code_list': request_data,
                'code_name_list': code_name_list
            }
        }
        return JsonResponse(resp)
    return JsonResponse(Errors.REQUEST_METHOD_ILLEGAL.__dict__)


def get_config_data():
    config = {'fund': YConfig.get('fund'), 'oss': {'enable': YConfig.get('oss:enable')}}
    code_name_list = []
    for code in config['fund']['code_list']:
        fund_name = FundData.fund_name_df.loc[FundData.fund_name_df['基金代码'] == code, '基金简称'].values[0]
        code_name_list.append(fund_name)
    config['fund']['code_name_list'] = code_name_list
    resp = Errors.SUCCESS.__dict__
    resp['data'] = config
    return JsonResponse(resp, json_dumps_params={'ensure_ascii': False})


handle_config_data = {
    'GET': get_config_data
}


def config_data(request):
    return handle_config_data[request.method]()


def get_sts_access_cred(request):
    response = AliyunOss.get_sts_access_credential(sys.argv[1:])
    resp = Errors.SUCCESS.__dict__
    resp['data'] = response.body.to_map()
    print(Errors.SUCCESS)
    print(Errors.SUCCESS.__dict__)
    return JsonResponse(resp)


def chives_handler(request, action: str):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        if action == 'signin':
            try:
                if Chives.objects.filter(login_name=post_data['login_name']).count() == 0:
                    return JsonResponse(Errors.NOT_FOUND.__dict__)

                chives = Chives.objects.get(login_name=post_data['login_name'])
                if chives.match_password(post_data['login_password']) is False:
                    return JsonResponse(Errors.NOT_FOUND.__dict__)

                payload = {
                    'chives_id': chives.id,
                    'exp': datetime.utcnow() + timedelta(seconds=YConfig.get('jwt:expire_time_seconds'))
                }
                jwt_token = jwt.encode(payload, YConfig.get('jwt:secret'), YConfig.get('jwt:algorithm'))
                resp = JsonResponse(Errors.SUCCESS.__dict__)
                resp.headers['authorization'] = jwt_token
                return resp
            except:
                print(sys.exc_info())
                return JsonResponse(Errors.UNKNOWN_ERROR.__dict__)
        if action == 'signout':
            return JsonResponse(Errors.SUCCESS.__dict__)
    return JsonResponse(Errors.REQUEST_METHOD_ILLEGAL.__dict__)


def test(request, name):
    if name == 'add-chives':
        print(request)
        a = add_chives('cirno', 'cirno0207')
        print(a)
        print(Errors.SUCCESS)
        print(Errors.SUCCESS.__dict__)
        return JsonResponse(Errors.SUCCESS.__dict__)
    return JsonResponse(Errors.REQUEST_ACTION_ILLEGAL.__dict__)

def test2():
    '1'.format()
