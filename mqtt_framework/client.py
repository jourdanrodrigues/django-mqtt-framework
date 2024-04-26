from dataclasses import dataclass
from importlib import import_module

from django.conf import settings
from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion

from mqtt_framework.topic_handler import TopicHandler


@dataclass
class ConnectionData:
    user: str | None
    password: str | None
    host: str
    port: int | None


class MqttClient(Client):
    def attach_topic_handlers(self) -> None:
        try:
            import_module(settings.MQTT_TOPIC_HANDLERS)
        except ModuleNotFoundError:
            pass

        topic_handlers: dict[str, type[TopicHandler]] = {}
        for topic_handler in TopicHandler.__subclasses__():
            topic_handlers[topic_handler.topic] = topic_handler
            self.subscribe(topic=topic_handler.topic, qos=topic_handler.qos)

        def handle_message(mqtt_client: MqttClient, userdata, message: MQTTMessage) -> None:
            handler = topic_handlers.get(message.topic)
            if handler is not None:
                handler(message=message).handle()

        self.on_message = handle_message

    @classmethod
    def from_settings(cls) -> 'MqttClient':
        self = cls(CallbackAPIVersion.VERSION2)
        conn = cls.get_connection_data()
        keep_alive = getattr(settings, 'MQTT_KEEPALIVE', 60)
        self.username_pw_set(conn.user, conn.password)
        self.connect(host=conn.host, port=conn.port, keepalive=keep_alive)
        return self

    @staticmethod
    def get_connection_data() -> ConnectionData:
        if settings.MQTT_BROKER_URL is None:
            raise ValueError("MQTT_BROKER_URL is not set")

        protocol, remaining = settings.MQTT_BROKER_URL.split("://")
        if protocol not in {"mqtt", "mqtts"}:
            raise ValueError(f"Invalid protocol for MQTT_BROKER_URL: {protocol}")

        if "@" in remaining:
            user_info, host_port = remaining.split("@")
            user, password = user_info.split(":") if ":" in user_info else (user_info, None)
        else:
            user, password = None, None
            host_port = remaining

        host, port = host_port.split(":") if ":" in host_port else (host_port, '1883')

        return ConnectionData(user=user, password=password, host=host, port=int(port))

