import json

from django.test import TestCase
from model_mommy import mommy
from rest_framework.reverse import reverse
from rest_framework import status

from phonebillsapi.api.models import CallRecord


class TestCallRecordView(TestCase):
    def setUp(self):
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
