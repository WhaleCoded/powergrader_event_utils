from typing import Dict, List
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.submission_pb2 import (
    Submission,
    SubmissionFiles,
    FileContent as FileContentProto,
)

from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


@dataclass
class FileContent:
    file_name: str
    file_type: str
    content: str


class SubmissionFilesEvent(PowerGraderEvent, ProtoWrapper[SubmissionFiles]):
    id: str
    student_id: str
    file_content: List[ProtoWrapper[FileContentProto]]  # List of wrapped FileContent

    def __init__(self, student_id: str, file_content: List[FileContent]) -> None:
        proto = SubmissionFiles()

        if student_id is not None:
            proto.student_id = student_id

        if file_content is not None:
            for file in file_content:
                # If at least one of the required fields is set, then add the file to the list
                if (
                    file.file_name is not None
                    or file.file_type is not None
                    or file.content is not None
                ):
                    file_proto = FileContentProto()

                    if file.file_name is not None:
                        file_proto.file_name = file.file_name

                    if file.file_type is not None:
                        file_proto.file_type = file.file_type

                    if file.content is not None:
                        file_proto.content = file.content

                    proto.file_content.append(file_proto)

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, SubmissionFiles, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> SubmissionFiles:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION_FILES

    @classmethod
    def deserialize(cls, event: bytes) -> "SubmissionFilesEvent":
        return general_deserialization(SubmissionFiles, cls, event, "id")


class SubmissionEvent(PowerGraderEvent, ProtoWrapper[Submission]):
    id: str
    student_id: str
    assignment_id: str
    submission_date: int
    submission_files_id: str
    when: int

    def __init__(
        self,
        student_id: str,
        assignment_id: str,
        submission_date: int,
        submission_files_id: str,
        when: int,
    ) -> None:
        proto = Submission()

        if student_id is not None:
            proto.student_id = student_id

        if assignment_id is not None:
            proto.assignment_id = assignment_id

        if submission_date is not None:
            proto.submission_date = submission_date

        if submission_files_id is not None:
            proto.submission_files_id = submission_files_id

        if when is not None:
            proto.when = when

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Submission, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION

    def _package_into_proto(self) -> Submission:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "SubmissionEvent":
        return general_deserialization(Submission, cls, event, "id")
