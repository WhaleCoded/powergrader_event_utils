from dataclasses import dataclass

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


@dataclass
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
            object_to_initialize=self,
            proto_type=Student,
            key_field_name="version_uuid",
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


@dataclass
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
            object_to_initialize=self,
            proto_type=Instructor,
            key_field_name="version_uuid",
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
        public_uuid="123456",
        name="John Doe",
        email="johndoe@gmail.com",
        version_timestamp=123456,
    )
    print(student_event.serialize())
    print(StudentEvent.deserialize(student_event.serialize()))

    instructor_event = InstructorEvent(
        public_uuid="123456",
        name="Jane Doe",
        email="johndoe@gmail.com",
        version_timestamp=123456,
    )
    print(instructor_event.serialize())
    print(InstructorEvent.deserialize(instructor_event.serialize()))
