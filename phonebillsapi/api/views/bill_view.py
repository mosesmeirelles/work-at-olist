from rest_framework import viewsets, status
from rest_framework.response import Response

from phonebillsapi.api.serializers import BillCallRecordSerializer
from phonebillsapi.bill.models import BillCallRecord
from phonebillsapi.bill.use_cases.get_phone_bill_price_use_case import GetPhoneBillPriceUseCase


class BillViewSet(viewsets.ViewSet):
    def list(self, request, subscriber=None):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        use_case = GetPhoneBillPriceUseCase.initialize()
        bill_price = use_case.execute(month, year, subscriber)

        data = {
            'bill_call_records': self.get_bill_call_records(month, year, subscriber),
            'subscriber': subscriber,
            'month': month,
            'year': year,
            'price': bill_price,
        }

        return Response(data, status=status.HTTP_200_OK)

    def get_bill_call_records(self, month, year, subscriber):
        bill_call_records = BillCallRecord.objects.filter_by_references(month, year, subscriber)
        return BillCallRecordSerializer(bill_call_records, many=True).data