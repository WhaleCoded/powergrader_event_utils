from typing import Type
from datetime import datetime
import time

from powergrader_event_utils.events.event import (
    PowerGraderEvent,
    EventType,
    get_event_type_from_uuid,
    get_kafka_topic_name_for_event_type,
    get_kafka_topic_names_for_event_types,
    get_event_type_from_uuid,
    deserialize_powergrader_event,
)

from powergrader_event_utils.events.assignment import *
from powergrader_event_utils.events.course import *
from powergrader_event_utils.events.user import *
from powergrader_event_utils.events.grade import *
from powergrader_event_utils.events.rag import *
from powergrader_event_utils.events.relationship import *
from powergrader_event_utils.events.submission import *
from powergrader_event_utils.events.publish import *
from powergrader_event_utils.events.retry import *

EMBEDDING_SIZE = 3072


def convert_event_type_to_event_class_type(
    event_type: EventType,
) -> Type[PowerGraderEvent]:
    class_name = event_type.value

    if event_type == EventType.NOT_SPECIFIED:
        return None

    return globals()[class_name]


def convert_proto_when_to_date_time(when: int) -> datetime:
    return datetime.fromtimestamp(when / 1000.0)


def get_miliseconds_since_epoch():
    return int(time.time_ns() / 1_000_000)
