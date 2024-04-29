from importlib import import_module
from typing import Optional

from django.conf import settings
from django.core.signals import setting_changed


class _MqttSettings:
    BROKER_URL: Optional[str] = None
    TOPIC_HANDLERS: Optional[str] = None
    KEEPALIVE: int = 60
    _DEFAULTS = {
        "BROKER_URL": None,
        "TOPIC_HANDLERS": None,
        "KEEPALIVE": 60,
    }

    def __init__(self, **kwargs):
        self.update(kwargs)

    def update(self, kwargs):
        values = {**self._DEFAULTS, **kwargs}
        for k, v in values.items():
            setattr(self, k, v)

        topic_handlers = values.get("TOPIC_HANDLERS", None)
        if isinstance(topic_handlers, str):
            import_module(topic_handlers)


mqtt_settings = _MqttSettings(**(settings.MQTT_FRAMEWORK or {}))


def _reload_mqtt_settings(*args, **kwargs):
    if kwargs["setting"] == "MQTT_FRAMEWORK":
        mqtt_settings.update(kwargs["value"])


setting_changed.connect(_reload_mqtt_settings)
