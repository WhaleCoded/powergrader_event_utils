from typing import List, Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.instructions_pb2 import (
    RegisterAssignmentInstruction,
    RegisterCriterionInstruction,
    AssignmentInstruction,
    CriterionInstruction,
    InvalidateInstruction,
    InstructionInfo as InstructionInfoProto,
)

from powergrader_event_utils.events.proto import ProtoWrapper


class InstructionInfo(ProtoWrapper):
    proto_type = InstructionInfoProto

    assignment_instruction_version_uuids: List[str]
    criterion_instruction_version_uuids: List[str]

    def __init__(
        self,
        assignment_instruction_version_uuids: List[str],
        criterion_instruction_version_uuids: List[str],
    ) -> None:
        super().__init__()
        self.assignment_instruction_version_uuids = assignment_instruction_version_uuids
        self.criterion_instruction_version_uuids = criterion_instruction_version_uuids


# Instruction Events
class RegisterAssignmentInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterAssignmentInstruction

    public_uuid: str
    assignment_version_uuid: str

    def __init__(
        self,
        assignment_version_uuid: Optional[str] = None,
        public_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid

        self.assignment_version_uuid = assignment_version_uuid


class RegisterCriterionInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterCriterionInstruction

    public_uuid: str
    assignment_version_uuid: str
    criterion_uuid: str

    def __init__(
        self,
        course_public_uuid: Optional[str] = None,
        assignment_version_uuid: Optional[str] = None,
        criterion_uuid: Optional[str] = None,
        public_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid

        self.course_public_uuid = course_public_uuid
        self.assignment_version_uuid = assignment_version_uuid
        self.criterion_uuid = criterion_uuid


class AssignmentInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = AssignmentInstruction

    public_uuid: str
    version_uuid: str
    content: str
    version_timestamp: int

    def __init__(
        self,
        content: Optional[str] = None,
        public_uuid: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)

        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
        self.content = content


class CriterionInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = CriterionInstruction

    public_uuid: str
    version_uuid: str
    content: str
    version_timestamp: int

    def __init__(
        self,
        content: Optional[str] = None,
        public_uuid: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)

        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
        self.content = content


class InvalidateInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "instruction_version_uuid"
    proto_type = InvalidateInstruction

    instruction_version_uuid: str
    is_assignment_instruction: bool

    def __init__(
        self,
        is_assignment_instruction: Optional[bool] = None,
        instruction_version_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.instruction_version_uuid = instruction_version_uuid
        self.is_assignment_instruction = is_assignment_instruction
