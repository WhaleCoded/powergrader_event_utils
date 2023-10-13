from typing import Dict, List
import json

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.assignment_pb2 import (
    Assignment,
    Rubric,
    RubricCriterion,
    CriteriaLevel,
)
from google.protobuf.json_format import MessageToJson


class AssignmentEvent(PowerGraderEvent):
    def __init__(self, rubric_id: str, name: str, instructions: str) -> None:
        if rubric_id is None:
            rubric_id = ""
        if name is None:
            name = ""
        if instructions is None:
            instructions = ""

        self.proto = Assignment()
        self.proto.rubric_id = rubric_id
        self.proto.name = name
        self.proto.instructions = instructions

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT

    def get_id(self) -> str or None:
        id = self.proto.id

        if id == "":
            return None

        return id

    def get_rubric_id(self) -> str or None:
        rubric_id = self.proto.rubric_id

        if rubric_id == "":
            return None

        return rubric_id

    def get_name(self) -> str or None:
        name = self.proto.name

        if name == "":
            return None

        return name

    def get_instructions(self) -> str or None:
        instructions = self.proto.instructions

        if instructions == "":
            return None

        return instructions

    def validate(self) -> bool:
        if (
            self.get_instructions() is not None
            and self.get_name() is not None
            and self.get_rubric_id() is not None
            and self.get_id() is not None
        ):
            return True

        return False

    def _package_into_proto(self) -> Assignment:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes):
        assignment = Assignment()
        assignment.ParseFromString(event)

        if assignment.id == "":
            # This is not a valid event
            return False

        new_assignment_class = cls.__new__(cls)
        new_assignment_class.proto = assignment
        super(cls, new_assignment_class).__init__(
            key=assignment.id,
            event_type=new_assignment_class.__class__.__name__,
        )

        if new_assignment_class.validate():
            return new_assignment_class

        return False


class RubricEvent(PowerGraderEvent):
    def __init__(self, instructor_id: str, name: str, criteria: List[dict]) -> None:
        if instructor_id is None:
            raise ValueError("instructor_id cannot be None")

        self.proto = Rubric()
        self.proto.instructor_id = instructor_id
        if name is None:
            name = ""
        self.proto.name = name

        proto_criteria = self._package_criteria_into_proto(criteria)
        for name, criterion in proto_criteria.items():
            self.proto.rubric_criteria[name].CopyFrom(criterion)

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RUBRIC

    def get_instructor_id(self) -> str or None:
        instructor_id = self.proto.instructor_id

        if instructor_id == "":
            return None

        return instructor_id

    def get_id(self) -> str or None:
        id = self.proto.id

        if id == "":
            return None

        return id

    def get_name(self) -> str or None:
        name = self.proto.name

        if name == "":
            return None

        return name

    def get_criteria(self) -> Dict[str, RubricCriterion] or None:
        criteria = self.proto.rubric_criteria

        json_criteria = {}
        for name, criterion in criteria.items():
            json_str = MessageToJson(criterion)
            json_criteria[name] = json.loads(json_str)

        if len(json_criteria) == 0:
            return None

        return json_criteria

    def validate(self) -> bool:
        if (
            self.get_instructor_id() is not None
            and self.get_id() is not None
            and self.get_criteria() is not None
        ):
            # Validate the criteria
            criteria = self.get_criteria()
            for criterion in criteria.values():
                if criterion["name"] == "" or criterion["id"] == "":
                    return False

                levels = criterion["levels"]
                for level in levels:
                    if level["score"] == "" or level["description"] == "":
                        return False

            return True

        return False

    def _package_criteria_into_proto(
        self, criteria: List[dict]
    ) -> Dict[str, RubricCriterion]:
        criteria_proto = {}
        for criterion in criteria:
            criterion_proto = RubricCriterion()
            criterion_proto.name = criterion["name"]

            if "id" in criterion:
                criterion_proto.id = criterion["id"]
            else:
                criterion_proto.id = generate_event_id("RubricCriterion")

            levels = criterion["levels"]
            for level in levels:
                level_proto = CriteriaLevel()
                level_proto.score = level["score"]
                level_proto.description = level["description"]

                criterion_proto.levels.append(level_proto)

            criteria_proto[criterion_proto.name] = criterion_proto

        return criteria_proto

    def _package_into_proto(self) -> Rubric:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes):
        rubric = Rubric()
        rubric.ParseFromString(event)

        if rubric.id == "":
            # This is not a valid event
            return False

        new_rubric_class = cls.__new__(cls)
        new_rubric_class.proto = rubric

        super(cls, new_rubric_class).__init__(
            key=new_rubric_class.proto.id,
            event_type=new_rubric_class.__class__.__name__,
        )

        if new_rubric_class.validate():
            return new_rubric_class

        return False
