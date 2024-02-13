from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
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
    key_field_name: str = "assignment_public_uuid"
    proto_type = AssignmentAddedToCourse

    assignment_public_uuid: str
    course_public_uuid: str
    timestamp: int

    def __init__(
        self, assignment_public_uuid: str, course_public_uuid: str, timestamp: int
    ) -> None:
        super().__init__()
        self.assignment_public_uuid = assignment_public_uuid
        self.course_public_uuid = course_public_uuid
        self.timestamp = timestamp


class AssignmentRemovedFromCourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "assignment_public_uuid"
    proto_type = AssignmentRemovedFromCourse

    assignment_public_uuid: str
    course_public_uuid: str
    timestamp: int

    def __init__(
        self, assignment_public_uuid: str, course_public_uuid: str, timestamp: int
    ):
        super().__init__()
        self.assignment_public_uuid = assignment_public_uuid
        self.course_public_uuid = course_public_uuid
        self.timestamp = timestamp


class StudentAddedToSectionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "student_public_uuid"
    proto_type = StudentAddedToSection

    student_public_uuid: str
    section_public_uuid: str
    timestamp: int

    def __init__(
        self, student_public_uuid: str, section_public_uuid: str, timestamp: int
    ):
        super().__init__()
        self.student_public_uuid = student_public_uuid
        self.section_public_uuid = section_public_uuid
        self.timestamp = timestamp


class StudentRemovedFromSectionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "student_public_uuid"
    proto_type = StudentRemovedFromSection

    student_public_uuid: str
    section_public_uuid: str
    timestamp: int

    def __init__(
        self, student_public_uuid: str, section_public_uuid: str, timestamp: int
    ):
        super().__init__()
        self.student_public_uuid = student_public_uuid
        self.section_public_uuid = section_public_uuid
        self.timestamp = timestamp


class InstructorAddedToCourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "instructor_public_uuid"
    proto_type = InstructorAddedToCourse

    instructor_public_uuid: str
    course_public_uuid: str
    timestamp: int

    def __init__(
        self, instructor_public_uuid: str, course_public_uuid: str, timestamp: int
    ):
        super().__init__()
        self.instructor_public_uuid = instructor_public_uuid
        self.course_public_uuid = course_public_uuid
        self.timestamp = timestamp


class InstructorRemovedFromCourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "instructor_public_uuid"
    proto_type = InstructorRemovedFromCourse

    instructor_public_uuid: str
    course_public_uuid: str
    timestamp: int

    def __init__(
        self, instructor_public_uuid: str, course_public_uuid: str, timestamp: int
    ):
        super().__init__()
        self.instructor_public_uuid = instructor_public_uuid
        self.course_public_uuid = course_public_uuid
        self.timestamp = timestamp
