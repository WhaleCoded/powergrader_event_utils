from typing import Dict, List

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.relationship_pb2 import (
    AssignmentAddedToClass,
    AssignmentRemovedFromClass,
    StudentAddedToClass,
    StudentRemovedFromClass,
    PublicUuidRegistered,
)
from google.protobuf.json_format import MessageToJson


class PublicUuidRegisteredEvent(PowerGraderEvent):
    def __init__(self, public_uuid: str, private_uuid: str) -> None:
        self.proto = PublicUuidRegistered()
        self.proto.public_uuid = public_uuid
        self.proto.private_uuid = private_uuid

        super().__init__(key=self.proto.public_uuid, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.PUBLIC_UUID_REGISTERED

    def get_public_uuid(self) -> str:
        return self.proto.public_uuid

    def get_private_uuid(self) -> str:
        return self.proto.private_uuid

    def validate(self) -> bool:
        return self.get_private_uuid() != "" and self.get_public_uuid() != ""

    def _package_into_proto(self) -> PublicUuidRegistered:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "PublicUuidRegisteredEvent":
        data = PublicUuidRegistered()
        data.ParseFromString(event)

        if not data.public_uuid or not data.private_uuid:
            return False

        instance = cls(data.public_uuid, data.private_uuid)
        if instance.validate():
            return instance

        return False


class AssignmentAddedToClassEvent(PowerGraderEvent):
    def __init__(self, assignment_id: str, class_id: str) -> None:
        self.proto = AssignmentAddedToClass()
        self.proto.assignment_id = assignment_id
        self.proto.class_id = class_id

        super().__init__(
            key=self.proto.assignment_id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_ADDED_TO_CLASS

    def get_assignment_id(self) -> str:
        return self.proto.assignment_id

    def get_class_id(self) -> str:
        return self.proto.class_id

    def validate(self) -> bool:
        return all([self.get_assignment_id(), self.get_class_id()])

    def _package_into_proto(self) -> AssignmentAddedToClass:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssignmentAddedToClassEvent":
        data = AssignmentAddedToClass()
        data.ParseFromString(event)

        if not data.assignment_id or not data.class_id:
            return False

        instance = cls(data.assignment_id, data.class_id)
        if instance.validate():
            return instance

        return False


class AssignmentRemovedFromClassEvent(PowerGraderEvent):
    def __init__(self, assignment_id: str, class_id: str) -> None:
        self.proto = AssignmentRemovedFromClass()
        self.proto.assignment_id = assignment_id
        self.proto.class_id = class_id

        super().__init__(
            key=self.proto.assignment_id, event_type=self.__class__.__name__
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_REMOVED_FROM_CLASS

    def get_assignment_id(self) -> str:
        return self.proto.assignment_id

    def get_class_id(self) -> str:
        return self.proto.class_id

    def validate(self) -> bool:
        return all([self.get_assignment_id(), self.get_class_id()])

    def _package_into_proto(self) -> AssignmentRemovedFromClass:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssignmentAddedToClassEvent":
        data = AssignmentRemovedFromClass()
        data.ParseFromString(event)

        if not data.assignment_id or not data.class_id:
            return False

        instance = cls(data.assignment_id, data.class_id)
        if instance.validate():
            return instance

        return False


class StudentAddedToClassEvent(PowerGraderEvent):
    def __init__(self, student_id: str, class_id: str) -> None:
        self.proto = StudentAddedToClass()
        self.proto.student_id = student_id
        self.proto.class_id = class_id

        super().__init__(key=self.proto.student_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_ADDED_TO_CLASS

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_class_id(self) -> str:
        return self.proto.class_id

    def validate(self) -> bool:
        return all([self.get_student_id(), self.get_class_id()])

    def _package_into_proto(self) -> StudentAddedToClass:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentAddedToClassEvent":
        data = StudentAddedToClass()
        data.ParseFromString(event)

        if not data.student_id or not data.class_id:
            return False

        instance = cls(data.student_id, data.class_id)
        if instance.validate():
            return instance

        return False


class StudentRemovedFromClassEvent(PowerGraderEvent):
    def __init__(self, student_id: str, class_id: str) -> None:
        self.proto = StudentRemovedFromClass()
        self.proto.student_id = student_id
        self.proto.class_id = class_id

        super().__init__(key=self.proto.student_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_REMOVED_FROM_CLASS

    def get_student_id(self) -> str:
        return self.proto.student_id

    def get_class_id(self) -> str:
        return self.proto.class_id

    def validate(self) -> bool:
        return all([self.get_student_id(), self.get_class_id()])

    def _package_into_proto(self) -> StudentRemovedFromClass:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentAddedToClassEvent":
        data = StudentRemovedFromClass()
        data.ParseFromString(event)

        if not data.student_id or not data.class_id:
            return False

        instance = cls(data.student_id, data.class_id)
        if instance.validate():
            return instance

        return False
