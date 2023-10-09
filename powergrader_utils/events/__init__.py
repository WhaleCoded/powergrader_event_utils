from powergrader_utils.events.base import PowerGraderEvent

from powergrader_utils.events.assignment import *
from powergrader_utils.events.course import *
from powergrader_utils.events.user import *
from powergrader_utils.events.grade import *
from powergrader_utils.events.relationship import *
from powergrader_utils.events.submission import *

from enum import Enum


class EventType(Enum):
    """
    An enum for the different types of events that can be published or recieved.
    """

    ASSIGNMENT = 0
    RUBRIC = 1
    COURSE = 2
    CLASS = 3
    ORGANIZATION = 4
    GRADE = 5
    GRADING_METHOD = 6
    FACULTY_GRADE_ADJUSTMENT = 7
    STUDENT_REQUESTED_REGRADE = 8
    ASSINGMENT_ADDED_TO_CLASS = 9
    ASSINGMENT_REMOVED_FROM_CLASS = 10
    STUDENT_ADDED_TO_CLASS = 11
    STUDENT_REMOVED_FROM_CLASS = 12
    SUBMISSION = 13
    STUDENT = 14
    INSTRUCTOR = 15


def deserialize_powergrader_event(event_type: bytes, event: bytes):
    str_event_type = event_type.decode("utf-8")

    powergrader_event_classes = {}
    for event_class in PowerGraderEvent.__subclasses__():
        powergrader_event_classes[event_class.__name__] = event_class

    print(powergrader_event_classes)

    if str_event_type in powergrader_event_classes:
        return powergrader_event_classes[str_event_type].deserialize(event)

    return None
