from typing import Dict, List

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.user_pb2 import (
    Student,
    Instructor,
)
from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


class StudentEvent(PowerGraderEvent, ProtoWrapper[Student]):
    id: str
    org_id: str
    name: str
    email: str

    def __init__(self, org_id: str, name: str, email: str) -> None:
        proto = Student()
        if org_id is not None:
            proto.org_id = org_id

        if name is not None:
            proto.name = name

        if email is not None:
            proto.email = email

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Student, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> Student:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentEvent":
        return general_deserialization(Student, cls, event, "id")


class InstructorEvent(PowerGraderEvent, ProtoWrapper[Instructor]):
    id: str
    org_id: str
    name: str
    email: str

    def __init__(self, org_id: str, name: str, email: str) -> None:
        proto = Instructor()

        if org_id is not None:
            proto.org_id = org_id

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
