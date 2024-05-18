import logging
import os
from collections import namedtuple
from importlib import import_module
from typing import Optional

try:
    from django.conf import settings
    from django.core.signals import setting_changed
except ImportError:
    settings = namedtuple("settings", ["MQTT_FRAMEWORK"])(None)  # type: ignore[arg-type]
    setting_changed = None
    _has_django = False
else:
    _has_django = True


class _MqttSettings:
    BROKER_URL: Optional[str]
    TOPIC_HANDLERS: Optional[str]
    KEEPALIVE: int
    _DEFAULTS = {
        "BROKER_URL": os.getenv("MQTT_BROKER_URL"),
        "TOPIC_HANDLERS": os.getenv("MQTT_TOPIC_HANDLERS"),
        "KEEPALIVE": os.getenv("KEEPALIVE", 60),
    }

    def __init__(self, **kwargs):
        self.update(kwargs)

    def get_logger(self) -> logging.Logger:
        return logging.getLogger("django.server" if _has_django else "mqtt_framework")

    def update(self, kwargs):
        values = {**self._DEFAULTS, **kwargs}
        for k, v in values.items():
            setattr(self, k, v)

        topic_handlers = values.get("TOPIC_HANDLERS")
        if isinstance(topic_handlers, str):
            import_module(topic_handlers)


mqtt_settings = _MqttSettings(**(settings.MQTT_FRAMEWORK or {}))


if setting_changed is not None:

    def _reload_mqtt_settings(*args, **kwargs):
        if kwargs["setting"] == "MQTT_FRAMEWORK":
            mqtt_settings.update(kwargs["value"])

    setting_changed.connect(_reload_mqtt_settings)
