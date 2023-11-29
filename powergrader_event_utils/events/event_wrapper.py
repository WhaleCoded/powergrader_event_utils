from typing import Type

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
    deserialize_powergrader_event,
)
from powergrader_event_utils.events.proto_events.event_wrapper_pb2 import (
    Retry,
    DeadLetter,
)
from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


def convert_event_type_to_member_name(event_type: EventType) -> str:
    if event_type == EventType.RETRY or event_type == EventType.DEAD_LETTER:
        raise ValueError("You can put a retry or dead letter event into a retry event.")
    elif event_type == EventType.ASSIGNMENT:
        member_name = "assignment"
    elif event_type == EventType.RUBRIC:
        member_name = "rubric"
    elif event_type == EventType.COURSE:
        member_name = "course"
    elif event_type == EventType.SECTION:
        member_name = "section"
    elif event_type == EventType.ORGANIZATION:
        member_name = "organization"
    elif event_type == EventType.CRITERIA_GRADE:
        member_name = "criteria_grade"
    elif event_type == EventType.CRITERIA_GRADE_EMBEDDING:
        member_name = "criteria_grade_embedding"
    elif event_type == EventType.ASSESSMENT_SIMILARITY:
        member_name = "assessment_similarity"
    elif event_type == EventType.STUDENT_REQUESTED_REGRADE:
        member_name = "student_requested_regrade"
    elif event_type == EventType.GRADING_STARTED:
        member_name = "grading_started"
    elif event_type == EventType.INSTRUCTOR_REVIEW:
        member_name = "instructor_review"
    elif event_type == EventType.COURSE_PUBLIC_ID:
        member_name = "register_course_public_id"
    elif event_type == EventType.SECTION_PUBLIC_ID:
        member_name = "register_section_public_id"
    elif event_type == EventType.INSTRUCTOR_PUBLIC_ID:
        member_name = "register_instructor_public_id"
    elif event_type == EventType.STUDENT_PUBLIC_ID:
        member_name = "register_student_public_id"
    elif event_type == EventType.ASSIGNMENT_PUBLIC_ID:
        member_name = "register_assignment_public_id"
    elif event_type == EventType.RUBRIC_PUBLIC_ID:
        member_name = "register_rubric_public_id"
    elif event_type == EventType.SUBMISSION_PUBLIC_ID:
        member_name = "register_submission_public_id"
    elif event_type == EventType.PUBLISHED_TO_LMS:
        member_name = "published_to_lms"
    elif event_type == EventType.PUBLISHED_GRADE_TO_LMS:
        member_name = "published_grade_to_lms"
    elif event_type == EventType.PUBLIC_ID_REFERENCE_CHANGED:
        member_name = "public_id_reference_change"
    elif event_type == EventType.ASSIGNMENT_ADDED_TO_COURSE:
        member_name = "assignment_added_to_course"
    elif event_type == EventType.ASSIGNMENT_REMOVED_FROM_COURSE:
        member_name = "assignment_removed_from_course"
    elif event_type == EventType.STUDENT_ADDED_TO_SECTION:
        member_name = "student_added_to_section"
    elif event_type == EventType.STUDENT_REMOVED_FROM_SECTION:
        member_name = "student_removed_from_section"
    elif event_type == EventType.INSTRUCTOR_ADDED_TO_COURSE:
        member_name = "instructor_added_to_course"
    elif event_type == EventType.INSTRUCTOR_REMOVED_FROM_COURSE:
        member_name = "instructor_removed_from_course"
    elif event_type == EventType.SUBMISSION:
        member_name = "submission"
    elif event_type == EventType.SUBMISSION_FILES:
        member_name = "submission_files"
    elif event_type == EventType.STUDENT:
        member_name = "student"
    elif event_type == EventType.INSTRUCTOR:
        member_name = "instructor"
    else:
        raise ValueError(
            "The event type provided can not be packaged into a retry event."
        )

    return member_name


def convert_member_name_to_event_type(member_name: str) -> EventType:
    if member_name == "assignment":
        event_type = EventType.ASSIGNMENT
    elif member_name == "rubric":
        event_type = EventType.RUBRIC
    elif member_name == "course":
        event_type = EventType.COURSE
    elif member_name == "section":
        event_type = EventType.SECTION
    elif member_name == "organization":
        event_type = EventType.ORGANIZATION
    elif member_name == "criteria_grade":
        event_type = EventType.CRITERIA_GRADE
    elif member_name == "criteria_grade_embedding":
        event_type = EventType.CRITERIA_GRADE_EMBEDDING
    elif member_name == "assessment_grade_similarity":
        event_type = EventType.ASSESSMENT_SIMILARITY
    elif member_name == "student_requested_regrade":
        event_type = EventType.STUDENT_REQUESTED_REGRADE
    elif member_name == "grading_started":
        event_type = EventType.GRADING_STARTED
    elif member_name == "instructor_review":
        event_type = EventType.INSTRUCTOR_REVIEW
    elif member_name == "register_course_public_id":
        event_type = EventType.COURSE_PUBLIC_ID
    elif member_name == "register_section_public_id":
        event_type = EventType.SECTION_PUBLIC_ID
    elif member_name == "register_instructor_public_id":
        event_type = EventType.INSTRUCTOR_PUBLIC_ID
    elif member_name == "register_student_public_id":
        event_type = EventType.STUDENT_PUBLIC_ID
    elif member_name == "register_assignment_public_id":
        event_type = EventType.ASSIGNMENT_PUBLIC_ID
    elif member_name == "register_rubric_public_id":
        event_type = EventType.RUBRIC_PUBLIC_ID
    elif member_name == "register_submission_public_id":
        event_type = EventType.SUBMISSION_PUBLIC_ID
    elif member_name == "published_to_lms":
        event_type = EventType.PUBLISHED_TO_LMS
    elif member_name == "published_grade_to_lms":
        event_type = EventType.PUBLISHED_GRADE_TO_LMS
    elif member_name == "public_id_reference_change":
        event_type = EventType.PUBLIC_ID_REFERENCE_CHANGED
    elif member_name == "assignment_added_to_course":
        event_type = EventType.ASSIGNMENT_ADDED_TO_COURSE
    elif member_name == "assignment_removed_from_course":
        event_type = EventType.ASSIGNMENT_REMOVED_FROM_COURSE
    elif member_name == "student_added_to_section":
        event_type = EventType.STUDENT_ADDED_TO_SECTION
    elif member_name == "student_removed_from_section":
        event_type = EventType.STUDENT_REMOVED_FROM_SECTION
    elif member_name == "instructor_added_to_course":
        event_type = EventType.INSTRUCTOR_ADDED_TO_COURSE
    elif member_name == "instructor_removed_from_course":
        event_type = EventType.INSTRUCTOR_REMOVED_FROM_COURSE
    elif member_name == "submission":
        event_type = EventType.SUBMISSION
    elif member_name == "submission_files":
        event_type = EventType.SUBMISSION_FILES
    elif member_name == "student":
        event_type = EventType.STUDENT
    elif member_name == "instructor":
        event_type = EventType.INSTRUCTOR
    else:
        raise ValueError(
            "The member name provided does not correspond to a valid event type."
        )

    return event_type


