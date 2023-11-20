from typing import Type

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
    deserialize_powergrader_event,
    get_event_type_from_uuid,
    get_kafka_topic_name_for_event_type,
    get_kafka_topic_names_for_event_types,
    get_event_type_from_uuid,
)

from powergrader_event_utils.events.assignment import *
from powergrader_event_utils.events.course import *
from powergrader_event_utils.events.event_wrapper import RetryEvent, DeadLetterEvent
from powergrader_event_utils.events.user import *
from powergrader_event_utils.events.grade import *
from powergrader_event_utils.events.relationship import *
from powergrader_event_utils.events.submission import *
from powergrader_event_utils.events.publish import *


def convert_event_type_to_event_class_type(
    event_type: EventType,
) -> Type[PowerGraderEvent]:
    class_name = event_type.value

    if event_type == EventType.NOT_SPECIFIED:
        return None

    return globals()[class_name]
