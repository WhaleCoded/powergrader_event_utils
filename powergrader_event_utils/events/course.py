from typing import Dict, List
from uuid import uuid4

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
from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


class CourseEvent(PowerGraderEvent, ProtoWrapper[Course]):
    public_id: str
    id: str
    organization_id: str
    instructor_id: str
    name: str
    description: str
    when: int

    def __init__(
        self,
        organization_id: str,
        instructor_id: str,
        name: str,
        description: str,
        when: int,
        public_id: str = None,
    ) -> None:
        proto = Course()

        if organization_id is not None:
            proto.organization_id = organization_id

        if instructor_id is not None:
            proto.instructor_id = instructor_id

        if name is not None:
            proto.name = name

        if description is not None:
            proto.description = description

        if when is not None:
            proto.when = when

        if public_id is None:
            public_id = str(uuid4())
        proto.public_id = public_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Course, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> Course:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.COURSE

    @classmethod
    def deserialize(cls, event: bytes) -> "CourseEvent":
        return general_deserialization(Course, cls, event, "public_id")


class SectionEvent(PowerGraderEvent, ProtoWrapper[Section]):
    public_id: str
    id: str
    course_id: str
    name: str
    is_active: bool
    when: int

    def __init__(
        self,
        course_id: str,
        name: str,
        is_active: bool,
        when: int,
        public_id: str = None,
    ) -> None:
        proto = Section()

        if course_id is not None:
            proto.course_id = course_id

        if name is not None:
            proto.name = name

        if is_active is not None:
            proto.is_active = is_active

        if when is not None:
            proto.when = when

        if public_id is None:
            public_id = str(uuid4())
        proto.public_id = public_id

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Section, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> Section:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SECTION

    @classmethod
    def deserialize(cls, event: bytes) -> "SectionEvent":
        return general_deserialization(Section, cls, event, "public_id")


class OrganizationEvent(PowerGraderEvent, ProtoWrapper[Organization]):
    id: str
    name: str
    code: str

    def __init__(self, name: str, code: str) -> None:
        proto = Organization()

        if name is not None:
            proto.name = name

        if code is not None:
            proto.code = code

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Organization, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> Organization:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ORGANIZATION

    @classmethod
    def deserialize(cls, event: bytes) -> "OrganizationEvent":
        return general_deserialization(Organization, cls, event, "id")