class RetryEvent(PowerGraderEvent):
    retry_number: int
    retry_reason: str
    event: PowerGraderEvent

    def __init__(
        self, retry_number: int, retry_reason: str, event: PowerGraderEvent
    ) -> None:
        if not isinstance(event, PowerGraderEvent):
            raise ValueError("The event you are trying to put into a retry is invalid.")

        self.proto = Retry()

        if retry_number is not None:
            self.proto.retry_number = retry_number
            self.retry_number = retry_number

        if retry_reason is not None:
            self.proto.retry_reason = retry_reason
            self.retry_reason = retry_reason

        if event is not None:
            self._put_event_into_proto(event)
            self.event = event

        super().__init__(key=str(event.key), event_type=self.__class__.__name__)

    def _put_event_into_proto(self, event: PowerGraderEvent) -> None:
        """
        This will put the event into the correct oneof field in the protobuf message. It will throw an exception if something about the event was malformed.
        """

        # Find the correct member
        event_type = event.get_event_type()
        member_name = convert_event_type_to_member_name(event_type)

        # Fill the member with the event
        member_field = self.proto.__getattribute__(member_name)
        member_field.CopyFrom(event.proto)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RETRY

    def _package_into_proto(self) -> Retry:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RetryEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = Retry()
        data.ParseFromString(event)
        # Extract the event object and package it
        event_member_name = data.WhichOneof("event")
        if event_member_name is None:
            return None
        event_bytes = data.__getattribute__(event_member_name).SerializeToString()
        powergrader_event_type = convert_member_name_to_event_type(event_member_name)
        packaged_event, _ = deserialize_powergrader_event(
            powergrader_event_type.value.encode("utf-8"), event_bytes
        )

        new_retry_instance = cls.__new__(cls)
        new_retry_instance.proto = data
        new_retry_instance.event = packaged_event
        new_retry_instance.retry_number = data.retry_number
        new_retry_instance.retry_reason = data.retry_reason
        super(cls, new_retry_instance).__init__(
            key=packaged_event.key,
            event_type=new_retry_instance.__class__.__name__,
        )

        return new_retry_instance


class DeadLetterEvent(PowerGraderEvent):
    dead_letter_reason: str
    event: PowerGraderEvent

    def __init__(self, dead_letter_reason: str, event: PowerGraderEvent) -> None:
        if not isinstance(event, PowerGraderEvent):
            raise ValueError("The event you are trying to put into a retry is invalid.")

        self.proto = DeadLetter()

        if dead_letter_reason is not None:
            self.proto.dead_letter_reason = dead_letter_reason
            self.dead_letter_reason = dead_letter_reason

        if event is not None:
            self._put_event_into_proto(event)
            self.event = event

        super().__init__(key=str(event.key), event_type=self.__class__.__name__)

    def _put_event_into_proto(self, event: PowerGraderEvent) -> None:
        """
        This will put the event into the correct oneof field in the protobuf message. It will throw an exception if something about the event was malformed.
        """

        # Find the correct member
        event_type = event.get_event_type()
        member_name = convert_event_type_to_member_name(event_type)

        # Fill the member with the event
        member_field = self.proto.__getattribute__(member_name)
        member_field.CopyFrom(event.proto)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.DEAD_LETTER

    def _package_into_proto(self) -> DeadLetter:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "DeadLetterEvent":
        # Deserialize the event bytes back to a protobuf message.
        data = DeadLetter()
        data.ParseFromString(event)

        # Extract the event object and package it
        event_member_name = data.WhichOneof("event")
        if event_member_name is None:
            return None

        event_bytes = data.__getattribute__(event_member_name).SerializeToString()
        powergrader_event_type = convert_member_name_to_event_type(event_member_name)
        packaged_event, _ = deserialize_powergrader_event(
            powergrader_event_type.value.encode("utf-8"), event_bytes
        )

        new_dead_letter_instance = cls.__new__(cls)
        new_dead_letter_instance.proto = data
        new_dead_letter_instance.event = packaged_event
        new_dead_letter_instance.dead_letter_reason = data.dead_letter_reason
        super(cls, new_dead_letter_instance).__init__(
            key=packaged_event.key,
            event_type=new_dead_letter_instance.__class__.__name__,
        )

        return new_dead_letter_instance
