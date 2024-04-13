from asyncio import sleep

from django.core.cache import cache
from django.test import SimpleTestCase
from paho.mqtt.client import MQTTMessage

from mqtt_framework.client import MqttClient


class TestMqttClient(SimpleTestCase):
    def setUp(self):
        self.mqtt_client = MqttClient.from_settings()
        self.mqtt_client.loop_start()

    def tearDown(self):
        cache.clear()
        self.mqtt_client.loop_stop()

    async def test_that_the_message_callback_works(self):
        topic = 'django/mqtt'
        payload = 'Hello, World!'
        cache_key = 'test_cache_key'
        self.mqtt_client.subscribe(topic)

        @self.mqtt_client.message_callback()
        def on_message(mqtt_client, userdata, message: MQTTMessage) -> None:
            cache.set(cache_key, {
                'topic': message.topic,
                'decoded_payload': message.payload.decode(),
                'user_data': userdata,
            })

        self.mqtt_client.publish(topic, payload)
        await sleep(0.01)  # Callbacks go to a thread, wait for them to handle the event

        self.assertEqual(cache.get(cache_key), {
            'topic': topic,
            'decoded_payload': payload,
            'user_data': None,
        })
