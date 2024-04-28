import json

from django.test import SimpleTestCase

from mqtt_framework.client import Message


class TestCreate(SimpleTestCase):
    def test_when_payload_is_dict_then_parses_to_string(self):
        payload = {"test": "value"}
        message = Message.create(topic="test/topic", payload=payload)

        self.assertEqual(message.payload, json.dumps(payload))

    def test_when_payload_is_list_then_parses_to_string(self):
        payload = ["test", "value"]
        message = Message.create(topic="test/topic", payload=payload)

        self.assertEqual(message.payload, json.dumps(payload))

    def test_when_payload_is_a_set_then_parses_to_string(self):
        payload = {"test", "value"}
        message = Message.create(topic="test/topic", payload=payload)

        self.assertEqual(message.payload, json.dumps(list(payload)))

    def test_when_payload_is_tuple_then_parses_to_string(self):
        payload = ("test", "value")
        message = Message.create(topic="test/topic", payload=payload)

        self.assertEqual(message.payload, json.dumps(list(payload)))

    def test_when_payload_is_bytes_then_parses_to_string(self):
        payload = b"test value"
        message = Message.create(topic="test/topic", payload=payload)

        self.assertEqual(message.payload, payload.decode())

    def test_when_payload_is_str_then_leaves_it_as_string(self):
        payload = "test value"
        message = Message.create(topic="test/topic", payload=payload)

        self.assertEqual(message.payload, payload)
