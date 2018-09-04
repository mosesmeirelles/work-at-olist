import datetime
import json
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse

from phonebillsapi import settings
from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.models import BillCallRecord, Tariff
from phonebillsapi.bill.use_cases.get_call_price_use_case import GetCallPriceUseCase


class TestBillView(TestCase):

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

        self.url = reverse('api:bill-list', kwargs={'subscriber': 99988526423})

    def test_get_bill_of_february_2016(self):
        expected = {
            'bill_call_records': [{
                'destination': '9993468278',
                'call_start_date': '2016-02-29',
                'call_start_time': '12:00:00',
                'call_duration': '02:00:00',
                'call_price': '11.16'
            }],
            'subscriber': '99988526423',
            'month': '2',
            'year': '2016',
            'price': 11.16
        }

        response = self.client.get(self.url, {'month': 2, 'year': 2016})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    @patch('django.utils.timezone.now')
    def test_get_bill_of_march_2018_without_parameters(self, mocked_timezone):
        mocked_timezone.return_value = datetime.datetime(2018, 4, 10, tzinfo=timezone.utc)

        expected = {
            'bill_call_records': [{
                'destination': '9993468278',
                'call_start_date': '2018-02-28',
                'call_start_time': '21:57:13',
                'call_duration': '24:13:43',
                'call_price': '86.94'
            }],
            'subscriber': '99988526423',
            'month': '3',
            'year': '2018',
            'price': 86.94
        }

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    @patch('django.utils.timezone.now')
    def test_get_bill_on_going_period(self, mocked_timezone):
        mocked_timezone.return_value = datetime.datetime(2018, 8, 10, tzinfo=timezone.utc)

        expected = {
            'detail': "Reference period hasn't ended."
        }

        response = self.client.get(self.url, {'month': 8, 'year': 2018})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), expected)

