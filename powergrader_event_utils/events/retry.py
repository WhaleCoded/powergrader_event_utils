from typing import Union

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.event_wrapper_pb2 import (
    Retry,
    DeadLetter,
)


class RetryEvent(ProtoPowerGraderEvent):
    key_field_name: str = None
    proto_type = Retry

    retry_number: int
    retry_reason: str
    instance_name: str
    event: ProtoPowerGraderEvent

    def __init__(
        self,
        retry_number: int,
        retry_reason: str,
        instance_name: str,
        event: ProtoPowerGraderEvent,
    ) -> None:
        if not isinstance(event, ProtoPowerGraderEvent):
            raise ValueError(
                f"Retry events can only contain powergrader events. Not {type(event)}"
            )
        if event.event_type in [EventType.RETRY, EventType.DEAD_LETTER]:
            raise ValueError(
                f"Retry events can only contain events which are not retry or dead letter events. Was given {event.event_type}"
            )
        self.key_field_name = event.key_field_name
        super().__init__()
        self.retry_number = retry_number
        self.retry_reason = retry_reason
        self.instance_name = instance_name
        self.event = event


class DeadLetterEvent(ProtoPowerGraderEvent):
    key_field_name: str = None
    proto_type = DeadLetter

    dead_letter_reason: str
    instance_name: str
    event: ProtoPowerGraderEvent

    def __init__(
        self, dead_letter_reason: str, instance_name: str, event: ProtoPowerGraderEvent
    ) -> None:
        if not isinstance(event, ProtoPowerGraderEvent):
            raise ValueError(
                f"Dead letter events can only contain powergrader events. Not {type(event)}"
            )
        if event.event_type in [EventType.RETRY, EventType.DEAD_LETTER]:
            raise ValueError(
                f"Dead letter events can only contain events which are not retry or dead letter events. Was given {event.event_type}"
            )
        self.key_field_name = event.key_field_name
        super().__init__()
        self.dead_letter_reason = dead_letter_reason
        self.instance_name = instance_name
        self.event = event


if __name__ == "__main__":
    from powergrader_event_utils.events.assignment import AssignmentEvent

    assignment = AssignmentEvent(
        public_uuid="public_uuid",
        instructor_public_uuid="instructor_public_uuid",
        rubric_version_uuid="rubric_version_uuid",
        name="name",
        description="description",
        version_timestamp=123456,
    )
    retry_event = RetryEvent(
        retry_number=1,
        retry_reason="reason",
        instance_name="instance",
        event=assignment,
    )
    print(retry_event.serialize())
    print(RetryEvent.deserialize(retry_event.serialize()))
    print(retry_event.event_type)

    dead_letter_event = DeadLetterEvent(
        dead_letter_reason="reason", instance_name="instance", event=assignment
    )
    print(dead_letter_event.serialize())
    print(DeadLetterEvent.deserialize(dead_letter_event.serialize()))
