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
from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)


class StudentEvent(PowerGraderEvent, ProtoWrapper[Student]):
    public_uuid: str
    version_uuid: str
    name: str
    email: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        name: str,
        email: str,
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            self,
            Student,
            "version_uuid",
            public_uuid=public_uuid,
            name=name,
            email=email,
            version_timestamp=version_timestamp,
        )

    def _package_into_proto(self) -> Student:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentEvent":
        return general_deserialization(Student, cls, event, "version_uuid")


class InstructorEvent(PowerGraderEvent, ProtoWrapper[Instructor]):
    public_uuid: str
    version_uuid: str
    name: str
    email: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        name: str,
        email: str,
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            self,
            Instructor,
            "version_uuid",
            public_uuid=public_uuid,
            name=name,
            email=email,
            version_timestamp=version_timestamp,
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR

    def _package_into_proto(self) -> Instructor:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorEvent":
        return general_deserialization(Instructor, cls, event, "version_uuid")


if __name__ == "__main__":
    student_event = StudentEvent(
        public_uuid=str(uuid4()), name="John Doe", email="johndoe@gmail.com"
    )
    print(student_event.serialize())
    print(StudentEvent.deserialize(student_event.serialize()))

    instructor_event = InstructorEvent(
        public_uuid=str(uuid4()), name="John Doe", email="johndoe@gmail.com"
    )
    print(instructor_event.serialize())
    print(InstructorEvent.deserialize(instructor_event.serialize()))
