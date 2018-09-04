from django.test import TestCase
from model_mommy import mommy

from phonebillsapi.api.models import CallRecord


class CallRecordQuerySetTests(TestCase):
    def setUp(self):
        self.call_id = 12
        self.subscriber = 99988526423

    def test_get_pair(self):
        mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.START)
        mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.END)

        start, end = CallRecord.objects.get_pair(call_id=self.call_id)

        self.assertTrue(start)
        self.assertTrue(end)
        self.assertEqual(start.call_id, end.call_id)

    def test_get_one_member_pair(self):
        mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.START)

        start, end = CallRecord.objects.get_pair(call_id=self.call_id)

        self.assertTrue(start)
        self.assertFalse(end)
