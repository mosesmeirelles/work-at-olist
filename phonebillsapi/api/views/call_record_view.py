from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from phonebillsapi.api.models import CallRecord
from phonebillsapi.api.serializers import CallRecordSerializer
from phonebillsapi.bill.models import BillCallRecord
from phonebillsapi.bill.use_cases.get_call_price_use_case import GetCallPriceUseCase


class CallRecordViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = CallRecordSerializer(data=request.data.copy())

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        start, end = CallRecord.objects.get_pair(serializer.data['call_id'])

        if start and end:
            use_case = GetCallPriceUseCase.initialize()

            BillCallRecord.objects.create(
                call_record_start=start,
                call_record_end=end,
                call_price=use_case.execute(start, end)
            )

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = CallRecord.objects.all()
        serializer = CallRecordSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        callrecord = get_object_or_404(CallRecord, pk=pk)
        serializer = CallRecordSerializer(callrecord)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        callrecord = get_object_or_404(CallRecord, pk=pk)
        callrecord.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        callrecord = get_object_or_404(CallRecord, pk=pk)
        serializer = CallRecordSerializer(callrecord, data=request.data.copy())

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

