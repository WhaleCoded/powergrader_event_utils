from typing import Dict, List
import json
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.assignment_pb2 import (
    Assignment,
    Rubric,
    RubricCriterion as RubricCriterionProto,
    CriteriaLevel as CriteriaLevelProto,
)

from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization
from google.protobuf.json_format import MessageToJson


class AssignmentEvent(PowerGraderEvent, ProtoWrapper[Assignment]):
    id: str
    rubric_id: str
    organization_id: str
    name: str
    instructions: str

    def __init__(
        self, rubric_id: str, organization_id, name: str, instructions: str
    ) -> None:
        proto = Assignment()

        if organization_id is not None:
            proto.organization_id = organization_id

        if rubric_id is not None:
            proto.rubric_id = rubric_id

        if name is not None:
            proto.name = name

        if instructions is not None:
            proto.instructions = instructions

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Assignment, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> Assignment:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT

    @classmethod
    def deserialize(cls, event: bytes) -> "AssignmentEvent":
        return general_deserialization(Assignment, cls, event, "id")


@dataclass
class CriteriaLevel:
    score: int
    description: str


@dataclass
class RubricCriterion:
    name: str
    id: str
    levels: List[CriteriaLevel]


class RubricEvent(PowerGraderEvent, ProtoWrapper[Rubric]):
    id: str
    instructor_id: str
    name: str
    rubric_criteria: Dict[str, ProtoWrapper[RubricCriterionProto]]

    def __init__(
        self, instructor_id: str, name: str, rubric_criteria: Dict[str, RubricCriterion]
    ) -> None:
        proto = Rubric()

        if instructor_id is not None:
            proto.instructor_id = instructor_id

        if name is not None:
            proto.name = name

        if rubric_criteria is not None:
            for key, criterion in rubric_criteria.items():
                if criterion is not None:
                    crit_proto = RubricCriterionProto()

                    if criterion.name is not None:
                        crit_proto.name = criterion.name

                    if criterion.id is not None:
                        crit_proto.id = criterion.id

                    if criterion.levels is not None:
                        for level in criterion.levels:
                            if level is not None:
                                level_proto = CriteriaLevelProto()

                                if level.score is not None:
                                    level_proto.score = level.score

                                if level.description is not None:
                                    level_proto.description = level.description

                                crit_proto.levels.append(level_proto)
                    proto.rubric_criteria[key].CopyFrom(crit_proto)

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, Rubric, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> Rubric:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RUBRIC

    @classmethod
    def deserialize(cls, event: bytes) -> "RubricEvent":
        return general_deserialization(Rubric, cls, event, "id")
