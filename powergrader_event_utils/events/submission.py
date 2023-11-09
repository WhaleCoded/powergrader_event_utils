from typing import Dict, List

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.submission_pb2 import (
    Submission,
    SubmissionFiles,
    FileContent,
)
from google.protobuf.json_format import MessageToJson


class SubmissionFilesEvent(PowerGraderEvent):
    def __init__(self, student_id: str, file_contents: List[dict]) -> None:
        self.proto = SubmissionFiles()
        self.proto.id = generate_event_id(self.__class__.__name__)
        self.proto.student_id = student_id

        for file_content in file_contents:
            fc_proto = FileContent()
            fc_proto.file_name = file_content["file_name"]
            fc_proto.file_type = (
                file_content["file_type"]
                if file_content["file_type"] is not None
                else "",
            )
            fc_proto.content = file_content["content"]
            self.proto.file_content.append(fc_proto)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION_FILES

    def get_id(self) -> str:
        return self.proto.id

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_file_contents(self) -> list:
        # This method will return a list of dicts representing the file contents
        return [
            {
                "file_name": fc.file_name,
                "file_type": fc.file_type,
                "content": fc.content,
            }
            for fc in self.proto.file_content
        ]

    def validate(self) -> bool:
        # Validate that there's at least one file content and all necessary IDs are present.
        for fc in self.get_file_content():
            if not all([fc["file_name"], fc["file_type"], fc["content"]]):
                return False

        return bool(self.get_id() and self.get_student_id())

    def _package_into_proto(self) -> SubmissionFiles:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "SubmissionFilesEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = SubmissionFiles()
        data.ParseFromString(event)

        # Check the integrity of the deserialized data.
        if not (data.id and data.student_id and data.file_content):
            return False

        # Repackage the file_content into the required format for the wrapper.
        file_contents = [
            {
                "file_name": fc.file_name,
                "file_type": fc.file_type,
                "content": fc.content,
            }
            for fc in data.file_content
        ]

        # Create and return an event instance if validation is successful.
        instance = cls(data.id, data.student_id, file_contents)
        if instance.validate():
            return instance

        return False


class SubmissionEvent(PowerGraderEvent):
    def __init__(
        self, student_id: str, assignment_id: str, submission_files_id: str
    ) -> None:
        self.proto = Submission()
        self.proto.student_id = student_id
        self.proto.assignment_id = assignment_id
        self.proto.submission_files_id = submission_files_id

        self.proto.id = generate_event_id(self.__class__.__name__)
        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION

    def get_id(self) -> str:
        return self.proto.id

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_assignment_id(self) -> str:
        return self.proto.assignment_id

    def get_submission_files_id(self) -> List[dict]:
        return self.proto.submission_files_id

    def validate(self) -> bool:
        if not all(
            [
                self.get_id(),
                self.get_student_id(),
                self.get_assignment_id(),
                self.get_submission_files_id(),
            ]
        ):
            return False
        return True

    def _package_into_proto(self) -> Submission:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "SubmissionEvent":
        data = Submission()
        data.ParseFromString(event)

        if not data.id:
            return False
        instance = cls(data.student_id, data.assignment_id, data.submission_files_id)
        instance.proto.id = data.id  # Set ID after creating the instance
        if instance.validate():
            return instance

        return False
