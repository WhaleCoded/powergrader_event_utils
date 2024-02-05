from typing import Dict, List
from enum import Enum
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)
from powergrader_event_utils.events.proto_events.assignment_pb2 import (
    AICriteriaGradingStarted,
    GradingMethod,
    Grade,
    AICriteriaGrade,
    AIInferredCriteriaGrade,
)


@dataclass
class AICriteriaGradingStartedEvent(PowerGraderEvent, ProtoWrapper[Assignment]):
    public_uuid: str
    version_uuid: str
    rubric_version_uuid: str
    name: str
    description: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        rubric_version_uuid: str,
        name: str,
        description: str,
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            self,
            Assignment,
            "version_uuid",
            public_uuid=public_uuid,
            rubric_version_uuid=rubric_version_uuid,
            name=name,
            description=description,
            version_timestamp=version_timestamp,
        )

    def _package_into_proto(self) -> Assignment:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT

    @classmethod
    def deserialize(cls, event: bytes) -> "AssignmentEvent":
        return general_deserialization(Assignment, cls, event, "version_uuid")
