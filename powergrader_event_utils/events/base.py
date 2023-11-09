from uuid import uuid4
from enum import Enum

from confluent_kafka import Producer

MAIN_TOPIC = "main-record"


class EventType(Enum):
    """
    An enum for the different types of events that can be published or recieved.
    """

    ASSIGNMENT = 0
    RUBRIC = 1
    COURSE = 2
    CLASS = 3
    ORGANIZATION = 4
    CRITERIA_GRADE = 5
    CRITERIA_EMBEDDING = 6
    ASSESMENT_SIMILARITY = 7
    STUDENT_REQUESTED_REGRADE = 8
    ASSIGNMENT_ADDED_TO_COURSE = 9
    ASSIGNMENT_REMOVED_FROM_COURSE = 10
    STUDENT_ADDED_TO_SECTION = 11
    STUDENT_REMOVED_FROM_SECTION = 12
    INSTRUCTOR_ADDED_TO_COURSE = 13
    INSTRUCTOR_REMOVED_FROM_COURSE = 14
    SUBMISSION = 15
    SUBMISSION_FILES = 16
    STUDENT = 17
    INSTRUCTOR = 18
    COURSE_PUBLIC_ID = 19
    SECTION_PUBLIC_ID = 20
    INSTRUCTOR_PUBLIC_ID = 21
    STUDENT_PUBLIC_ID = 22
    ASSIGNMENT_PUBLIC_ID = 23
    RUBRIC_PUBLIC_ID = 24
    SUBMISSION_PUBLIC_ID = 25
    PUBLISHED_TO_LMS = 26
    PRIVATE_ID_ADDED_TO_PUBLIC_ID = 27
    PRIAVTE_ID_REMOVED_FROM_PUBLIC_ID = 28
    GRADING_STARTED = 29
    INSTRUCTOR_REVIEW = 30
    NOT_SPECIFIED = 31


def generate_event_id(class_name: str) -> str:
    """
    Generates a unique event id for a given class name.
    """

    return class_name.replace("Event", "") + "--" + str(uuid4())


# Setup a common interface for the event system


class PowerGraderEvent:
    def __init__(self, key: str, event_type):
        self.key = key
        self.event_type = event_type

    def publish(self, producer: Producer) -> bool:
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            # producer.begin_transaction()
            producer.produce(
                MAIN_TOPIC,
                key=self.key,
                value=serialized_event,
                headers={"event_type": self.event_type},
            )
            producer.flush()
            # producer.commit_transaction()
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

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.NOT_SPECIFIED
