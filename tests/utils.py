import time

from django.core.cache import cache

from mqtt_framework import TopicHandler


def wait_a_moment() -> None:
    """
    Messages are handled in a thread. This is to wait for them to be handled.
    "moment" is a relative term and will reflect whatever time is needed here.
    """
    time.sleep(0.01)


class TestTopicHandler(TopicHandler):
    topic = "test_topic"

    def handle(self) -> None:
        cache.set(self.topic, self.payload)
