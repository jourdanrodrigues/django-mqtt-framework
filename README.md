# Django MQTT framework

**An MQTT listener and a friendly MQTT client.**

---

# Overview

Django MQTT framework is a Django app that provides a simple MQTT listener and a solid client. It is built on top of the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library.

----

# Requirements

* Python 3.6+
* Django 5.0, 4.2, 4.1, 4.0, 3.2, 3.1, 3.0

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.

# Installation

Install using `pip` (soon)...

    pip install django-mqtt-framework

Add `'mqtt_framework'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = [
    # ...
    'mqtt_framework',
]
```

# Running the MQTT listener

To run the MQTT listener, you can use the `runmqtt` management command:

    python manage.py runmqtt

# Defining topic handlers

Within `your_app/topic_handlers.py` module, you'll write the topic handlers:

```python
from mqtt_framework import TopicHandler
from rest_framework import serializers
from django.core.cache import cache
from pydantic import BaseModel


class SimpleTestModel(BaseModel):
    testing: str


class SimpleTestSerializer(serializers.Serializer):
    testing = serializers.CharField()

    def create(self, validated_data):
        cache.set('test_message', validated_data)
        return validated_data


class SerializerTopicHandler(TopicHandler):
    topic = 'test/topic'
    serializer_class = SimpleTestSerializer
    qos = 1

    # Calls the serializer's "save" method


class PydanticTopicHandler(TopicHandler):
    topic = 'another/topic'
    pydantic_model = SimpleTestModel
    qos = 0

    def handle(self):
        pydantic_instance = self.get_validated_payload()
        # Do something with the pydantic_instance
```

# Django Settings

```python
MQTT_FRAMEWORK = {
    'BROKER_URL': 'mqtt://<user>:<password>@<host>:<port>',
    'TOPIC_HANDLERS': 'your_app.topic_handlers',
    'KEEPALIVE': 60,
}
```

That's it, we're done!

    ./manage.py runmqtt
