from django.urls import path
from .core import views, apis

urlpatterns = [
    path('api/data/<str:data_name>', apis.get_data, name='get_data'),
    path('', views.index, name='index'),
]
