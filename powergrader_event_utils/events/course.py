from typing import Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.course_pb2 import (
    Course,
    Section,
    Organization,
)


class CourseEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Course

    public_uuid: str
    version_uuid: str
    instructor_public_uuid: str
    name: str
    description: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        instructor_public_uuid: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.public_uuid = public_uuid
        self.instructor_public_uuid = instructor_public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        self.description = description
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class SectionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Section

    public_uuid: str
    version_uuid: str
    course_public_uuid: str
    name: str
    closed: bool
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        course_public_uuid: Optional[str] = None,
        name: Optional[str] = None,
        closed: Optional[bool] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        if not isinstance(closed, bool):
            raise ValueError(
                f"SectionEvent closed must be a boolean, not {type(closed)}"
            )
        super().__init__()
        self.public_uuid = public_uuid
        self.course_public_uuid = course_public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        self.closed = closed
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class OrganizationEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Organization

    public_uuid: str
    version_uuid: str
    name: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        name: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
