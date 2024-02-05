from typing import Type

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
    deserialize_powergrader_event,
)
from powergrader_event_utils.events.proto_events.event_wrapper_pb2 import (
    Retry,
    DeadLetter,
)
from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


def convert_event_type_to_member_name(event_type: EventType) -> str:
    if event_type == EventType.RETRY or event_type == EventType.DEAD_LETTER:
        raise ValueError("You can put a retry or dead letter event into a retry event.")

    # CONVERT TO SNAKE CASE
    return event_type.name.lower()


def convert_member_name_to_event_type(member_name: str) -> EventType:
    # convert the member to screaming snake case
    screaming_snake_case = member_name.upper()
    return EventType.__getattribute__(screaming_snake_case)


class RetryEvent(PowerGraderEvent):
    retry_number: int
    retry_reason: str
    instance_name: str
    event: PowerGraderEvent

    def __init__(
        self,
        retry_number: int,
        retry_reason: str,
        instance_name: str,
        event: PowerGraderEvent,
    ) -> None:
        if not isinstance(event, PowerGraderEvent):
            raise ValueError("The event you are trying to put into a retry is invalid.")

        self.proto = Retry()

        if retry_number is not None:
            self.proto.retry_number = retry_number
        self.retry_number = retry_number

        if retry_reason is not None:
            self.proto.retry_reason = retry_reason
        self.retry_reason = retry_reason

        if instance_name is not None:
            self.proto.instance_name = instance_name
        self.instance_name = instance_name

        if event is not None:
            self._put_event_into_proto(event)
            self.event = event

        super().__init__(
            key=str(event.key),
            event_type=self.__class__.__name__,
            alternate_topic_event_type=event.get_event_type(),
        )

    def _put_event_into_proto(self, event: PowerGraderEvent) -> None:
        """
        This will put the event into the correct oneof field in the protobuf message. It will throw an exception if something about the event was malformed.
        """

        # Find the correct member
        event_type = event.get_event_type()
        member_name = convert_event_type_to_member_name(event_type)

        # Fill the member with the event
        member_field = self.proto.__getattribute__(member_name)
        member_field.CopyFrom(event.proto)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RETRY

    def _package_into_proto(self) -> Retry:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RetryEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = Retry()
        data.ParseFromString(event)
        # Extract the event object and package it
        event_member_name = data.WhichOneof("event")
        if event_member_name is None:
            return None
        event_bytes = data.__getattribute__(event_member_name).SerializeToString()
        powergrader_event_type = convert_member_name_to_event_type(event_member_name)
        packaged_event, _ = deserialize_powergrader_event(
            powergrader_event_type.value.encode("utf-8"), event_bytes
        )

        new_retry_instance = cls.__new__(cls)
        new_retry_instance.proto = data
        new_retry_instance.event = packaged_event
        new_retry_instance.retry_number = data.retry_number
        new_retry_instance.retry_reason = data.retry_reason
        new_retry_instance.instance_name = data.instance_name
        super(cls, new_retry_instance).__init__(
            key=packaged_event.key,
            event_type=new_retry_instance.__class__.__name__,
        )

        return new_retry_instance


class DeadLetterEvent(PowerGraderEvent):
    dead_letter_reason: str
    instance_name: str
    event: PowerGraderEvent

    def __init__(
        self, dead_letter_reason: str, instance_name: str, event: PowerGraderEvent
    ) -> None:
        if not isinstance(event, PowerGraderEvent):
            raise ValueError("The event you are trying to put into a retry is invalid.")

        self.proto = DeadLetter()

        if instance_name is not None:
            self.proto.instance_name = instance_name
        self.instance_name = instance_name

        if dead_letter_reason is not None:
            self.proto.dead_letter_reason = dead_letter_reason
        self.dead_letter_reason = dead_letter_reason

        if event is not None:
            self._put_event_into_proto(event)
            self.event = event

        super().__init__(key=str(event.key), event_type=self.__class__.__name__)

    def _put_event_into_proto(self, event: PowerGraderEvent) -> None:
        """
        This will put the event into the correct oneof field in the protobuf message. It will throw an exception if something about the event was malformed.
        """

        # Find the correct member
        event_type = event.get_event_type()
        member_name = convert_event_type_to_member_name(event_type)

        # Fill the member with the event
        member_field = self.proto.__getattribute__(member_name)
        member_field.CopyFrom(event.proto)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.DEAD_LETTER

    def _package_into_proto(self) -> DeadLetter:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "DeadLetterEvent":
        # Deserialize the event bytes back to a protobuf message.
        data = DeadLetter()
        data.ParseFromString(event)

        # Extract the event object and package it
        event_member_name = data.WhichOneof("event")
        if event_member_name is None:
            return None

        event_bytes = data.__getattribute__(event_member_name).SerializeToString()
        powergrader_event_type = convert_member_name_to_event_type(event_member_name)
        packaged_event, _ = deserialize_powergrader_event(
            powergrader_event_type.value.encode("utf-8"), event_bytes
        )

        new_dead_letter_instance = cls.__new__(cls)
        new_dead_letter_instance.proto = data
        new_dead_letter_instance.event = packaged_event
        new_dead_letter_instance.dead_letter_reason = data.dead_letter_reason
        super(cls, new_dead_letter_instance).__init__(
            key=packaged_event.key,
            event_type=new_dead_letter_instance.__class__.__name__,
        )

        return new_dead_letter_instance
