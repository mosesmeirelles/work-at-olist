from django.test import TestCase

from phonebillsapi.api.serializers import TariffSerializer


class TariffSerializerTests(TestCase):
    def test_required_fields(self):
        required_fields = ['tariff_time', 'standing_charge', 'call_charge', 'interval_start', 'interval_end']
        serializer = TariffSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(required_fields), len(serializer.errors))

        for field_name in required_fields:
            self.assertIn(field_name, serializer.errors)

    def test_valid_object_insert(self):
        data = {
            "tariff_time": "standard",
            "standing_charge": "0.36",
            "call_charge": "0.09",
            "interval_start": "06:00:00",
            "interval_end": "22:00:00"
        }

        serializer = TariffSerializer(data=data)
        serializer.is_valid()

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        self.assertTrue(instance.id)
