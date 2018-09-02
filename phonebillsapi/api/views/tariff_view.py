from rest_framework import viewsets

from phonebillsapi.api.serializers import TariffSerializer
from phonebillsapi.bill.models import Tariff


class TariffViewSet(viewsets.ModelViewSet):

    serializer_class = TariffSerializer
    queryset = Tariff.objects.all()
