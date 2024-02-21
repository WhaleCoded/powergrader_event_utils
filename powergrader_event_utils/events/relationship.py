from typing import Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_timestamp,
    generate_event_uuid,
)
from powergrader_event_utils.events.proto_events.relationship_pb2 import (
    AssignmentAddedToCourse,
    AssignmentRemovedFromCourse,
    StudentAddedToSection,
    StudentRemovedFromSection,
    InstructorAddedToCourse,
    InstructorRemovedFromCourse,
)


class AssignmentAddedToCourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = AssignmentAddedToCourse

    assignment_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self,
        assignment_public_uuid: str,
        course_public_uuid: str,
        timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.assignment_public_uuid = assignment_public_uuid
        self.course_public_uuid = course_public_uuid
        if timestamp == None:
            timestamp = generate_event_timestamp()
        self.timestamp = timestamp


class AssignmentRemovedFromCourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = AssignmentRemovedFromCourse

    assignment_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self,
        assignment_public_uuid: str,
        course_public_uuid: str,
        timestamp: Optional[int] = None,
    ):
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.assignment_public_uuid = assignment_public_uuid
        self.course_public_uuid = course_public_uuid
        if timestamp == None:
            timestamp = generate_event_timestamp()
        self.timestamp = timestamp


class StudentAddedToSectionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = StudentAddedToSection

    student_public_uuid: str
    section_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self,
        student_public_uuid: str,
        section_public_uuid: str,
        timestamp: Optional[int] = None,
    ):
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.student_public_uuid = student_public_uuid
        self.section_public_uuid = section_public_uuid
        if timestamp == None:
            timestamp = generate_event_timestamp()
        self.timestamp = timestamp


class StudentRemovedFromSectionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = StudentRemovedFromSection

    student_public_uuid: str
    section_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self,
        student_public_uuid: str,
        section_public_uuid: str,
        timestamp: Optional[int] = None,
    ):
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.student_public_uuid = student_public_uuid
        self.section_public_uuid = section_public_uuid
        if timestamp == None:
            timestamp = generate_event_timestamp()
        self.timestamp = timestamp


class InstructorAddedToCourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = InstructorAddedToCourse

    instructor_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self,
        instructor_public_uuid: str,
        course_public_uuid: str,
        timestamp: Optional[int] = None,
    ):
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.instructor_public_uuid = instructor_public_uuid
        self.course_public_uuid = course_public_uuid
        if timestamp == None:
            timestamp = generate_event_timestamp()
        self.timestamp = timestamp


class InstructorRemovedFromCourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = InstructorRemovedFromCourse

    instructor_public_uuid: str
    course_public_uuid: str
    timestamp: int
    version_uuid: str

    def __init__(
        self,
        instructor_public_uuid: str,
        course_public_uuid: str,
        timestamp: Optional[int] = None,
    ):
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.instructor_public_uuid = instructor_public_uuid
        self.course_public_uuid = course_public_uuid
        if timestamp == None:
            timestamp = generate_event_timestamp()
        self.timestamp = timestamp
