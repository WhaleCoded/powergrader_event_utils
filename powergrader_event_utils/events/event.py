from uuid import uuid4
from strenum import StrEnum
from typing import Self, List, Optional

from confluent_kafka import Producer

from powergrader_event_utils.events.proto import ProtoWrapper

MAIN_TOPIC = "main-record"

# TODO: docs


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
    SUBMISSION_FILE_GROUP = "SubmissionFileGroupEvent"

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


def get_kafka_topic_names_for_event_types(
    event_types: Optional[List[EventType]] = None,
) -> List[str]:
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
    except Exception:
        return EventType.NOT_SPECIFIED

    return event_type


class PowerGraderEvent:
    """
    A base class for all events. This class provides methods for publishing and
    serializing events. Subclasses must implement the serialize and deserialize
    methods.
    """

    key_field_name: str = None
    event_type: EventType
    topic_name: str

    def __init__(self, event_type: str):
        if self.key_field_name is None:
            raise NotImplementedError(
                "Implementations of the PowerGraderEvent class must have a key_field_name class attribute set."
            )
        self.event_type = EventType(event_type)
        self.topic_name = get_kafka_topic_name_for_event_type(self.event_type)

    def publish(self, producer: Producer) -> bool:
        """
        Publishes the event to a kafka topic. The topic name is determined by the event
        type. The event is serialized and published as a byte object.

        Args:
            producer (Producer): A kafka producer object.

        Returns:
            bool: True if the event was successfully published, False otherwise.
        """
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            producer.produce(
                self.topic_name,
                key=self.key,
                value=serialized_event,
                headers={"event_type": self.event_type.value},
            )
            return True
        return False

    async def publish_async(self, producer: Producer) -> bool:
        """
        Publishes the event to a kafka topic. The topic name is determined by the event
        type. The event is serialized and published as a byte object.

        Args:
            producer (Producer): A kafka producer object.

        Returns:
            bool: True if the event was successfully published, False otherwise.
        """
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            producer.produce(
                self.topic_name,
                key=self.key,
                value=serialized_event,
                headers={"event_type": self.event_type.value},
            )
            return True
        return False

    def publish_to_custom_topic(self, producer: Producer, topic_name: str) -> bool:
        """
        Publishes the event to a custom kafka topic. The event is serialized and published as a byte object.

        Args:
            producer (Producer): A kafka producer object.
            topic_name (str): The name of the kafka topic.

        Returns:
            bool: True if the event was successfully published, False otherwise.
        """
        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            producer.produce(
                topic_name,
                key=self.key,
                value=serialized_event,
                headers={"event_type": self.event_type},
            )
            return True
        return False

    def serialize(self) -> bytes:
        raise NotImplementedError("This method must be implemented in the subclass.")

    @classmethod
    def deserialize(cls, event: bytes) -> "PowerGraderEvent":
        raise NotImplementedError("This method must be implemented in the subclass.")


class ProtoPowerGraderEvent(PowerGraderEvent, ProtoWrapper):
    """
    A base class for all events that use protobuf serialization. This class provides
    methods for publishing and serializing events, and functionality for smoothly
    wrapping the protobuf types into nice python classes. Subclasses must set their
    `proto_type` and `key_field_name` class attributes.
    """

    def __init__(self):
        ProtoWrapper.__init__(self)
        PowerGraderEvent.__init__(self, self.__class__.__name__)

    def serialize(self) -> bytes:
        """
        Serializes the event to a bytes object, using the protobuf serialization.
        Serialization schema can be found in this objects proto_type attribute.

        Returns:
            bytes: The serialized event.
        """
        return self.proto.SerializeToString()

    @classmethod
    def deserialize(cls, event: bytes) -> Self:
        """
        Deserializes the event from a bytes object, using the protobuf deserialization.
        Deserialization schema can be found in this objects proto_type attribute.

        Args:
            event (bytes): The serialized event.

        Returns:
            ProtoPowerGraderEvent: The deserialized event.
        """
        proto = cls.proto_type()
        proto.ParseFromString(event)
        event = cls.from_proto(proto)
        return event
