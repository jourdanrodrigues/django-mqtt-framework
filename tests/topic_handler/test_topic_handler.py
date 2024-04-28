from uuid import uuid4

from django.core.cache import cache
from django.test import SimpleTestCase

from mqtt_framework.client import Message
from mqtt_framework.topic_handler import TopicHandler


class TestInit(SimpleTestCase):
    def test_when_topic_does_not_match_then_raises_exception(self):
        class SampleHandler(TopicHandler):
            topic = "test/topic"

        message = Message.create(topic="test/other")

        with self.assertRaisesMessage(ValueError, "Topic test/other does not match test/topic"):
            SampleHandler(message=message)

    def test_when_topic_matches_then_sets_message_and_payload(self):
        class SampleHandler(TopicHandler):
            topic = "test/topic"

        payload = {"test": "value"}
        message = Message.create(topic=SampleHandler.topic, payload=payload)

        handler = SampleHandler(message=message)

        self.assertEqual(handler.message, message)
        self.assertEqual(handler.payload, payload)

    def test_when_topic_handler_does_not_have_topic_then_raises_exception(self):
        message = "Class SampleHandler is missing or has invalid attributes: topic"

        with self.assertRaisesMessage(TopicHandler.SetupError, message):

            class SampleHandler(TopicHandler):
                pass

    def test_when_topic_handler_has_invalid_qos_then_raises_exception(self):
        message = "Class SampleHandler is missing or has invalid attributes: qos"

        with self.assertRaisesMessage(TopicHandler.SetupError, message):

            class SampleHandler(TopicHandler):
                topic = "test/topic"
                qos = "invalid"


class TestHandle(SimpleTestCase):
    def tearDown(self):
        cache.clear()

    def test_when_a_serializer_is_set_then_uses_it(self):
        try:
            from rest_framework import serializers
        except ImportError:  # pragma: no cover
            return

        cache_key = str(uuid4())
        payload = {"test": "value"}

        class SampleSerializer(serializers.Serializer):
            test = serializers.CharField()

            def create(self, validated_data):
                cache.set(cache_key, validated_data)
                return validated_data

        class SampleHandler(TopicHandler):
            topic = "test/serializer"
            serializer_class = SampleSerializer

        message = Message.create(topic=SampleHandler.topic, payload=payload)

        SampleHandler(message=message).handle()

        self.assertEqual(cache.get(cache_key), payload)

    def test_when_a_pydantic_model_is_set_and_has_no_implementation_then_raises_exception(self):
        try:
            from pydantic import BaseModel
        except ImportError:  # pragma: no cover
            return

        payload = {"test": "value"}

        class SampleModel(BaseModel):
            test: str

        class SampleHandler(TopicHandler):
            topic = "test/pydantic"
            pydantic_model = SampleModel

        message = Message.create(topic=SampleHandler.topic, payload=payload)

        error = 'Override "SampleHandler.handle" to handle the payload.'

        with self.assertRaisesMessage(NotImplementedError, error):
            SampleHandler(message=message).handle()

    def test_when_neither_pydantic_model_or_serializer_are_set_and_has_no_implementation_then_raises_exception(self):
        payload = {"test": "value"}

        class OtherHandler(TopicHandler):
            topic = "test/empty"

        message = Message.create(topic=OtherHandler.topic, payload=payload)

        error = 'Override "OtherHandler.handle" to handle the payload.'

        with self.assertRaisesMessage(NotImplementedError, error):
            OtherHandler(message=message).handle()
