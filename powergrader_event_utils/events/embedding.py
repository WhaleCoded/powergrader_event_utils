from typing import List, Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.grade_pb2 import (
    CriterionGradeEmbedding,
    SubmissionEmbedding,
    CriterionEmbedding,
)


class CriterionGradeEmbeddingEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = CriterionGradeEmbedding

    version_uuid: str
    criterion_grade_version_uuid: str
    embedder_uuid: str
    embedding: List[float]
    version_timestamp: int

    def __init__(
        self,
        criterion_grade_version_uuid: str,
        embedder_uuid: str,
        embedding: List[float],
        version_timestamp: Optional[int] = None,
    ) -> None:
        if len(embedding) == 0:
            raise ValueError(
                f"{self.__class__.__name__} embedding must have at least one element"
            )
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.criterion_grade_version_uuid = criterion_grade_version_uuid
        self.embedder_uuid = embedder_uuid
        self.embedding = embedding
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class SubmissionEmbeddingEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = SubmissionEmbedding

    version_uuid: str
    submission_version_uuid: str
    embedder_uuid: str
    embedding: List[float]
    version_timestamp: int

    def __init__(
        self,
        submission_version_uuid: str,
        embedder_uuid: str,
        embedding: List[float],
        version_timestamp: Optional[int] = None,
    ) -> None:
        if len(embedding) == 0:
            raise ValueError(
                f"{self.__class__.__name__} embedding must have at least one element"
            )
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.submission_version_uuid = submission_version_uuid
        self.embedder_uuid = embedder_uuid
        self.embedding = embedding
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class CriterionEmbeddingEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = CriterionEmbedding

    version_uuid: str
    criterion_version_uuid: str
    embedder_uuid: str
    embedding: List[float]
    version_timestamp: int

    def __init__(
        self,
        criterion_version_uuid: str,
        embedder_uuid: str,
        embedding: List[float],
        version_timestamp: Optional[int] = None,
    ) -> None:
        if len(embedding) == 0:
            raise ValueError(
                f"{self.__class__.__name__} embedding must have at least one element"
            )
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.criterion_version_uuid = criterion_version_uuid
        self.embedder_uuid = embedder_uuid
        self.embedding = embedding
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
