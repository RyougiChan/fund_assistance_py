import os

from django.http import HttpResponse, JsonResponse

from analysis.lib.utils import get_path


def get_data(request, data_name):
    name_map = {
        'simulation_trade': 'simulation_trade',
        'bollinger_bands': 'bollinger_bands'
    }
    if name_map.get(data_name) is None:
        return JsonResponse({})

    data = [d.replace('.png', '') for d in os.listdir(get_path('../data/image/{}'.format(name_map[data_name])))]
    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii': False})


