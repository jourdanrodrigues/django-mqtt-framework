import os

SECRET_KEY = "fake-key"  # nosec B105
INSTALLED_APPS = ["mqtt_framework"]
MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE") or 60)
MQTT_TOPIC_HANDLERS = "mqtt_framework.topics"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",  # nosec B108
    },
}
