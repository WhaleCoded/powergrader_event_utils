from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.course_pb2 import (
    Course,
    Section,
    Organization,
)
from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)


@dataclass
class CourseEvent(PowerGraderEvent, ProtoWrapper[Course]):
    public_uuid: str
    version_uuid: str
    instructor_public_uuid: str
    name: str
    description: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        instructor_public_uuid: str,
        name: str,
        description: str,
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            self,
            Course,
            "version_uuid",
            public_uuid=public_uuid,
            instructor_public_uuid=instructor_public_uuid,
            name=name,
            description=description,
            version_timestamp=version_timestamp,
        )

    def _package_into_proto(self) -> Course:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "CourseEvent":
        return general_deserialization(Course, cls, event, "version_uuid")


@dataclass
class SectionEvent(PowerGraderEvent, ProtoWrapper[Section]):
    public_uuid: str
    version_uuid: str
    course_public_uuid: str
    name: str
    closed: bool
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        course_public_uuid: str,
        name: str,
        closed: bool,
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            self,
            Section,
            "version_uuid",
            public_uuid=public_uuid,
            course_public_uuid=course_public_uuid,
            name=name,
            closed=closed,
            version_timestamp=version_timestamp,
        )

    def _package_into_proto(self) -> Section:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SECTION

    @classmethod
    def deserialize(cls, event: bytes) -> "SectionEvent":
        return general_deserialization(Section, cls, event, "version_uuid")


@dataclass
class OrganizationEvent(PowerGraderEvent, ProtoWrapper[Organization]):
    public_uuid: str
    version_uuid: str
    name: str
    version_timestamp: int

    def __init__(self, public_uuid: str, name: str, version_timestamp: int) -> None:
        general_proto_type_init(
            self,
            Organization,
            "version_uuid",
            public_uuid=public_uuid,
            name=name,
            version_timestamp=version_timestamp,
        )

    def _package_into_proto(self) -> Organization:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ORGANIZATION

    @classmethod
    def deserialize(cls, event: bytes) -> "OrganizationEvent":
        return general_deserialization(Organization, cls, event, "version_uuid")


if __name__ == "__main__":
    course = CourseEvent(
        public_uuid="public_uuid",
        instructor_public_uuid="instructor_public_uuid",
        name="name",
        description="description",
        version_timestamp=123,
    )
    print(course.serialize())
    print(CourseEvent.deserialize(course.serialize()))

    section = SectionEvent(
        public_uuid="public_uuid",
        course_public_uuid="course_public_uuid",
        name="name",
        closed=False,
        version_timestamp=123,
    )
    print(section.serialize())
    print(SectionEvent.deserialize(section.serialize()))

    organization = OrganizationEvent(
        public_uuid="public_uuid",
        name="name",
        version_timestamp=123,
    )
    print(organization.serialize())
    print(OrganizationEvent.deserialize(organization.serialize()))
