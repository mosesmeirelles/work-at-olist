from rest_framework import viewsets

from phonebillsapi.api.serializers import TariffSerializer
from phonebillsapi.bill.models import Tariff


class TariffViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given tariff.

    list:
    Return a list of all existing tariffs.

    create:
    Create a new tariff.

    update:
    Update an existing tariff.

    delete:
    Delete a tariff.
    """

    serializer_class = TariffSerializer
    queryset = Tariff.objects.all()
