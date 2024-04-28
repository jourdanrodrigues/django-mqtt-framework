import os

from django_cache_url import config

SECRET_KEY = "fake-key"  # nosec B105
INSTALLED_APPS = ["mqtt_framework"]
MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE") or 60)
MQTT_TOPIC_HANDLERS = "tests.utils"

CACHES = {
    "default": config("CACHE_URL"),
}
