from rest_framework import serializers

from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.models import Tariff


class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = '__all__'


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'