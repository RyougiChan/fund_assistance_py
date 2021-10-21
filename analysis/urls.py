from django.urls import path
from .core import views, apis

urlpatterns = [
    path('api/data/config', apis.config_data, name='get_config_data'),
    path('api/data/figure', apis.figure_data, name='get_figure_data'),
    path('api/security/credential', apis.get_sts_access_cred, name='get_figure_data'),
    path('api/chives/<str:action>', apis.chives_handler, name='chives'),
    path('api/test/<str:name>', apis.test, name='test'),
    path('', views.index, name='index'),
]
