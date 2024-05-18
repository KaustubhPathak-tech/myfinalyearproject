from django.contrib import admin
from django.urls import path
from .views import index, TempDataList, HumidityDataList, sensor_data_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('api/temp-data/', TempDataList.as_view(), name='sensor-data-list'),
    path('api/humidity-data/', HumidityDataList.as_view(), name='humidity-data-list'),
    path('sensor-data/', sensor_data_view, name='sensor_data'),
]
