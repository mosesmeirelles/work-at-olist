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

    def test_get_pairs_by_period(self):
        mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.START, timestamp="2017-12-12T15:07:13Z")
        mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.END, timestamp="2017-12-12T15:07:13Z")
        mommy.make(CallRecord, call_id=self.call_id + 1, type=CallRecord.START, timestamp="2017-12-12T15:07:13Z")
        mommy.make(CallRecord, call_id=self.call_id + 1, type=CallRecord.END, timestamp="2017-12-12T15:07:13Z")

        pairs = CallRecord.objects.get_completed_pairs(timestamp__month=12, timestamp__year=2017)

        self.assertEqual(len(pairs), 2)

    def test_get_pairs_by_period_and_subscriber(self):
        mommy.make(CallRecord,
                   call_id=self.call_id,
                   type=CallRecord.START,
                   timestamp="2017-12-12T15:07:13Z",
                   source=self.subscriber)
        mommy.make(CallRecord,
                   call_id=self.call_id,
                   type=CallRecord.END,
                   timestamp="2017-12-12T15:07:13Z")
        mommy.make(CallRecord,
                   call_id=self.call_id + 1,
                   type=CallRecord.START,
                   timestamp="2017-12-12T15:07:13Z",
                   source=self.subscriber)
        mommy.make(CallRecord,
                   call_id=self.call_id + 1,
                   type=CallRecord.END,
                   timestamp="2017-12-12T15:07:13Z")
        mommy.make(CallRecord,
                   call_id=self.call_id + 2,
                   type=CallRecord.START,
                   timestamp="2017-12-12T15:07:13Z",
                   source='000000000')
        mommy.make(CallRecord,
                   call_id=self.call_id + 2,
                   type=CallRecord.END,
                   timestamp="2017-12-12T15:07:13Z")

        pairs = CallRecord.objects.get_completed_pairs(timestamp__month=12, timestamp__year=2017,
                                                       source=self.subscriber)

        self.assertEqual(len(pairs), 2)

    def test_get_pairs_by_period_with_call_finishing_next_month(self):
        mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.START, timestamp="2018-02-28T21:57:13Z")
        mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.END, timestamp="2018-03-01T22:10:56Z")

        pairs = CallRecord.objects.get_completed_pairs(timestamp__month=3, timestamp__year=2018)

        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][0].call_id, self.call_id)
