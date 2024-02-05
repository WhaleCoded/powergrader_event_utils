from uuid import uuid4
from strenum import StrEnum
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
    AI_CRITERION_GRADING_STARTED = "AICriterionGradingStartedEvent"
    GRADING_METHOD = "GradingMethodEvent"
    AI_CRITERION_GRADE = "AICriterionGradeEvent"
    AI_INFERRED_CRITERION_GRADE = "AIInferredCriterionGradeEvent"
    INSTRUCTOR_CRITERION_GRADE = "InstructorCriterionGradeEvent"
    INSTRUCTOR_OVERRIDE_CRITERION_GRADE = "InstructorOverrideCriterionGradeEvent"
    CRITERION_GRADE_EMBEDDING = "CriterionGradeEmbeddingEvent"
    INSTRUCTOR_SUBMISSION_GRADE_APPROVAL = "InstructorSubmissionGradeApprovalEvent"

    # Publish events
    REGISTER_COURSE_PUBLIC_UUID = "RegisterCoursePublicUUIDEvent"
    REGISTER_SECTION_PUBLIC_UUID = "RegisterSectionPublicUUIDEvent"
    REGISTER_INSTRUCTOR_PUBLIC_UUID = "RegisterInstructorPublicUUIDEvent"
    REGISTER_STUDENT_PUBLIC_UUID = "RegisterStudentPublicUUIDEvent"
    REGISTER_ASSIGNMENT_PUBLIC_UUID = "RegisterAssignmentPublicUUIDEvent"
    REGISTER_RUBRIC_PUBLIC_UUID = "RegisterRubricPublicUUIDEvent"
    REGISTER_SUBMISSION_PUBLIC_UUID = "RegisterSubmissionPublicUUIDEvent"
    PUBLISHED_TO_LMS = "PublishedToLMSEvent"
    PUBLISHED_GRADE_TO_LMS = "PublishedGradeToLMSEvent"

    # Relationship events
    ASSIGNMENT_ADDED_TO_COURSE = "AssignmentAddedToCourseEvent"
    ASSIGNMENT_REMOVED_FROM_COURSE = "AssignmentRemovedFromCourseEvent"
    STUDENT_ADDED_TO_SECTION = "StudentAddedToSectionEvent"
    STUDENT_REMOVED_FROM_SECTION = "StudentRemovedFromSectionEvent"
    INSTRUCTOR_ADDED_TO_COURSE = "InstructorAddedToCourseEvent"
    INSTRUCTOR_REMOVED_FROM_COURSE = "InstructorRemovedFromCourseEvent"

    # Submission events
    SUBMISSION = "SubmissionEvent"
    SUBMISSION_GROUP_FILE = "SubmissionGroupFileEvent"

    # User events
    STUDENT = "StudentEvent"
    INSTRUCTOR = "InstructorEvent"

    # Other
    NOT_SPECIFIED = "DOES_NOT_EXIST"


def get_kafka_topic_name_for_event_type(event_type: EventType) -> str:
    """
    Returns the kafka topic names for a given event type.
    """

    return event_type.value.replace("Event", "")


def get_kafka_topic_names_for_event_types(event_types: list[EventType]) -> list[str]:
    """
    Returns the kafka topic names for a given list of event types.
    """

    if event_types is None:
        # Return all topics
        all_topics = set(
            [
                get_kafka_topic_name_for_event_type(event_type)
                for event_type in EventType
            ]
        )
        all_topics.remove(EventType.NOT_SPECIFIED.value)

        return list(all_topics)

    return [
        get_kafka_topic_name_for_event_type(event_type) for event_type in event_types
    ]


def generate_event_uuid(class_name: str) -> str:
    """
    Generates a unique event uuid for a given class name.
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

    try:
        event_type = EventType(class_name)
    except Exception as e:
        return EventType.NOT_SPECIFIED

    return event_type


# Setup a common interface for the event system


class PowerGraderEvent:
    def __init__(
        self, key: str, event_type: str, alternate_topic_event_type: EventType = None
    ):
        self.key = key
        self.event_type = EventType(event_type)
        if alternate_topic_event_type is not None:
            self.topic_name = get_kafka_topic_name_for_event_type(
                alternate_topic_event_type
            )
        else:
            self.topic_name = get_kafka_topic_name_for_event_type(self.event_type)

    def publish(self, producer: Producer) -> bool:
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            # producer.begin_transaction()
            producer.produce(
                self.topic_name,
                key=self.key,
                value=serialized_event,
                headers={"event_type": self.event_type.value},
            )
            # producer.flush()
            # producer.commit_transaction()
            return True

        return False

    async def publish_async(self, producer: Producer) -> bool:
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            # producer.begin_transaction()
            producer.produce(
                self.topic_name,
                key=self.key,
                value=serialized_event,
                headers={"event_type": self.event_type.value},
            )
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
            # producer.flush()
            # producer.commit_transaction()
            return True

        return False

    def _package_into_proto(self) -> object:
        pass

    def serialize(self) -> str:
        return self._package_into_proto().SerializeToString()

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
