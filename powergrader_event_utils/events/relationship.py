from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.relationship_pb2 import (
    AssignmentAddedToCourse,
    AssignmentRemovedFromCourse,
    StudentAddedToSection,
    StudentRemovedFromSection,
    InstructorAddedToCourse,
    InstructorRemovedFromCourse,
)

from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)


@dataclass
class AssignmentAddedToCourseEvent(
    PowerGraderEvent, ProtoWrapper[AssignmentAddedToCourse]
):
    assignment_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self, assignment_public_uuid: str, course_public_uuid: str, timestamp: int
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AssignmentAddedToCourse,
            key_field_name="version_uuid",
            assignment_public_uuid=assignment_public_uuid,
            course_public_uuid=course_public_uuid,
            timestamp=timestamp,
        )

    def _package_into_proto(self) -> AssignmentAddedToCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_ADDED_TO_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "AssignmentAddedToCourseEvent":
        return general_deserialization(
            AssignmentAddedToCourse, cls, event, "assignment_public_uuid"
        )


@dataclass
class AssignmentRemovedFromCourseEvent(
    PowerGraderEvent, ProtoWrapper[AssignmentRemovedFromCourse]
):
    assignment_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self, assignment_public_uuid: str, course_public_uuid: str, timestamp: int
    ):
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AssignmentRemovedFromCourse,
            key_field_name="version_uuid",
            assignment_public_uuid=assignment_public_uuid,
            course_public_uuid=course_public_uuid,
            timestamp=timestamp,
        )

    def _package_into_proto(self) -> AssignmentRemovedFromCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_REMOVED_FROM_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "AssignmentRemovedFromCourseEvent":
        return general_deserialization(
            AssignmentRemovedFromCourse, cls, event, "assignment_public_uuid"
        )


@dataclass
class StudentAddedToSectionEvent(PowerGraderEvent, ProtoWrapper[StudentAddedToSection]):
    student_public_uuid: str
    section_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self, student_public_uuid: str, section_public_uuid: str, timestamp: int
    ):
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=StudentAddedToSection,
            key_field_name="version_uuid",
            student_public_uuid=student_public_uuid,
            section_public_uuid=section_public_uuid,
            timestamp=timestamp,
        )

    def _package_into_proto(self) -> StudentAddedToSection:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_ADDED_TO_SECTION

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentAddedToSectionEvent":
        return general_deserialization(
            StudentAddedToSection, cls, event, "student_public_uuid"
        )


@dataclass
class StudentRemovedFromSectionEvent(
    PowerGraderEvent, ProtoWrapper[StudentRemovedFromSection]
):
    student_public_uuid: str
    section_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self, student_public_uuid: str, section_public_uuid: str, timestamp: int
    ):
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=StudentRemovedFromSection,
            key_field_name="version_uuid",
            student_public_uuid=student_public_uuid,
            section_public_uuid=section_public_uuid,
            timestamp=timestamp,
        )

    def _package_into_proto(self) -> StudentRemovedFromSection:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_REMOVED_FROM_SECTION

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentRemovedFromSectionEvent":
        return general_deserialization(
            StudentRemovedFromSection, cls, event, "student_public_uuid"
        )


@dataclass
class InstructorAddedToCourseEvent(
    PowerGraderEvent, ProtoWrapper[InstructorAddedToCourse]
):
    instructor_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self, instructor_public_uuid: str, course_public_uuid: str, timestamp: int
    ):
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorAddedToCourse,
            key_field_name="version_uuid",
            instructor_public_uuid=instructor_public_uuid,
            course_public_uuid=course_public_uuid,
            timestamp=timestamp,
        )

    def _package_into_proto(self) -> InstructorAddedToCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_ADDED_TO_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorAddedToCourseEvent":
        return general_deserialization(
            InstructorAddedToCourse, cls, event, "instructor_public_uuid"
        )


@dataclass
class InstructorRemovedFromCourseEvent(
    PowerGraderEvent, ProtoWrapper[InstructorRemovedFromCourse]
):
    instructor_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self, instructor_public_uuid: str, course_public_uuid: str, timestamp: int
    ):
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorRemovedFromCourse,
            key_field_name="version_uuid",
            instructor_public_uuid=instructor_public_uuid,
            course_public_uuid=course_public_uuid,
            timestamp=timestamp,
        )

    def _package_into_proto(self) -> InstructorRemovedFromCourse:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_REMOVED_FROM_COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorRemovedFromCourseEvent":
        return general_deserialization(
            InstructorRemovedFromCourse, cls, event, "instructor_public_uuid"
        )


if __name__ == "__main__":
    assignment_added_to_course = AssignmentAddedToCourseEvent(
        assignment_public_uuid="123", course_public_uuid="123", timestamp=123
    )
    print(assignment_added_to_course.serialize())
    print(
        AssignmentAddedToCourseEvent.deserialize(assignment_added_to_course.serialize())
    )

    assignment_removed_from_course = AssignmentRemovedFromCourseEvent(
        assignment_public_uuid="123", course_public_uuid="123", timestamp=123
    )
    print(assignment_removed_from_course.serialize())
    print(
        AssignmentRemovedFromCourseEvent.deserialize(
            assignment_removed_from_course.serialize()
        )
    )

    student_added_to_section = StudentAddedToSectionEvent(
        student_public_uuid="123", section_public_uuid="123", timestamp=123
    )
    print(student_added_to_section.serialize())
    print(StudentAddedToSectionEvent.deserialize(student_added_to_section.serialize()))

    student_removed_from_section = StudentRemovedFromSectionEvent(
        student_public_uuid="123", section_public_uuid="123", timestamp=123
    )
    print(student_removed_from_section.serialize())
    print(
        StudentRemovedFromSectionEvent.deserialize(
            student_removed_from_section.serialize()
        )
    )

    instructor_added_to_course = InstructorAddedToCourseEvent(
        instructor_public_uuid="123", course_public_uuid="123", timestamp=123
    )
    print(instructor_added_to_course.serialize())
    print(
        InstructorAddedToCourseEvent.deserialize(instructor_added_to_course.serialize())
    )

    instructor_removed_from_course = InstructorRemovedFromCourseEvent(
        instructor_public_uuid="123", course_public_uuid="123", timestamp=123
    )
    print(instructor_removed_from_course.serialize())
    print(
        InstructorRemovedFromCourseEvent.deserialize(
            instructor_removed_from_course.serialize()
        )
    )
