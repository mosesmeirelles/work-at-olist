import datetime

from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.models import Tariff
from phonebillsapi.bill.use_cases.get_call_price_use_case import GetCallPriceUseCase


class TestGetCallPrice(TestCase):
    def setUp(self):
        mommy.make(Tariff,
                   tariff_time=Tariff.STANDARD,
                   interval_start=datetime.time(6, 0, 0),
                   interval_end=datetime.time(22, 0, 0),
                   call_charge=0.09,
                   standing_charge=0.36)
        mommy.make(Tariff,
                   tariff_time=Tariff.REDUCED,
                   interval_start=datetime.time(22, 0, 0),
                   interval_end=datetime.time(6, 0, 0),
                   call_charge=0.09,
                   standing_charge=0.36)

    def test_get_price_same_interval(self):
        call_start = mommy.make(CallRecord, timestamp=datetime.datetime(2016, 2, 29, 12, 00, 00, tzinfo=timezone.utc))
        call_end = mommy.make(CallRecord, timestamp=datetime.datetime(2016, 2, 29, 14, 00, 00, tzinfo=timezone.utc))

        use_case = GetCallPriceUseCase.initialize()
        call_price = use_case.execute(call_start, call_end)

        self.assertEqual(call_price, 11.16)

    def test_get_price_different_interval(self):
        call_start = mommy.make(CallRecord, timestamp=datetime.datetime(2017, 12, 12, 21, 57, 13, tzinfo=timezone.utc))
        call_end = mommy.make(CallRecord, timestamp=datetime.datetime(2017, 12, 12, 22, 10, 56, tzinfo=timezone.utc))

        use_case = GetCallPriceUseCase.initialize()
        call_price = use_case.execute(call_start, call_end)

        self.assertEqual(call_price, 0.54)

    def test_get_price_different_interval_in_days(self):
        call_start = mommy.make(CallRecord, timestamp=datetime.datetime(2018, 2, 28, 21, 57, 13, tzinfo=timezone.utc))
        call_end = mommy.make(CallRecord, timestamp=datetime.datetime(2018, 3, 1, 22, 10, 56, tzinfo=timezone.utc))

        use_case = GetCallPriceUseCase.initialize()
        call_price = use_case.execute(call_start, call_end)

        self.assertEqual(call_price, 86.94)
