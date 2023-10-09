from uuid import uuid4
from confluent_kafka import Producer

MAIN_TOPIC = "main-record"


def generate_event_id(class_name: str) -> str:
    """
    Generates a unique event id for a given class name.
    """

    return class_name + "--" + str(uuid4())


# Setup a common interface for the event system


class PowerGraderEvent:
    def __init__(self, key: str, event_type):
        self.key = key
        self.event_type = event_type

    def publish(self, producer: Producer) -> bool:
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            producer.produce(
                MAIN_TOPIC,
                key=self.key,
                value=serialized_event,
                headers={"event_type": self.event_type},
            )
            producer.flush()
            return True

        return False

    def validate(self) -> bool:
        pass

    def _package_into_proto(self) -> object:
        pass

    def serialize(self) -> str or bool:
        if self.validate():
            return self._package_into_proto().SerializeToString()

        return False

    @classmethod
    def deserialize(cls, event: str):
        pass
