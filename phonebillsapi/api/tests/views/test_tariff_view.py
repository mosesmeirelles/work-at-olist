import json

from django.test import TestCase
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse

from phonebillsapi.bill.models import Tariff


class TestTariffView(TestCase):
    def setUp(self):
        self.url_list = reverse('api:tariff-list')
        self.data = {
            "tariff_time": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.09",
            "interval_start": "06:00:00",
            "interval_end": "22:00:00"
        }

    def test_insert_tariff(self):
        response = self.client.post(self.url_list, data=json.dumps(self.data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_tariffs(self):
        mommy.make(Tariff)
        mommy.make(Tariff)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_specific_tariff(self):
        mommy.make(Tariff, id=10, **self.data)
        url_detail = reverse('api:tariff-detail', args=[10])

        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 10)

    def test_update_tariff(self):
        mommy.make(Tariff, id=10, **self.data)
        url_detail = reverse('api:tariff-detail', args=[10])

        new_data = {
            "tariff_time": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.08",
            "interval_start": "06:00:00",
            "interval_end": "22:00:00"
        }

        response = self.client.put(url_detail, data=json.dumps(new_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['call_charge'], new_data['call_charge'])
