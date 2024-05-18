import json
import logging
from uuid import uuid4

from django.core.cache import cache
from django.test import SimpleTestCase
from paho.mqtt.client import MQTTMessage

from mqtt_framework import TopicHandler
from mqtt_framework.client import MqttClient
from mqtt_framework.settings import mqtt_settings
from tests.utils import a_moment

logger = mqtt_settings.get_logger()


class TestInit(SimpleTestCase):
    def test_when_broker_url_is_none_then_raises_exception(self):
        with self.assertRaisesMessage(ValueError, 'MqttClient needs a "broker_url"'):
            MqttClient(broker_url=None)


class TestClient(SimpleTestCase):
    def tearDown(self):
        logger.setLevel(logging.INFO)
        cache.clear()

    async def test_that_the_message_callback_works(self):
        topic = f"mqtt/{uuid4()}"
        payload = "Hello, World!"
        cache_key = str(uuid4())
        mqtt = MqttClient()
        mqtt.client.loop_start()
        mqtt.client.subscribe(topic)

        @mqtt.client.message_callback()
        def on_message(mqtt_client, userdata, message: MQTTMessage) -> None:
            data = {
                "topic": message.topic,
                "decoded_payload": message.payload.decode(),
                "user_data": userdata,
            }
            cache.set(cache_key, data)

        mqtt.client.publish(topic, payload)
        await a_moment()

        mqtt.client.loop_stop()

        expected_data = {
            "topic": topic,
            "decoded_payload": payload,
            "user_data": None,
        }
        self.assertEqual(cache.get(cache_key), expected_data)

    async def test_that_the_topic_handlers_get_attached(self):
        logger.setLevel(logging.WARNING)

        cache_key = str(uuid4())

        class DjangoMqttHandler(TopicHandler):
            topic = f"mqtt/{uuid4()}"

            def handle(self) -> None:
                cache.set(cache_key, self.payload)

        mqtt = MqttClient()
        mqtt.client.loop_start()
        mqtt.attach_topic_handlers()
        payload = {"test": "went well"}

        mqtt.client.publish(DjangoMqttHandler.topic, json.dumps(payload))
        await a_moment()

        mqtt.client.loop_stop()

        self.assertEqual(cache.get(cache_key), payload)
