from django.urls import path
from .core import views, apis

urlpatterns = [
    path('api/data/config', apis.config_data, name='get_config_data'),
    path('api/data/figure', apis.figure_data, name='get_figure_data'),
    path('', views.index, name='index'),
]
