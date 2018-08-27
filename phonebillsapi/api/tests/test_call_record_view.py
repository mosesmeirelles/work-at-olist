import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class TestCallRecordView(TestCase):
    def setUp(self):
        self.url = reverse('api:callrecord')

    def test_insert_call_start_record(self):
        data = {
            "id": 1,
            "type": "start",
            "timestamp": "2016-02-29T12:00:00Z",
            "call_id": 70,
            "source": '99988526423',
            "destination": '9993468278'
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
