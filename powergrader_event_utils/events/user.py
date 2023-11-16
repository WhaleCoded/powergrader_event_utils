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
        if not org_id or not name or not email:
            raise ValueError("org_id, name, and email are required.")

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
        return bool(
            self.get_id() and self.get_org_id() and self.get_name() and self.get_email()
        )

    def _package_into_proto(self) -> Student:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentEvent":
        data = Student()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class InstructorEvent(PowerGraderEvent):
    def __init__(self, org_id: str, name: str, email: str) -> None:
        if not org_id or not name or not email:
            raise ValueError("org_id, name, and email are required.")

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

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False
