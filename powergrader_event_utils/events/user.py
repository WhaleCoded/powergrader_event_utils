from dataclasses import dataclass

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
)
from powergrader_event_utils.events.proto_events.user_pb2 import (
    Student,
    Instructor,
)


class StudentEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Student

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
        super().__init__()
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        self.email = email
        self.version_timestamp = version_timestamp


class InstructorEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Instructor

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
        super().__init__()
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        self.email = email
        self.version_timestamp = version_timestamp
