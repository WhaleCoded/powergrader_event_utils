from typing import Dict, List, Sequence, Union, Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.assignment_pb2 import (
    Assignment,
    Rubric,
    RubricCriterion as RubricCriterionProto,
    CriterionLevel as CriterionLevelProto,
)

from powergrader_event_utils.events.proto import ProtoWrapper


class AssignmentEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Assignment

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
        instructor_public_uuid: Optional[str] = None,
        rubric_version_uuid: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.public_uuid = public_uuid
        self.instructor_public_uuid = instructor_public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.rubric_version_uuid = rubric_version_uuid
        self.name = name
        self.description = description
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp


class CriterionLevel(ProtoWrapper):
    proto_type = CriterionLevelProto

    score: int
    description: str

    def __init__(self, score: int, description: str) -> None:
        super().__init__()
        self.score = score
        self.description = description


class RubricCriterion(ProtoWrapper):
    proto_type = RubricCriterionProto

    uuid: str
    name: str
    levels: List[CriterionLevel]

    def __init__(
        self, name: Optional[str] = None, levels: Optional[List[CriterionLevel]] = None
    ) -> None:
        if not all(isinstance(level, CriterionLevel) for level in levels):
            raise ValueError("RubricCriterion levels must be CriterionLevel")

        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.name = name
        self.levels = levels


class RubricEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = Rubric

    public_uuid: str
    version_uuid: str
    instructor_public_uuid: str
    name: str
    rubric_criteria: Dict[str, RubricCriterion]
    version_timestamp: int

    def __init__(
        self,
        public_uuid: str,
        instructor_public_uuid: Optional[str] = None,
        name: Optional[str] = None,
        rubric_criteria: Optional[
            Union[Dict[str, RubricCriterion], Sequence[RubricCriterion]]
        ] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        if isinstance(rubric_criteria, Sequence) and not isinstance(
            rubric_criteria, str
        ):
            rubric_criteria_dictionary = {}
            for criterion in rubric_criteria:
                try:
                    criterion_name = criterion.name
                except AttributeError:
                    raise ValueError(
                        f"Rubric received a list of RubricCriterion, but one or more elements were not RubricCriterion. Received {type(criterion)}"
                    )
                if criterion_name in rubric_criteria_dictionary:
                    raise ValueError(
                        f"Rubric received multiple criteria with the same name: {criterion.name}. Each criterion must have a unique name."
                    )
                rubric_criteria_dictionary[criterion_name] = criterion
            rubric_criteria = rubric_criteria_dictionary
        if len(rubric_criteria) < 1:
            raise ValueError("Rubric must have at least one criterion")
        for criterion in rubric_criteria.values():
            if not isinstance(criterion, RubricCriterion):
                raise ValueError(
                    f"rubric_criteria must be a list or dictionary of RubricCriterion. Received {type(criterion)}"
                )
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.instructor_public_uuid = instructor_public_uuid
        self.name = name
        self.rubric_criteria = rubric_criteria
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
