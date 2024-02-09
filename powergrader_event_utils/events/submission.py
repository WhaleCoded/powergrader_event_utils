from typing import List, Union
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.submission_pb2 import (
    Submission,
    SubmissionFileGroup,
    FileContent as FileContentProto,
)

from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
)


@dataclass
class FileContent(ProtoWrapper[FileContentProto]):
    file_name: str
    file_type: str
    content: bytes

    def __init__(
        self, file_name: str, file_type: str, content: Union[bytes, List[int], str]
    ) -> None:
        if isinstance(content, str):
            content = content.encode("utf-8")
        elif isinstance(content, list):
            content = bytes(content)
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=FileContentProto,
            key_field_name=None,
            is_powergrader_event=False,
            file_name=file_name,
            file_type=file_type,
            content=content,
        )


@dataclass
class SubmissionFileGroupEvent(PowerGraderEvent, ProtoWrapper[SubmissionFileGroup]):
    uuid: str
    student_public_uuid: str
    file_contents: List[FileContent]

    def __init__(
        self, student_public_uuid: str, file_contents: List[FileContent]
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=SubmissionFileGroup,
            key_field_name="uuid",
            student_public_uuid=student_public_uuid,
            file_contents=file_contents,
        )

    def _package_into_proto(self) -> SubmissionFileGroup:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION_FILES

    @classmethod
    def deserialize(cls, event: bytes) -> "SubmissionFileGroupEvent":
        return general_deserialization(SubmissionFileGroup, cls, event, "uuid")


@dataclass
class SubmissionEvent(PowerGraderEvent, ProtoWrapper[Submission]):
    public_uuid: str
    version_uuid: str
    student_public_uuid: str
    assignment_version_uuid: str
    submission_file_group_uuid: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        student_public_uuid: str,
        assignment_version_uuid: str,
        submission_file_group_uuid: str,
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=Submission,
            key_field_name="version_uuid",
            public_uuid=public_uuid,
            student_public_uuid=student_public_uuid,
            assignment_version_uuid=assignment_version_uuid,
            submission_file_group_uuid=submission_file_group_uuid,
            version_timestamp=version_timestamp,
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION

    def _package_into_proto(self) -> Submission:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "SubmissionEvent":
        return general_deserialization(Submission, cls, event, "version_uuid")


if __name__ == "__main__":
    file_content = FileContent("file_name", "file_type", b"content")

    submission_file_group = SubmissionFileGroupEvent(
        "student_public_uuid", [file_content]
    )
    print(submission_file_group.serialize())
    print(SubmissionFileGroupEvent.deserialize(submission_file_group.serialize()))

    submission = SubmissionEvent(
        "public_uuid",
        "student_public_uuid",
        "assignment_version_uuid",
        "submission_file_group_uuid",
        123,
    )
    print(submission.serialize())
    print(SubmissionEvent.deserialize(submission.serialize()))
