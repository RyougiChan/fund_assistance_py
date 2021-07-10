from django.urls import path
from .core import views, apis

urlpatterns = [
    path('api/data/config', apis.config_data, name='get_config_data'),
    path('api/data/<str:data_name>', apis.get_figure_data, name='get_figure_data'),
    path('api/data/trade_figure', apis.get_simulation_trade_figure, name='get_simulation_trade_figure'),
    path('', views.index, name='index'),
]
