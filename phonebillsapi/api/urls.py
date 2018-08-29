from rest_framework.routers import SimpleRouter

from phonebillsapi.api.views.call_record_view import CallRecordViewSet

router = SimpleRouter()
router.register('callrecord', CallRecordViewSet, base_name='callrecord')

urlpatterns = [] + router.urls
