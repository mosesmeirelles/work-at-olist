import datetime
import json

from django.test import TransactionTestCase
from model_mommy import mommy

from phonebillsapi import settings
from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.models import BillCallRecord, Tariff
from phonebillsapi.bill.use_cases.get_call_price_use_case import GetCallPriceUseCase
from phonebillsapi.bill.use_cases.get_phone_bill_price_use_case import GetPhoneBillPriceUseCase


class TestGetBillPriceUseCase(TransactionTestCase):

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

        with open(settings.TESTDATA, 'r') as json_data:
            self.test_data = json.load(json_data)

        for data in self.test_data['call_records']:
            mommy.make(CallRecord, **data)

            start, end = CallRecord.objects.get_pair(data['call_id'])

            if start and end:
                uc = GetCallPriceUseCase.initialize()

                mommy.make(BillCallRecord,
                           call_record_start=start,
                           call_record_end=end,
                           call_price=uc.execute(start, end))

        self.subscriber = 99988526423

    def test_get_bill_december_2017(self):
        use_case = GetPhoneBillPriceUseCase.initialize()
        total = use_case.execute(reference_month=12, reference_year=2017, subscriber=self.subscriber)

        self.assertEqual(total, 90.81)

    def test_get_bill_february_2016(self):
        use_case = GetPhoneBillPriceUseCase.initialize()
        total = use_case.execute(reference_month=2, reference_year=2016, subscriber=self.subscriber)

        self.assertEqual(total, 11.16)

    def test_get_bill_march_2018(self):
        use_case = GetPhoneBillPriceUseCase.initialize()
        total = use_case.execute(reference_month=3, reference_year=2018, subscriber=self.subscriber)

        self.assertEqual(total, 86.94)
