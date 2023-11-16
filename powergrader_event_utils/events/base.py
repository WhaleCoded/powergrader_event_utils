from uuid import uuid4
from enum import StrEnum
from typing import Tuple

from confluent_kafka import Producer

MAIN_TOPIC = "main-record"


# This could be replaced with a dynamically created enum with the following syntax: DynamicEnum = enum.Enum('DynamicEnum', {'foo':42, 'bar':24})
# However, this would mean that there would be no type hints for the enum.
class EventType(StrEnum):
    """
    An enum for the different types of events that can be published or recieved.
    The value will be the name of the corresponding event class.
    """

    # Assignment events
    ASSIGNMENT = "AssignmentEvent"
    RUBRIC = "RubricEvent"

    # Course events
    COURSE = "CourseEvent"
    SECTION = "SectionEvent"
    ORGANIZATION = "OrganizationEvent"

    # Event Wrapper events
    RETRY = "RetryEvent"
    DEAD_LETTER = "DeadLetterEvent"

    # Grade events
    CRITERIA_GRADE = "CriteriaGradeEvent"
    CRITERIA_EMBEDDING = "CriteriaEmbeddingEvent"
    ASSESMENT_SIMILARITY = "AssesmentSimilarityEvent"
    STUDENT_REQUESTED_REGRADE = "StudentRequestedRegradeEvent"
    GRADING_STARTED = "GradingStartedEvent"
    INSTRUCTOR_REVIEW = "InstructorReviewEvent"

    # Publish events
    COURSE_PUBLIC_ID = "RegisterCoursePublicIDEvent"
    SECTION_PUBLIC_ID = "RegisterSectionPublicIDEvent"
    INSTRUCTOR_PUBLIC_ID = "RegisterInstructorPublicIDEvent"
    STUDENT_PUBLIC_ID = "RegisterStudentPublicIDEvent"
    ASSIGNMENT_PUBLIC_ID = "RegisterAssignmentPublicIDEvent"
    RUBRIC_PUBLIC_ID = "RegisterRubricPublicIDEvent"
    SUBMISSION_PUBLIC_ID = "RegisterSubmissionPublicIDEvent"
    PUBLISHED_TO_LMS = "PublishedToLMSEvent"

    # Relationship events
    ASSIGNMENT_ADDED_TO_COURSE = "AssignmentAddedToCourseEvent"
    ASSIGNMENT_REMOVED_FROM_COURSE = "AssignmentRemovedFromCourseEvent"
    STUDENT_ADDED_TO_SECTION = "StudentAddedToSectionEvent"
    STUDENT_REMOVED_FROM_SECTION = "StudentRemovedFromSectionEvent"
    INSTRUCTOR_ADDED_TO_COURSE = "InstructorAddedToCourseEvent"
    INSTRUCTOR_REMOVED_FROM_COURSE = "InstructorRemovedFromCourseEvent"
    PRIVATE_ID_ADDED_TO_PUBLIC_ID = "PrivateIDAddedToPublicIDEvent"
    PRIAVTE_ID_REMOVED_FROM_PUBLIC_ID = "PrivateIDRemovedFromPublicIDEvent"

    # Submission events
    SUBMISSION = "SubmissionEvent"
    SUBMISSION_FILES = "SubmissionFilesEvent"

    # User events
    STUDENT = "StudentEvent"
    INSTRUCTOR = "InstructorEvent"

    # Other
    NOT_SPECIFIED = "DOES_NOT_EXIST"


def generate_event_id(class_name: str) -> str:
    """
    Generates a unique event id for a given class name.
    """

    return class_name.replace("Event", "") + "--" + str(uuid4())


def get_event_type_from_uuid(uuid: str) -> EventType:
    """
    Returns the event type for a given class name.
    """

    if "--" not in uuid:
        return EventType.NOT_SPECIFIED

    class_name = uuid.split("--")[0]
    class_name = class_name + "Event"

    if class_name not in EventType.__members__:
        return EventType.NOT_SPECIFIED

    return EventType(class_name)


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

    def publish_to_custom_topic(self, producer: Producer, topic_name: str) -> bool:
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            # producer.begin_transaction()
            producer.produce(
                topic_name,
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
