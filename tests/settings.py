import os

from django_cache_url import config

SECRET_KEY = "fake-key"  # nosec B105
INSTALLED_APPS = ["mqtt_framework"]
MQTT_FRAMEWORK = {
    "BROKER_URL": os.getenv("MQTT_BROKER_URL"),
    "TOPIC_HANDLERS": "tests.utils",
}

CACHES = {
    "default": config("CACHE_URL"),
}
