from rest_framework import serializers

from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.models import Tariff, BillCallRecord


class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = '__all__'


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'


class BillCallRecordSerializer(serializers.ModelSerializer):
    destination = serializers.SerializerMethodField()
    call_start_date = serializers.SerializerMethodField()
    call_start_time = serializers.SerializerMethodField()

    class Meta:
        model = BillCallRecord
        fields = ('call_duration', 'call_price', 'destination', 'call_start_date', 'call_start_time')

    def get_destination(self, obj):
        return obj.call_record_start.destination

    def get_call_start_date(self, obj):
        return obj.call_record_start.timestamp.date()

    def get_call_start_time(self, obj):
        return obj.call_record_start.timestamp.time()