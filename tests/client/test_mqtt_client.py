import json
from asyncio import sleep
from uuid import uuid4

from django.core.cache import cache
from django.test import SimpleTestCase
from paho.mqtt.client import MQTTMessage
from rest_framework import serializers

from mqtt_framework.client import MqttClient
from mqtt_framework.topic_handler import TopicHandler


async def a_moment() -> None:
    """
    Messages are handled in a thread. This is to wait for them to be handled.
    "moment" is a relative term and will reflect whatever time is needed here.
    """
    await sleep(0.01)


class TestMqttClient(SimpleTestCase):
    def tearDown(self):
        cache.clear()

    async def test_that_the_message_callback_works(self):
        topic = f'mqtt/{uuid4()}'
        payload = 'Hello, World!'
        cache_key = str(uuid4())
        mqtt_client = MqttClient.from_settings()
        mqtt_client.loop_start()
        mqtt_client.subscribe(topic)

        @mqtt_client.message_callback()
        def on_message(mqtt_client, userdata, message: MQTTMessage) -> None:
            cache.set(cache_key, {
                'topic': message.topic,
                'decoded_payload': message.payload.decode(),
                'user_data': userdata,
            })

        mqtt_client.publish(topic, payload)
        await a_moment()

        mqtt_client.loop_stop()

        self.assertEqual(cache.get(cache_key), {
            'topic': topic,
            'decoded_payload': payload,
            'user_data': None,
        })

    async def test_that_the_topic_handler_works(self):
        cache_key = str(uuid4())

        class DjangoMqttSerializer(serializers.Serializer):
            test = serializers.CharField()

            def create(self, validated_data):
                cache.set(cache_key, validated_data)
                return validated_data

        class DjangoMqttHandler(TopicHandler):
            topic = f'mqtt/{uuid4()}'
            serializer_class = DjangoMqttSerializer

        mqtt_client = MqttClient.from_settings()
        mqtt_client.loop_start()
        mqtt_client.attach_topic_handlers()
        payload = {'test': 'went well'}

        mqtt_client.publish(DjangoMqttHandler.topic, json.dumps(payload))
        await a_moment()

        mqtt_client.loop_stop()

        self.assertEqual(cache.get(cache_key), payload)
