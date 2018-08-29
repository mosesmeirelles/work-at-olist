from django.test import TestCase

from phonebillsapi.api.serializers import CallRecordSerializer


class CallRecordSerializerTests(TestCase):
    def test_required_fields(self):
        required_fields = ['type', 'timestamp', 'call_id']
        serializer = CallRecordSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(required_fields), len(serializer.errors))

        for field_name in required_fields:
            self.assertIn(field_name, serializer.errors)

    def test_valid_object_insert(self):
        data = {
            "id": 1,
            "type": "start",
            "timestamp": "2016-02-29T12:00:00Z",
            "call_id": 70,
            "source": '99988526423',
            "destination": '9993468278'
        }

        serializer = CallRecordSerializer(data=data)
        serializer.is_valid()

        self.assertTrue(serializer.is_valid())

        instance = serializer.save()

        self.assertTrue(instance.id)
