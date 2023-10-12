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
from google.protobuf.json_format import MessageToJson


class StudentEvent(PowerGraderEvent):
    def __init__(self, org_id: str, name: str, email: str) -> None:
        self.proto = Student()
        self.proto.org_id = org_id
        self.proto.name = name
        self.proto.email = email
        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT

    def get_id(self) -> str:
        return self.proto.id

    def get_org_id(self) -> str:
        return self.proto.org_id

    def get_name(self) -> str:
        return self.proto.name

    def get_email(self) -> str:
        return self.proto.email

    def validate(self) -> bool:
        return all(
            [self.get_id(), self.get_org_id(), self.get_name(), self.get_email()]
        )

    def _package_into_proto(self) -> Student:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentEvent":
        data = Student()
        data.ParseFromString(event)

        if not data.id:
            return False

        instance = cls(data.org_id, data.name, data.email)
        instance.proto.id = data.id  # Set ID after creating the instance
        if instance.validate():
            return instance

        return False


class InstructorEvent(PowerGraderEvent):
    def __init__(self, org_id: str, name: str, email: str) -> None:
        self.proto = Instructor()
        self.proto.org_id = org_id
        self.proto.name = name
        self.proto.email = email
        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR

    def get_id(self) -> str:
        return self.proto.id

    def get_org_id(self) -> str:
        return self.proto.org_id

    def get_name(self) -> str:
        return self.proto.name

    def get_email(self) -> str:
        return self.proto.email

    def validate(self) -> bool:
        return all(
            [self.get_id(), self.get_org_id(), self.get_name(), self.get_email()]
        )

    def _package_into_proto(self) -> Instructor:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "InstructorEvent":
        data = Instructor()
        data.ParseFromString(event)

        if not data.id:
            return False

        instance = cls(data.org_id, data.name, data.email)
        instance.proto.id = data.id  # Set ID after creating the instance
        if instance.validate():
            return instance

        return False
