from typing import Dict, List

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.relationship_pb2 import (
    AssignmentAddedToCourse,
    AssignmentRemovedFromCourse,
    StudentAddedToSection,
    StudentRemovedFromSection,
    InstructorAddedToCourse,
    InstructorRemovedFromCourse,
    PublicIDReferenceChanged,
)

from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


class PublicIDReferenceChangedEvent(
    PowerGraderEvent, ProtoWrapper[PublicIDReferenceChanged]
):
    id: str
    private_uuid: str
    public_uuid: str
    when: int

    def __init__(self, private_uuid: str, public_uuid: str, when: int) -> None:
        proto = PublicIDReferenceChanged()

        if private_uuid is not None:
            proto.private_uuid = private_uuid

        if public_uuid is not None:
            proto.public_uuid = public_uuid

        if when is not None:
            proto.when = when

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, PublicIDReferenceChanged, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> PublicIDReferenceChanged:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.PUBLIC_ID_REFERENCE_CHANGED

    @classmethod
    def deserialize(cls, event: bytes) -> "PublicIDReferenceChanged":
        return general_deserialization(PublicIDReferenceChanged, cls, event, "id")


class AssignmentAddedToCourseEvent(
    PowerGraderEvent, ProtoWrapper[AssignmentAddedToCourse]
):
    id: str
    assignment_id: str
    course_id: str

    def __init__(self, assignment_id: str, course_id: str) -> None:
        proto = AssignmentAddedToCourse()

        if assignment_id is not None:
            proto.assignment_id = assignment_id

        if course_id is not None:
            proto.course_id = course_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, AssignmentAddedToCourse, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> AssignmentAddedToCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_ADDED_TO_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "AssignmentAddedToCourseEvent":
        return general_deserialization(AssignmentAddedToCourse, cls, event, "id")


class AssignmentRemovedFromCourseEvent(
    PowerGraderEvent, ProtoWrapper[AssignmentRemovedFromCourse]
):
    id: str
    assignment_id: str
    course_id: str

    def __init__(self, assignment_id: str, course_id: str) -> None:
        proto = AssignmentRemovedFromCourse()

        if assignment_id is not None:
            proto.assignment_id = assignment_id

        if course_id is not None:
            proto.course_id = course_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, AssignmentRemovedFromCourse, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> AssignmentRemovedFromCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_REMOVED_FROM_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "AssignmentRemovedFromCourseEvent":
        return general_deserialization(AssignmentRemovedFromCourse, cls, event, "id")


class StudentAddedToSectionEvent(PowerGraderEvent, ProtoWrapper[StudentAddedToSection]):
    id: str
    student_id: str
    section_id: str

    def __init__(self, student_id: str, section_id: str) -> None:
        proto = StudentAddedToSection()

        if student_id is not None:
            proto.student_id = student_id

        if section_id is not None:
            proto.section_id = section_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, StudentAddedToSection, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> StudentAddedToSection:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_ADDED_TO_SECTION

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentAddedToSectionEvent":
        return general_deserialization(StudentAddedToSection, cls, event, "id")


class StudentRemovedFromSectionEvent(
    PowerGraderEvent, ProtoWrapper[StudentRemovedFromSection]
):
    id: str
    student_id: str
    section_id: str

    def __init__(self, student_id: str, section_id: str) -> None:
        proto = StudentRemovedFromSection()

        if student_id is not None:
            proto.student_id = student_id

        if section_id is not None:
            proto.section_id = section_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, StudentRemovedFromSection, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> StudentRemovedFromSection:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_REMOVED_FROM_SECTION

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentRemovedFromSectionEvent":
        return general_deserialization(StudentRemovedFromSection, cls, event, "id")


class InstructorAddedToCourseEvent(
    PowerGraderEvent, ProtoWrapper[InstructorAddedToCourse]
):
    id: str
    instructor_id: str
    course_id: str

    def __init__(self, instructor_id: str, course_id: str) -> None:
        proto = InstructorAddedToCourse()

        if instructor_id is not None:
            proto.instructor_id = instructor_id

        if course_id is not None:
            proto.course_id = course_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, InstructorAddedToCourse, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> InstructorAddedToCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_ADDED_TO_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorAddedToCourseEvent":
        return general_deserialization(InstructorAddedToCourse, cls, event, "id")


class InstructorRemovedFromCourseEvent(
    PowerGraderEvent, ProtoWrapper[InstructorRemovedFromCourse]
):
    id: str
    instructor_id: str
    course_id: str

    def __init__(self, instructor_id: str, course_id: str) -> None:
        proto = InstructorRemovedFromCourse()

        if instructor_id is not None:
            proto.instructor_id = instructor_id

        if course_id is not None:
            proto.course_id = course_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, InstructorRemovedFromCourse, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> InstructorRemovedFromCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_REMOVED_FROM_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorRemovedFromCourseEvent":
        return general_deserialization(InstructorRemovedFromCourse, cls, event, "id")
