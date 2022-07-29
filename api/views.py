from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import CyclesLengthSerializer, TemperatureSerializer
from cycles.models import CyclesLength, Temperature
# Create your views here.


class CyclesLengthViewSet(viewsets.ModelViewSet):
    queryset = CyclesLength.objects.all()
    serializer_class = CyclesLengthSerializer


class TemperatureViewSet(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    def list(self, request, *args, **kwargs):
        queryset = Temperature.objects.all()
        serializer = TemperatureSerializer(queryset, many=True)
        return Response(serializer.data)
