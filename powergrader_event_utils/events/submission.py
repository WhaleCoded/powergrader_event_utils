from typing import List, Union, Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.submission_pb2 import (
    Submission,
    SubmissionFileGroup,
    FileContent as FileContentProto,
)

from powergrader_event_utils.events.proto import ProtoWrapper


class FileContent(ProtoWrapper):
    proto_type = FileContentProto

    file_name: str
    file_type: str
    content: bytes

    def __init__(
        self, file_name: str, file_type: str, content: Union[bytes, List[int], str]
    ) -> None:
        if isinstance(content, str):
            content = content.encode("utf-8")
        elif isinstance(content, list):
            try:
                content = bytes(content)
            except ValueError:
                raise ValueError(
                    "If content is a list, it must be a list of integers withing the range of 0-255"
                )
        super().__init__()
        self.file_name = file_name
        self.file_type = file_type
        self.content = content


class SubmissionFileGroupEvent(ProtoPowerGraderEvent):
    key_field_name: str = "uuid"
    proto_type = SubmissionFileGroup

    uuid: str
    student_public_uuid: str
    file_contents: List[FileContent]

    def __init__(
        self,
        student_public_uuid: Optional[str] = None,
        file_contents: Optional[List[FileContent]] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.student_public_uuid = student_public_uuid
        self.file_contents = file_contents


class SubmissionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Submission

    public_uuid: str
    version_uuid: str
    student_public_uuid: str
    assignment_version_uuid: str
    submission_file_group_uuid: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        student_public_uuid: Optional[str] = None,
        assignment_version_uuid: Optional[str] = None,
        submission_file_group_uuid: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.public_uuid = public_uuid
        self.student_public_uuid = student_public_uuid
        self.assignment_version_uuid = assignment_version_uuid
        self.submission_file_group_uuid = submission_file_group_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        if version_timestamp == None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
