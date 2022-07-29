from cycles.models import CyclesLength, Temperature
from rest_framework import serializers


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"
        depth = 1


class TemperatureMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ["day_of_cycle", "temperature"]


class CyclesLengthSerializer(serializers.ModelSerializer):
    temperatures = TemperatureMiniSerializer(many=True)

    class Meta:
        model = CyclesLength
        fields = ["id", "user", "first_day", "length", "temperatures"]
