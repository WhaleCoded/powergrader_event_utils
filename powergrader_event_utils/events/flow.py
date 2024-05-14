from typing import Optional, Self, List

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.flow_pb2 import (
    FlowNode as FlowNodeProto,
    FlowLog,
)

from powergrader_event_utils.events.proto import ProtoWrapper, ProtoEnumWrapper


class FlowNode(ProtoWrapper):
    proto_type = FlowNodeProto

    uuid: str
    parent_uuid: str
    content: str
    child_nodes: List[Self]

    def __init__(
        self,
        content: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        if uuid is None:
            uuid = generate_event_uuid(self.__class__.__name__)
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.content = content


class FlowLogEvent(ProtoPowerGraderEvent):
    key_field_name: str = "uuid"
    proto_type = FlowLog

    uuid: str
    name: str
    ai_grading_started_uuid: str
    nodes: List[FlowNode]

    def __init__(
        self,
        name: Optional[str] = None,
        ai_grading_started_uuid: Optional[str] = None,
        nodes: Optional[List[FlowNode]] = None,
        uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        if uuid is None:
            uuid = generate_event_uuid(self.__class__.__name__)
        self.uuid = uuid
        self.name = name
        self.ai_grading_started_uuid = ai_grading_started_uuid
        self.nodes = nodes
