from typing import Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
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
        name: Optional[str] = None,
        email: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        self.email = email
        if version_timestamp == None:
            version_timestamp = generate_event_timestamp()
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
        name: Optional[str] = None,
        email: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        self.email = email
        if version_timestamp == None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


if __name__ == "__main__":
    student = StudentEvent("123")
    print(student)
