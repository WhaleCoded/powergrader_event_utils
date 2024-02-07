from typing import Dict, List
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.assignment_pb2 import (
    Assignment,
    Rubric,
    RubricCriterion as RubricCriterionProto,
    CriterionLevel as CriterionLevelProto,
)

from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)


@dataclass
class AssignmentEvent(PowerGraderEvent, ProtoWrapper[Assignment]):
    public_uuid: str
    instructor_public_uuid: str
    version_uuid: str
    rubric_version_uuid: str
    name: str
    description: str
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        instructor_public_uuid: str,
        rubric_version_uuid: str,
        name: str,
        description: str,
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=Assignment,
            key_field_name="version_uuid",
            public_uuid=public_uuid,
            instructor_public_uuid=instructor_public_uuid,
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


@dataclass
class CriterionLevel(ProtoWrapper[CriterionLevelProto]):
    score: int
    description: str

    def __init__(self, score: int, description: str) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=CriterionLevelProto,
            key_field_name=None,
            is_powergrader_event=False,
            score=score,
            description=description,
        )


@dataclass
class RubricCriterion(ProtoWrapper[RubricCriterionProto]):
    uuid: str
    name: str
    levels: List[CriterionLevel]

    def __init__(self, uuid: str, name: str, levels: List[CriterionLevel]) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RubricCriterionProto,
            key_field_name="uuid",
            is_powergrader_event=False,
            uuid=uuid,
            name=name,
            levels=levels,
        )


@dataclass
class RubricEvent(PowerGraderEvent, ProtoWrapper[Rubric]):
    public_uuid: str
    version_uuid: str
    instructor_public_uuid: str
    name: str
    rubric_criteria: Dict[str, RubricCriterion]
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        instructor_public_uuid: str,
        name: str,
        rubric_criteria: Dict[str, RubricCriterion],
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=Rubric,
            key_field_name="version_uuid",
            public_uuid=public_uuid,
            instructor_public_uuid=instructor_public_uuid,
            name=name,
            rubric_criteria=rubric_criteria,
            version_timestamp=version_timestamp,
        )

    def _package_into_proto(self) -> Rubric:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RUBRIC

    @classmethod
    def deserialize(cls, event: bytes) -> "RubricEvent":
        return general_deserialization(Rubric, cls, event, "version_uuid")


if __name__ == "__main__":
    new_rubric = RubricEvent(
        public_uuid="123",
        instructor_public_uuid="123",
        name="test",
        rubric_criteria={
            "123": RubricCriterion("123", "test", [CriterionLevel(1, "test")])
        },
        version_timestamp=123,
    )
    print(new_rubric.serialize())
    print(RubricEvent.deserialize(new_rubric.serialize()))

    new_assignment = AssignmentEvent(
        public_uuid="123",
        rubric_version_uuid="123",
        name="test",
        description="test",
        version_timestamp=123,
    )
    print(new_assignment.serialize())
    print(AssignmentEvent.deserialize(new_assignment.serialize()))
