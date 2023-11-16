from typing import Dict, List

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.course_pb2 import (
    Course,
    Section,
    Organization,
)
from google.protobuf.json_format import MessageToJson


class CourseEvent(PowerGraderEvent):
    def __init__(
        self, organization_id: str, instructor_id: str, name: str, description: str
    ) -> None:
        if not organization_id or not instructor_id:
            raise ValueError("Organization ID and Instructor ID must be provided")

        if description is None:
            description = ""

        self.proto = Course()
        self.proto.instructor_id = instructor_id
        self.proto.organization_id = organization_id
        self.proto.name = name
        self.proto.description = description

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.COURSE

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_organization_id(self) -> str or None:
        organization_id = self.proto.organization_id
        return organization_id if organization_id != "" else None

    def get_instructor_id(self) -> str or None:
        instructor_id = self.proto.instructor_id
        return instructor_id if instructor_id != "" else None

    def get_name(self) -> str or None:
        name = self.proto.name
        return name if name != "" else None

    def get_description(self) -> str or None:
        description = self.proto.description
        return description if description != "" else None

    def validate(self) -> bool:
        return bool(
            self.get_instructor_id() and self.get_organization_id() and self.get_id()
        )

    def _package_into_proto(self) -> Course:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "CourseEvent":
        course = Course()
        course.ParseFromString(event)

        new_course_class = cls.__new__(cls)
        new_course_class.proto = course
        super(cls, new_course_class).__init__(
            key=course.id,
            event_type=new_course_class.__class__.__name__,
        )

        if new_course_class.validate():
            return new_course_class

        return False


class SectionEvent(PowerGraderEvent):
    def __init__(self, course_id: str, name: str) -> None:
        if not course_id:
            raise ValueError("Course ID must be provided")
        self.proto = Section()
        self.proto.course_id = course_id
        self.proto.name = name

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SECTION

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_course_id(self) -> str or None:
        course_id = self.proto.course_id
        return course_id if course_id != "" else None

    def get_name(self) -> str or None:
        name = self.proto.name
        return name if name != "" else None

    def validate(self) -> bool:
        return bool(self.get_id() and self.get_course_id())

    def _package_into_proto(self) -> Section:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "SectionEvent":
        section = Section()
        section.ParseFromString(event)

        new_section_instance = cls.__new__(cls)
        new_section_instance.proto = section
        super(cls, new_section_instance).__init__(
            key=section.id,
            event_type=new_section_instance.__class__.__name__,
        )

        if new_section_instance.validate():
            return new_section_instance

        return False


class OrganizationEvent(PowerGraderEvent):
    def __init__(self, name: str, code: str) -> None:
        if code is None:
            code = ""

        self.proto = Organization()
        self.proto.name = name
        self.proto.code = code

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ORGANIZATION

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_name(self) -> str or None:
        name = self.proto.name
        return name if name != "" else None

    def get_code(self) -> str or None:
        code = self.proto.code
        return code if code != "" else None

    def validate(self) -> bool:
        return bool(self.get_id() and self.get_name())

    def _package_into_proto(self) -> Organization:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "OrganizationEvent":
        organization = Organization()
        organization.ParseFromString(event)

        new_organization_instance = cls.__new__(cls)
        new_organization_instance.proto = organization
        super(cls, new_organization_instance).__init__(
            key=organization.id,
            event_type=new_organization_instance.__class__.__name__,
        )

        if new_organization_instance.validate():
            return new_organization_instance

        return False
