"""
The only imports from "paho" are supposed to be in this file.
If you find them anywhere else, please move them here (feel free to turn this into a module).
"""

import json
from dataclasses import dataclass
from importlib import import_module
from typing import Optional, Union

from django.conf import settings
from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion

Payload = Union[dict, list, set, tuple, str, bytes, None]


class Message:
    def __init__(self, instance: MQTTMessage):
        self.instance = instance
        self.payload: str = instance.payload.decode()
        self.topic: str = instance.topic

    @classmethod
    def create(cls, *, message_id: Optional[int] = None, topic: str, payload: Payload = None) -> "Message":
        instance = MQTTMessage(mid=message_id, topic=topic.encode())
        instance.payload = cls.payload_to_bytes(payload)
        return cls(instance)

    @staticmethod
    def payload_to_bytes(payload: Payload) -> bytes:
        if payload is None:
            return b""
        if isinstance(payload, (dict, list)):
            return json.dumps(payload).encode()
        elif isinstance(payload, (set, tuple)):
            return json.dumps(list(payload)).encode()
        elif isinstance(payload, str):
            return payload.encode()
        return payload


@dataclass
class ConnectionData:
    user: Optional[str]
    password: Optional[str]
    host: str
    port: Optional[int]


class MqttClient:
    def __init__(
        self,
        broker_url=settings.MQTT_BROKER_URL,
        version: CallbackAPIVersion = CallbackAPIVersion.VERSION2,
        keepalive: int = getattr(settings, "MQTT_KEEPALIVE", 60),
    ):
        if broker_url is None:
            raise ValueError(f'{type(self).__name__} needs a "broker_url"')

        self.client = Client(callback_api_version=version)
        self.conn = self._build_conn(broker_url=settings.MQTT_BROKER_URL)
        self.client.username_pw_set(self.conn.user, self.conn.password)
        self.client.connect(
            host=self.conn.host,
            port=self.conn.port,
            keepalive=keepalive,
        )

    def listen_forever(self) -> None:
        self.attach_topic_handlers()
        self.client.loop_forever()

    def publish(self, topic: str, payload: Payload) -> None:
        self.client.publish(topic=topic, payload=Message.payload_to_bytes(payload))

    def attach_topic_handlers(self) -> None:
        """
        This is imported here to allow usage of this file in any other file.
        """
        from mqtt_framework.topic_handler import TopicHandler

        try:
            import_module(settings.MQTT_TOPIC_HANDLERS)
        except ModuleNotFoundError:
            pass

        topic_handlers: dict[str, type[TopicHandler]] = {}
        for topic_handler in TopicHandler.__subclasses__():
            topic_handlers[topic_handler.topic] = topic_handler
            self.client.subscribe(topic=topic_handler.topic, qos=topic_handler.qos)

        def handle_message(mqtt_client: MqttClient, userdata, message: MQTTMessage) -> None:
            handler = topic_handlers.get(message.topic)
            if handler is not None:
                handler(message=Message(message)).handle()

        self.client.on_message = handle_message

    @staticmethod
    def _build_conn(broker_url: str) -> ConnectionData:
        protocol, remaining = broker_url.split("://")
        if protocol not in {"mqtt", "mqtts"}:
            raise ValueError(f"Invalid protocol for MQTT_BROKER_URL: {protocol}")

        if "@" in remaining:
            user_info, host_port = remaining.split("@")
            user, password = user_info.split(":") if ":" in user_info else (user_info, None)
        else:
            user, password = None, None
            host_port = remaining

        host, port = host_port.split(":") if ":" in host_port else (host_port, "1883")

        return ConnectionData(user=user, password=password, host=host, port=int(port))
