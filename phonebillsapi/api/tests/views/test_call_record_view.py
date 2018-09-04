import datetime
import json

from django.test import TestCase
from model_mommy import mommy
from rest_framework.reverse import reverse
from rest_framework import status

from phonebillsapi.api.models import CallRecord
from phonebillsapi.bill.models import BillCallRecord, Tariff


class TestCallRecordView(TestCase):
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

        self.url_list = reverse('api:callrecord-list')

    def test_insert_call_start_record(self):
        data = {
            "id": 1,
            "type": "start",
            "timestamp": "2016-02-29T12:00:00Z",
            "call_id": 70,
            "source": '99988526423',
            "destination": '9993468278'
        }
        response = self.client.post(self.url_list, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_insert_call_start_and_end_record_should_create_bill_call_record(self):
        start = {
            "id": 1,
            "type": "start",
            "timestamp": "2016-02-29T12:00:00Z",
            "call_id": 70,
            "source": '99988526423',
            "destination": '9993468278'
        }

        end = {
            "id": 9,
            "type": "end",
            "timestamp": "2016-02-29T14:00:00Z",
            "call_id": 70
        }
        self.client.post(self.url_list, data=json.dumps(start), content_type='application/json')
        self.client.post(self.url_list, data=json.dumps(end), content_type='application/json')

        bill_call_record = BillCallRecord.objects.all()

        self.assertEqual(len(bill_call_record), 1)
        self.assertEqual(bill_call_record.first().call_record_start.call_id, 70)

    def test_get_all_call_records(self):
        mommy.make(CallRecord)
        mommy.make(CallRecord)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_specific_call_record(self):
        mommy.make(CallRecord, id=10)
        url_detail = reverse('api:callrecord-detail', args=[10])

        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 10)

    def test_update_call_record(self):
        mommy.make(CallRecord,
                   id=10,
                   source='000000000')
        url_detail = reverse('api:callrecord-detail', args=[10])

        new_data = {
            "type": "start",
            "timestamp": "2016-02-29T12:00:00Z",
            "call_id": 70,
            "source": '99988526423',
            "destination": '9993468278'
        }

        response = self.client.put(url_detail, data=json.dumps(new_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['source'], new_data['source'])

    def test_validation_insert_two_equal_call_records(self):
        mommy.make(CallRecord,
                   id=10,
                   call_id=70,
                   type=CallRecord.START)

        data = {
            "type": "start",
            "timestamp": "2016-02-29T12:00:00Z",
            "call_id": 70,
            "source": '99988526423',
            "destination": '9993468278'
        }

        expected = {
            "non_field_errors": [
                "The fields call_id, type must make a unique set."
            ]
        }

        response = self.client.post(self.url_list, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected)

    def test_validation_phone_number(self):
        data = {
            "type": "start",
            "timestamp": "2016-02-29T12:00:00Z",
            "call_id": 70,
            "source": '99988526423',
            "destination": '123as'
        }

        expected = {
            'destination': ["Phone number must be entered in the format '12345678910'. 10 to 11 digits allowed."]
        }

        response = self.client.post(self.url_list, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected)
