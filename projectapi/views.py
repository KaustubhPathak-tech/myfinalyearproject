from django.shortcuts import render
from rest_framework import generics
from .models import SensorData
from .serializers import SensorDataSerializer, HumidityDataSerializer

def index(request):
    return render(request,'index.html')

class TempDataList(generics.ListAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    
class HumidityDataList(generics.ListAPIView):
    queryset = SensorData.objects.all()
    serializer_class = HumidityDataSerializer
    
def sensor_data_view(request):
    sensor_data = SensorData.objects.all()
    return render(request, 'sensor_data.html', {'sensor_data': sensor_data})
