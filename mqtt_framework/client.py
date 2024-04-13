import re
from functools import cached_property

from django.conf import settings
from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion


class MqttClient(Client):
    @classmethod
    def from_settings(cls) -> 'MqttClient':
        client = cls(CallbackAPIVersion.VERSION2)
        client.authenticate_from_settings()
        client.connect_from_settings()
        return client

    def authenticate_from_settings(self) -> None:
        self.username_pw_set(self._connection_data.get("user"), self._connection_data.get("password"))

    def connect_from_settings(self) -> None:
        port = self._connection_data.get("port")
        self.connect(
            host=self._connection_data["host"],
            port=int(port) if bool(port) else 1883,
            keepalive=getattr(settings, 'MQTT_KEEPALIVE', 60),
        )

    @cached_property
    def _connection_data(self) -> dict:
        match = re.match(
            r"[a-z]+://((?P<user>.*):(?P<password>.*)@)?(?P<host>[^:]*)(:(?P<port>\d+))?",
            settings.MQTT_BROKER_URL,
        )
        if match is None:
            raise ValueError(f"Invalid MQTT URL: {settings.MQTT_BROKER_URL}")
        return match.groupdict()


client = MqttClient.from_settings()
client.authenticate_from_settings()
client.connect_from_settings()
