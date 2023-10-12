from typing import Tuple

from powergrader_event_utils.events.base import PowerGraderEvent, EventType

from powergrader_event_utils.events.assignment import *
from powergrader_event_utils.events.course import *
from powergrader_event_utils.events.user import *
from powergrader_event_utils.events.grade import *
from powergrader_event_utils.events.relationship import *
from powergrader_event_utils.events.submission import *


def deserialize_powergrader_event(
    event_type: bytes, event: bytes
) -> Tuple[PowerGraderEvent, EventType] or None:
    str_event_type = event_type.decode("utf-8")

    powergrader_event_classes = {}
    for event_class in PowerGraderEvent.__subclasses__():
        powergrader_event_classes[event_class.__name__] = event_class

    if str_event_type in powergrader_event_classes:
        deserialized_event = powergrader_event_classes[str_event_type].deserialize(
            event
        )
        event_type = powergrader_event_classes[str_event_type].get_event_type()

        return deserialized_event, event_type

    return None
