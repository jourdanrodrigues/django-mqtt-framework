import select
import time
from subprocess import PIPE, STDOUT, Popen  # nosec B404
from uuid import uuid4

from django.core.cache import cache
from django.test import SimpleTestCase

from mqtt_framework.client import MqttClient
from tests.utils import TestTopicHandler


class TestCommand(SimpleTestCase):
    process: Popen

    @classmethod
    def setUpClass(cls):
        cls.process = Popen(["python", "manage.py", "runmqtt"], stdout=PIPE, stderr=STDOUT)  # nosec B603, B607
        try:
            cls.assertLogsMessage("Listening MQTT events from")
        except Exception as e:
            cls.tearDownClass()
            raise e from None

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.__exit__(None, None, None)

    def tearDown(self):
        cache.clear()

    def test_that_it_listens_to_events(self):
        payload = {"test": str(uuid4())}

        MqttClient().publish(TestTopicHandler.topic, payload)  # "TestTopicHandler" is loaded via settings

        self.assertLogsMessage("Received message to the topic")
        self.assertDictEqual(cache.get(TestTopicHandler.topic), payload)

    @classmethod
    def assertLogsMessage(cls, message: str, *, max_iterations: int = 10, interval: float = 0.1) -> None:
        poll = select.poll()
        poll.register(cls.process.stdout, select.POLLIN)  # type: ignore[arg-type]
        iterations = 0
        lines = []
        while iterations < max_iterations:
            if poll.poll(0):
                line = cls.process.stdout.readline().decode()  # type: ignore[union-attr]
                if not line:
                    continue
                if message in line:
                    return
                lines.append(line)

            iterations += 1
            time.sleep(interval)

        lines_str = "\n    ".join(lines)
        logs = f"Logs:{lines_str}" if lines_str else "No logs found."
        raise AssertionError(f"Could not find log message:\n    {message}\n{logs}")
