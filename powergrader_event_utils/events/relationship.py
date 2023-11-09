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
        return all([self.get_public_uuid(), self.get_private_uuid()])

    def _package_into_proto(self) -> PrivateIDAddedToPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "PrivateIDAddedToPublicIDEvent":
        data = PrivateIDAddedToPublicID()
        data.ParseFromString(event)

        if not data.private_uuid or not data.public_uuid:
            return False

        instance = cls(data.private_uuid, data.public_uuid)
        if instance.validate():
            return instance

        return False


class PrivateIDRemovedFromPublicIDEvent(PowerGraderEvent):
    def __init__(self, private_uuid: str, public_uuid: str) -> None:
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
        return all([self.get_public_uuid(), self.get_private_uuid()])

    def _package_into_proto(self) -> PrivateIDRemovedFromPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "PrivateIDRemovedFromPublicIDEvent":
        data = PrivateIDRemovedFromPublicID()
        data.ParseFromString(event)

        if not data.private_uuid or not data.public_uuid:
            return False

        instance = cls(data.private_uuid, data.public_uuid)
        if instance.validate():
            return instance

        return False


class AssignmentAddedToCourseEvent(PowerGraderEvent):
    def __init__(self, assignment_id: str, course_id: str) -> None:
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
        return all([self.get_assignment_id(), self.get_course_id()])

    def _package_into_proto(self) -> AssignmentAddedToCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssignmentAddedToCourseEvent":
        data = AssignmentAddedToCourse()
        data.ParseFromString(event)

        if not data.assignment_id or not data.course_id:
            return False

        instance = cls(data.assignment_id, data.course_id)
        if instance.validate():
            return instance

        return False


class AssignmentRemovedFromCourseEvent(PowerGraderEvent):
    def __init__(self, assignment_id: str, course_id: str) -> None:
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
        return all([self.get_assignment_id(), self.get_course_id()])

    def _package_into_proto(self) -> AssignmentRemovedFromCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssignmentAddedToCourseEvent":
        data = AssignmentRemovedFromCourse()
        data.ParseFromString(event)

        if not data.assignment_id or not data.course_id:
            return False

        instance = cls(data.assignment_id, data.course_id)
        if instance.validate():
            return instance

        return False


class StudentAddedToSectionEvent(PowerGraderEvent):
    def __init__(self, student_id: str, course_id: str) -> None:
        self.proto = StudentAddedToSection()
        self.proto.student_id = student_id
        self.proto.course_id = course_id

        super().__init__(key=self.proto.student_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_ADDED_TO_SECTION

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_course_id(self) -> str:
        return self.proto.course_id

    def validate(self) -> bool:
        return all([self.get_student_id(), self.get_course_id()])

    def _package_into_proto(self) -> StudentAddedToSection:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentAddedToSectionEvent":
        data = StudentAddedToSection()
        data.ParseFromString(event)

        if not data.student_id or not data.course_id:
            return False

        instance = cls(data.student_id, data.course_id)
        if instance.validate():
            return instance

        return False


class StudentRemovedFromCourseEvent(PowerGraderEvent):
    def __init__(self, student_id: str, course_id: str) -> None:
        self.proto = StudentRemovedFromSection()
        self.proto.student_id = student_id
        self.proto.course_id = course_id

        super().__init__(key=self.proto.student_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_REMOVED_FROM_SECTION

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_course_id(self) -> str:
        return self.proto.course_id

    def validate(self) -> bool:
        return all([self.get_student_id(), self.get_course_id()])

    def _package_into_proto(self) -> StudentRemovedFromSection:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentAddedToSectionEvent":
        data = StudentRemovedFromSection()
        data.ParseFromString(event)

        if not data.student_id or not data.course_id:
            return False

        instance = cls(data.student_id, data.course_id)
        if instance.validate():
            return instance

        return False


class InstructorAddedToCourseEvent(PowerGraderEvent):
    def __init__(self, instructor_id: str, course_id: str) -> None:
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
        return all([self.get_instructor_id(), self.get_course_id()])

    def _package_into_proto(self) -> InstructorAddedToCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "InstructorAddedToCourseEvent":
        data = InstructorAddedToCourse()
        data.ParseFromString(event)

        if not data.instructor_id or not data.course_id:
            return False

        instance = cls(data.instructor_id, data.course_id)
        if instance.validate():
            return instance

        return False


class InstructorRemovedFromCourseEvent(PowerGraderEvent):
    def __init__(self, instructor_id: str, course_id: str) -> None:
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
        return all([self.get_instructor_id(), self.get_course_id()])

    def _package_into_proto(self) -> InstructorRemovedFromCourse:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorRemovedFromCourseEvent" or bool:
        data = InstructorRemovedFromCourse()
        data.ParseFromString(event)

        if not data.instructor_id or not data.course_id:
            return False

        instance = cls(data.instructor_id, data.course_id)
        if instance.validate():
            return instance

        return False
