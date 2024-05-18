import json
import logging
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from mqtt_framework.client import Message

try:
    from pydantic import BaseModel  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    BaseModel = None  # type: ignore[no-redef]

try:
    from rest_framework.serializers import Serializer  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    Serializer = None  # type: ignore[no-redef]

logger = logging.getLogger(__name__)


class TopicHandler:
    topic: str
    serializer_class: Type[Serializer]
    pydantic_model: Type[BaseModel]
    qos: int = 0

    def __init_subclass__(cls, **kwargs):
        cls._validate_setup()
        super().__init_subclass__(**kwargs)

    def __init__(self, *, message: "Message"):
        if message.topic != self.topic:
            raise ValueError(f"Topic {message.topic} does not match {self.topic}")

        self.message = message
        self.payload = self.parse_payload(message.payload)

    def handle(self) -> None:
        output = self.get_validated_payload()
        if not isinstance(output, Serializer):
            raise NotImplementedError(f'Override "{type(self).__name__}.handle" to handle the payload.')
        output.save()

    def get_validated_payload(self):
        serializer_class: Serializer = getattr(self, "serializer_class", None)
        if isinstance(serializer_class, type) and issubclass(serializer_class, Serializer):
            context = self.get_serializer_context()
            serializer = serializer_class(
                instance=self.get_serializer_instance(),
                data=self.payload,
                context=context,
            )
            serializer.is_valid(raise_exception=True)
            return serializer

        pydantic_model: BaseModel = getattr(self, "pydantic_model", None)
        if isinstance(pydantic_model, type) and issubclass(pydantic_model, BaseModel):
            return self.pydantic_model(**self.payload)

        return self.payload

    @classmethod
    def parse_payload(cls, payload: str):
        try:
            return json.loads(payload)
        except json.decoder.JSONDecodeError:
            return payload

    def get_serializer_instance(self):
        return None

    def get_serializer_context(self):
        return {"message": self.message}

    @classmethod
    def _validate_setup(cls) -> None:
        attributes = []

        topic = getattr(cls, "topic", None)
        if not isinstance(topic, str) or len(topic) == 0:
            attributes.append("topic")

        if cls.qos not in {0, 1, 2}:
            attributes.append("qos")

        if len(attributes) > 0:
            raise cls.SetupError(f"Class {cls.__name__} is missing or has invalid attributes: {', '.join(attributes)}")

    class SetupError(Exception):
        pass
