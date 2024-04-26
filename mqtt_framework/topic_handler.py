import json
import logging

from paho.mqtt.client import MQTTMessage
from rest_framework import serializers

logger = logging.getLogger(__name__)


class TopicHandler:
    topic: str
    serializer_class: type[serializers.Serializer]
    qos: int = 0

    def __init_subclass__(cls, **kwargs):
        cls._validate_setup()
        super().__init_subclass__(**kwargs)

    def __init__(self, *, message: MQTTMessage):
        self.message = message
        self.payload = self.parse_payload(message.payload)

    def handle(self) -> None:
        context = self.get_serializer_context()
        serializer = self.serializer_class(data=self.payload, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @classmethod
    def parse_payload(cls, payload: str | bytes):
        return json.loads(payload)

    def get_serializer_context(self):
        return {'message': self.message}

    @classmethod
    def _validate_setup(cls) -> None:
        attributes = []
        if not hasattr(cls, 'serializer_class'):
            attributes.append('serializer_class')

        topic = getattr(cls, 'topic')
        if not isinstance(topic, str) or len(topic) == 0:
            attributes.append('topic')

        if cls.qos not in {0, 1, 2}:
            attributes.append('qos')

        if len(attributes) > 0:
            raise cls.SetupError(
                f"Class {cls.__name__} is missing or has invalid attributes: {', '.join(attributes)}"
            )

    class SetupError(Exception):
        pass
