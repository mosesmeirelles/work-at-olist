from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from phonebillsapi.api.serializers import CallRecordSerializer


class CallRecordView(APIView):
    def post(self, *args, **kwargs):
        serializer = CallRecordSerializer(data=self.request.data.copy())

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

