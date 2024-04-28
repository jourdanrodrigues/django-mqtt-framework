from django.core.management import BaseCommand

from mqtt_framework.client import MqttClient


class Command(BaseCommand):
    help = "Starts the MQTT listener"

    def handle(self, *args, **options):
        MqttClient().listen_forever()
