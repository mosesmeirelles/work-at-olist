from django.urls import path
from rest_framework.routers import SimpleRouter

from phonebillsapi.api.views.bill_view import BillViewSet
from phonebillsapi.api.views.call_record_view import CallRecordViewSet
from phonebillsapi.api.views.tariff_view import TariffViewSet

router = SimpleRouter()
router.register('callrecord', CallRecordViewSet, base_name='callrecord')
router.register('tariff', TariffViewSet, base_name='tariff')

urlpatterns = [
    path('bill/<slug:subscriber>/', BillViewSet.as_view({'get': 'list'}), name='bill-list')
] + router.urls
