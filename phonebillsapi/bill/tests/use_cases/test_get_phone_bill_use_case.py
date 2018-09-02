import json

from django.test import TransactionTestCase
from model_mommy import mommy

from phonebillsapi import settings
from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.use_cases.get_phone_bill_use_case import GetPhoneBillUseCase


class TestCallRecordView(TransactionTestCase):

    def setUp(self):
        with open(settings.TESTDATA, 'r') as json_data:
            self.test_data = json.load(json_data)

        for data in self.test_data['call_records']:
            mommy.make(CallRecord, **data)

    def test_get_bill_december_2017(self):
        use_case = GetPhoneBillUseCase.initialize()
        total = use_case.execute(reference_month=12, reference_year=2017)

        self.assertEqual(total, 89.01)

    def test_get_bill_february_2016(self):
        use_case = GetPhoneBillUseCase.initialize()
        total = use_case.execute(reference_month=2, reference_year=2016)

        self.assertEqual(total, 11.16)

    def test_get_bill_march_2018(self):
        use_case = GetPhoneBillUseCase.initialize()
        total = use_case.execute(reference_month=3, reference_year=2018)

        self.assertEqual(total, 86.94)
