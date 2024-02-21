from typing import Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.artifacts_pb2 import (
    AssignmentArtifact,
    SubmissionArtifact,
    CriterionArtifact,
    GradeArtifact,
    ArtifactLog,
)


class AssignmentArtifactEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = AssignmentArtifact

    version_uuid: str
    assignment_version_uuid: str
    artifact: str
    version_timestamp: int

    def __init__(
        self,
        assignment_version_uuid: str,
        artifact: str,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.assignment_version_uuid = assignment_version_uuid
        self.artifact = artifact
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class SubmissionArtifactEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = SubmissionArtifact

    version_uuid: str
    submission_version_uuid: str
    artifact: str
    version_timestamp: int

    def __init__(
        self,
        submission_version_uuid: str,
        artifact: str,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.submission_version_uuid = submission_version_uuid
        self.artifact = artifact
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class CriterionArtifactEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = CriterionArtifact

    version_uuid: str
    criterion_version_uuid: str
    artifact: str
    version_timestamp: int

    def __init__(
        self,
        criterion_version_uuid: str,
        artifact: str,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.criterion_version_uuid = criterion_version_uuid
        self.artifact = artifact
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class GradeArtifactEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = GradeArtifact

    version_uuid: str
    grade_version_uuid: str
    artifact: str
    version_timestamp: int

    def __init__(
        self,
        grade_version_uuid: str,
        artifact: str,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.grade_version_uuid = grade_version_uuid
        self.artifact = artifact
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class ArtifactLogEvent(ProtoPowerGraderEvent):
    key_field_name: str = "artifact_version_uuid"
    proto_type = ArtifactLog

    artifact_version_uuid: str
    log: str

    def __init__(
        self,
        artifact_version_uuid: str,
        log: str,
    ) -> None:
        super().__init__()
        self.artifact_version_uuid = artifact_version_uuid
        self.log = log
