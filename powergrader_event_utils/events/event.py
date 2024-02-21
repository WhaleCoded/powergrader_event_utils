from typing import Self, List, Optional, Sequence

import time
from uuid import uuid4
from strenum import StrEnum


from powergrader_event_utils.events.proto import ProtoWrapper

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


def generate_event_timestamp() -> int:
    """
    Generates a timestamp for the event in milliseconds since epoch.
    """

    return int(time.time_ns() / 1_000_000)


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
    key: str
    event_type: EventType
    topic_name: str

    def __init__(self, event_type: str, key: str = None):
        if self.key_field_name is None:
            raise NotImplementedError(
                "Implementations of the PowerGraderEvent class must have a key_field_name class attribute set."
            )
        self.event_type = EventType(event_type)
        self.topic_name = get_kafka_topic_name_for_event_type(self.event_type)
        if key is None:
            key = getattr(self, self.key_field_name)
        if not isinstance(key, str):
            raise TypeError(
                f"{self.__class__.__name__} key field must be of type str. Received {type(key)}"
            )
        self.key = key

    def publish(
        self,
        kafka_producer: "Producer",
        secondary_publishing_topics: Optional[List[str]] = None,
    ) -> bool:
        """
        Publishes the event to a kafka topic. The topic name is determined by the event
        type. The event is serialized and published as a byte object. Can optionally
        publish to additional user specified topics.

        Args:
            kafka_producer (Producer): A kafka producer object.
            secondary_publishing_topics (Optional[List[str]], optional): A list of
                additional topics to publish to. Defaults to None.

        Returns:
            bool: True if the event was successfully published, False otherwise.
        """
        # Before we try to start sending anything, we will do some type checking
        # First, make sure that we have a key, topic and an event type
        key = self.key
        if not isinstance(key, str):
            raise TypeError(
                f"{self.__class__.__name__} key field must be of type str. Has type {type(key)}"
            )
        topic_name = self.topic_name
        if not isinstance(topic_name, str):
            raise TypeError(
                f"{self.__class__.__name__} topic_name must be of type str. Has type {type(topic_name)}"
            )
        event_type = self.event_type
        if not isinstance(event_type, EventType):
            raise TypeError(
                f"{self.__class__.__name__} event_type must be of type EventType. Has type {type(event_type)}"
            )

        # Then, if we have secondary publishing topics, we will make sure that they are a list of strings
        if secondary_publishing_topics:
            if (
                isinstance(secondary_publishing_topics, Sequence)
                and not isinstance(secondary_publishing_topics, str)
                and not isinstance(secondary_publishing_topics, bytes)
            ):
                for topic in secondary_publishing_topics:
                    if not isinstance(topic, str):
                        raise TypeError(
                            f"secondary_publishing_topics must be a list of strings. Received {type(topic)} in list"
                        )
            else:
                raise TypeError(
                    f"secondary_publishing_topics must be a list of strings. Received {type(secondary_publishing_topics)}"
                )

        serialized_event = self.serialize()
        if isinstance(serialized_event, bytes):
            kafka_producer.produce(
                self.topic_name,
                key=key,
                value=serialized_event,
                headers={"event_type": event_type.value},
            )
            if secondary_publishing_topics:
                for topic in secondary_publishing_topics:
                    kafka_producer.produce(
                        topic,
                        key=key,
                        value=serialized_event,
                        headers={"event_type": event_type.value},
                    )
            return True
        return False

    async def publish_async(
        self,
        producer: "Producer",
        secondary_publishing_topics: Optional[List[str]] = None,
    ) -> bool:
        """
        Publishes the event to a kafka topic. The topic name is determined by the event
        type. The event is serialized and published as a byte object. Can optionally
        publish to additional user specified topics.

        Args:
            producer (Producer): A kafka producer object.
            secondary_publishing_topics (Optional[List[str]], optional): A list of
                additional topics to publish to. Defaults to None.

        Returns:
            bool: True if the event was successfully published, False otherwise.
        """
        return self.publish(producer, secondary_publishing_topics)

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

    def __init__(self, key: str = None):
        ProtoWrapper.__init__(self)
        PowerGraderEvent.__init__(self, self.__class__.__name__, key)

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


class Producer:
    """
    Mock class for kafka producer.
    """

    def produce(self, topic_name, key, value, headers):
        raise NotImplementedError(
            "This class is purely for type hinting and should not be instantiated."
        )
