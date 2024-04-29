# Django MQTT framework

**An MQTT listener and a friendly MQTT client.**

---

# Overview

Django MQTT framework is a Django app that provides a simple MQTT listener and a solid client. It is built on top of the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library.

Some reasons you might want to use MQTT framework:

* **Django MQTT listener**: A simple MQTT listener that can be used to listen to MQTT messages and perform actions based on the messages received.
* **Django MQTT client**: A solid MQTT client that can be used to publish messages to an MQTT broker.

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


class TestTopicHandler(TopicHandler):
    topic = 'test/topic'
    qos = 1

    def handle(self):
        print("Received test message: ", self.message.payload)


class AnotherTopicHandler(TopicHandler):
    topic = 'another/topic'
    qos = 0

    def handle(self):
        print("Received another message: ", self.message.payload)
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
