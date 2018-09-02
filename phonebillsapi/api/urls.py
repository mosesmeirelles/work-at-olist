from rest_framework.routers import SimpleRouter

from phonebillsapi.api.views.call_record_view import CallRecordViewSet
from phonebillsapi.api.views.tariff_view import TariffViewSet

router = SimpleRouter()
router.register('callrecord', CallRecordViewSet, base_name='callrecord')
router.register('tariff', TariffViewSet, base_name='tariff')

urlpatterns = [] + router.urls
