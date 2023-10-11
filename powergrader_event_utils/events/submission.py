from typing import Dict, List

from powergrader_event_utils.events.base import PowerGraderEvent, generate_event_id
from powergrader_event_utils.events.proto_events.submission_pb2 import (
    Submission,
    FileContent,
)
from google.protobuf.json_format import MessageToJson


class SubmissionEvent(PowerGraderEvent):
    def __init__(
        self, student_id: str, assignment_id: str, file_contents: List[dict]
    ) -> None:
        self.proto = Submission()
        self.proto.student_id = student_id
        self.proto.assignment_id = assignment_id

        for file_content in file_contents:
            fc_proto = FileContent()
            fc_proto.file_name = file_content["file_name"]
            fc_proto.file_type = (
                file_content["file_type"]
                if file_content["file_type"] is not None
                else ""
            )
            fc_proto.content = file_content["content"]
            self.proto.file_content.append(fc_proto)

        self.proto.id = generate_event_id(self.__class__.__name__)
        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    def get_id(self) -> str:
        return self.proto.id

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_assignment_id(self) -> str:
        return self.proto.assignment_id

    def get_file_content(self) -> List[dict]:
        return [
            {
                "file_name": fc.file_name,
                "file_type": fc.file_type,
                "content": fc.content,
            }
            for fc in self.proto.file_content
        ]

    def validate(self) -> bool:
        if not all([self.get_id(), self.get_student_id(), self.get_assignment_id()]):
            return False
        for fc in self.get_file_content():
            if not all([fc["file_name"], fc["file_type"], fc["content"]]):
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

        file_contents = [
            {
                "file_name": fc.file_name,
                "file_type": fc.file_type,
                "content": fc.content,
            }
            for fc in data.file_content
        ]
        instance = cls(data.student_id, data.assignment_id, file_contents)
        instance.proto.id = data.id  # Set ID after creating the instance
        if instance.validate():
            return instance

        return False
