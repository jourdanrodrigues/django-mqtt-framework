import logging

from django.core.management import BaseCommand

from mqtt_framework.client import MqttClient


class Command(BaseCommand):
    help = "Starts the MQTT listener"

    def handle(self, *args, **options):
        logger = self._get_logger()

        client = MqttClient()

        logger.info(f'Listening MQTT events from "{client.conn.host}:{client.conn.port}"')
        client.listen_forever()

    @staticmethod
    def _get_logger() -> logging.Logger:
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger(__name__)
        logger.setLevel("INFO")
        logger.addHandler(handler)

        return logger
