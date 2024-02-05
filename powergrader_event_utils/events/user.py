from typing import Dict, List
from uuid import uuid4

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.user_pb2 import (
    Student,
    Instructor,
)
from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


class StudentEvent(PowerGraderEvent, ProtoWrapper[Student]):
    public_id: str
    id: str
    organization_id: str
    name: str
    email: str
    when: int

    def __init__(
        self,
        organization_id: str,
        name: str,
        email: str,
        when: int,
        public_id: str = None,
    ) -> None:
        proto = Student()
        if organization_id is not None:
            proto.organization_id = organization_id

        if when is not None:
            proto.when = when

        if public_id is None:
            public_id = str(uuid4())
        proto.public_id = public_id

        if name is not None:
            proto.name = name

        if email is not None:
            proto.email = email

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Student, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> Student:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentEvent":
        return general_deserialization(Student, cls, event, "public_id")


class InstructorEvent(PowerGraderEvent, ProtoWrapper[Instructor]):
    public_id: str
    id: str
    organization_id: str
    name: str
    email: str
    when: int

    def __init__(
        self,
        organization_id: str,
        name: str,
        email: str,
        when: int,
        public_id: str = None,
    ) -> None:
        proto = Instructor()

        if organization_id is not None:
            proto.organization_id = organization_id

        if when is not None:
            proto.when = when

        if public_id is None:
            public_id = str(uuid4())
        proto.public_id = public_id

        if name is not None:
            proto.name = name

        if email is not None:
            proto.email = email

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Instructor, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR

    def _package_into_proto(self) -> Instructor:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorEvent":
        return general_deserialization(Instructor, cls, event, "id")
