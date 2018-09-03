from django.test import TestCase
from model_mommy import mommy

from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.models import BillCallRecord


class TestBillCallQuerySet(TestCase):
    def setUp(self):
        self.call_id = 12
        self.subscriber = 99988526423

    def test_get_pairs_by_period(self):
        start1 = mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.START, timestamp="2017-12-12T15:07:13Z")
        end1 = mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.END, timestamp="2017-12-12T15:07:13Z")
        start2 = mommy.make(CallRecord, call_id=self.call_id + 1, type=CallRecord.START,
                            timestamp="2017-12-12T15:07:13Z")
        end2 = mommy.make(CallRecord, call_id=self.call_id + 1, type=CallRecord.END, timestamp="2017-12-12T15:07:13Z")
        mommy.make(BillCallRecord, call_record_start=start1, call_record_end=end1)
        mommy.make(BillCallRecord, call_record_start=start2, call_record_end=end2)

        bill_call_records = BillCallRecord.objects.filter_by_references(month=12, year=2017)

        self.assertEqual(len(bill_call_records), 2)

    def test_get_pairs_by_period_and_subscriber(self):
        start1 = mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.START, timestamp="2017-12-12T15:07:13Z",
                            source=self.subscriber)
        end1 = mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.END, timestamp="2017-12-12T15:07:13Z")
        start2 = mommy.make(CallRecord, call_id=self.call_id + 1, type=CallRecord.START,
                            timestamp="2017-12-12T15:07:13Z", source=self.subscriber)
        end2 = mommy.make(CallRecord, call_id=self.call_id + 1, type=CallRecord.END, timestamp="2017-12-12T15:07:13Z")
        start3 = mommy.make(CallRecord, call_id=self.call_id + 2, type=CallRecord.START,
                            timestamp="2017-12-12T15:07:13Z", source='000000000')
        end3 = mommy.make(CallRecord, call_id=self.call_id + 2, type=CallRecord.END, timestamp="2017-12-12T15:07:13Z")

        mommy.make(BillCallRecord, call_record_start=start1, call_record_end=end1)
        mommy.make(BillCallRecord, call_record_start=start2, call_record_end=end2)
        mommy.make(BillCallRecord, call_record_start=start3, call_record_end=end3)

        bill_call_records = BillCallRecord.objects.filter_by_references(month=12, year=2017, subscriber=self.subscriber)

        self.assertEqual(len(bill_call_records), 2)

    def test_get_pairs_by_period_with_call_finishing_next_month(self):
        start = mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.START, timestamp="2018-02-28T21:57:13Z")
        end = mommy.make(CallRecord, call_id=self.call_id, type=CallRecord.END, timestamp="2018-03-01T22:10:56Z")
        mommy.make(BillCallRecord, call_record_start=start, call_record_end=end)

        bill_call_records = BillCallRecord.objects.filter_by_references(month=3, year=2018)

        self.assertEqual(len(bill_call_records), 1)
        self.assertEqual(bill_call_records[0].call_record_start.call_id, self.call_id)
