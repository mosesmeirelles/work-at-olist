import json

from django.test import TransactionTestCase
from model_mommy import mommy

from phonebillsapi import settings
from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.use_cases.get_phone_bill_price_use_case import GetPhoneBillPriceUseCase


class TestGetBillPriceUseCase(TransactionTestCase):

    def setUp(self):
        with open(settings.TESTDATA, 'r') as json_data:
            self.test_data = json.load(json_data)

        for data in self.test_data['call_records']:
            mommy.make(CallRecord, **data)

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
