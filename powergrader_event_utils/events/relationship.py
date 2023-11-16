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
    PrivateIDAddedToPublicID,
    PrivateIDRemovedFromPublicID,
)
from google.protobuf.json_format import MessageToJson


class PrivateIDAddedToPublicIDEvent(PowerGraderEvent):
    def __init__(self, private_uuid: str, public_uuid: str) -> None:
        if not private_uuid or not public_uuid:
            raise ValueError("Private ID and Public ID must be provided")

        self.proto = PrivateIDAddedToPublicID()
        self.proto.private_uuid = private_uuid
        self.proto.public_uuid = public_uuid

        super().__init__(
            key=self.proto.private_uuid, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.PRIVATE_ID_ADDED_TO_PUBLIC_ID

    def get_private_uuid(self) -> str:
        return self.proto.private_uuid

    def get_public_uuid(self) -> str:
        return self.proto.public_uuid

    def validate(self) -> bool:
        return bool(self.get_public_uuid() and self.get_private_uuid())

    def _package_into_proto(self) -> PrivateIDAddedToPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "PrivateIDAddedToPublicIDEvent":
        data = PrivateIDAddedToPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.private_uuid,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class PrivateIDRemovedFromPublicIDEvent(PowerGraderEvent):
    def __init__(self, private_uuid: str, public_uuid: str) -> None:
        if not private_uuid or not public_uuid:
            raise ValueError("Private ID and Public ID must be provided")

        self.proto = PrivateIDRemovedFromPublicID()
        self.proto.private_uuid = private_uuid
        self.proto.public_uuid = public_uuid

        super().__init__(
            key=self.proto.private_uuid, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.PRIAVTE_ID_REMOVED_FROM_PUBLIC_ID

    def get_private_uuid(self) -> str:
        return self.proto.private_uuid

    def get_public_uuid(self) -> str:
        return self.proto.public_uuid

    def validate(self) -> bool:
        return bool(self.get_public_uuid() and self.get_private_uuid())

    def _package_into_proto(self) -> PrivateIDRemovedFromPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "PrivateIDRemovedFromPublicIDEvent":
        data = PrivateIDRemovedFromPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.private_uuid,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class AssignmentAddedToCourseEvent(PowerGraderEvent):
    def __init__(self, assignment_id: str, course_id: str) -> None:
        if not assignment_id or not course_id:
            raise ValueError("Assignment ID and Course ID must be provided")

        self.proto = AssignmentAddedToCourse()
        self.proto.assignment_id = assignment_id
        self.proto.course_id = course_id

        super().__init__(
            key=self.proto.assignment_id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_ADDED_TO_COURSE

    def get_assignment_id(self) -> str:
        return self.proto.assignment_id

    def get_course_id(self) -> str:
        return self.proto.course_id

    def validate(self) -> bool:
        return bool(self.get_assignment_id() and self.get_course_id())

    def _package_into_proto(self) -> AssignmentAddedToCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssignmentAddedToCourseEvent":
        data = AssignmentAddedToCourse()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.assignment_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class AssignmentRemovedFromCourseEvent(PowerGraderEvent):
    def __init__(self, assignment_id: str, course_id: str) -> None:
        if not assignment_id or not course_id:
            raise ValueError("Assignment ID and Course ID must be provided")

        self.proto = AssignmentRemovedFromCourse()
        self.proto.assignment_id = assignment_id
        self.proto.course_id = course_id

        super().__init__(
            key=self.proto.assignment_id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_REMOVED_FROM_COURSE

    def get_assignment_id(self) -> str:
        return self.proto.assignment_id

    def get_course_id(self) -> str:
        return self.proto.course_id

    def validate(self) -> bool:
        return bool(self.get_assignment_id() and self.get_course_id())

    def _package_into_proto(self) -> AssignmentRemovedFromCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssignmentAddedToCourseEvent":
        data = AssignmentRemovedFromCourse()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.assignment_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class StudentAddedToSectionEvent(PowerGraderEvent):
    def __init__(self, student_id: str, section_id: str) -> None:
        if not student_id or not section_id:
            raise ValueError("Student ID and Section ID must be provided")

        self.proto = StudentAddedToSection()
        self.proto.student_id = student_id
        self.proto.section_id = section_id

        super().__init__(key=self.proto.student_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_ADDED_TO_SECTION

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_section_id(self) -> str:
        return self.proto.section_id

    def validate(self) -> bool:
        return bool(self.get_student_id() and self.get_section_id())

    def _package_into_proto(self) -> StudentAddedToSection:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentAddedToSectionEvent":
        data = StudentAddedToSection()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.student_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class StudentRemovedFromCourseEvent(PowerGraderEvent):
    def __init__(self, student_id: str, section_id: str) -> None:
        if not student_id or not section_id:
            raise ValueError("Student ID and Section ID must be provided")

        self.proto = StudentRemovedFromSection()
        self.proto.student_id = student_id
        self.proto.section_id = section_id

        super().__init__(key=self.proto.student_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_REMOVED_FROM_SECTION

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_section_id(self) -> str:
        return self.proto.section_id

    def validate(self) -> bool:
        return bool(self.get_student_id() and self.get_section_id())

    def _package_into_proto(self) -> StudentRemovedFromSection:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentAddedToSectionEvent":
        data = StudentRemovedFromSection()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.student_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class InstructorAddedToCourseEvent(PowerGraderEvent):
    def __init__(self, instructor_id: str, course_id: str) -> None:
        if not instructor_id or not course_id:
            raise ValueError("Instructor ID and Course ID must be provided")

        self.proto = InstructorAddedToCourse()
        self.proto.instructor_id = instructor_id
        self.proto.course_id = course_id

        super().__init__(
            key=self.proto.instructor_id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_ADDED_TO_COURSE

    def get_instructor_id(self) -> str:
        return self.proto.instructor_id

    def get_course_id(self) -> str:
        return self.proto.course_id

    def validate(self) -> bool:
        # You can add additional validation logic here if necessary
        return bool(self.get_instructor_id() and self.get_course_id())

    def _package_into_proto(self) -> InstructorAddedToCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "InstructorAddedToCourseEvent":
        data = InstructorAddedToCourse()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.instructor_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class InstructorRemovedFromCourseEvent(PowerGraderEvent):
    def __init__(self, instructor_id: str, course_id: str) -> None:
        if not instructor_id or not course_id:
            raise ValueError("Instructor ID and Course ID must be provided")

        self.proto = InstructorRemovedFromCourse()
        self.proto.instructor_id = instructor_id
        self.proto.course_id = course_id

        super().__init__(
            key=self.proto.instructor_id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_REMOVED_FROM_COURSE

    def get_instructor_id(self) -> str:
        return self.proto.instructor_id

    def get_course_id(self) -> str:
        return self.proto.course_id

    def validate(self) -> bool:
        # Validation logic to ensure instructor_id and course_id are present.
        return bool(self.get_instructor_id() and self.get_course_id())

    def _package_into_proto(self) -> InstructorRemovedFromCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorRemovedFromCourseEvent" or bool:
        data = InstructorRemovedFromCourse()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.instructor_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False
