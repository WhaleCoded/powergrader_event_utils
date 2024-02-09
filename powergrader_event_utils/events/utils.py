from typing import Any, Mapping, Sequence, Dict, TypeVar, Generic, Type
from enum import Enum
import sys

from powergrader_event_utils.events import PowerGraderEvent
from powergrader_event_utils.events.proto_events.assignment_pb2 import *
from powergrader_event_utils.events.proto_events.course_pb2 import *
from powergrader_event_utils.events.proto_events.grade_pb2 import *
from powergrader_event_utils.events.proto_events.publish_pb2 import *
from powergrader_event_utils.events.proto_events.relationship_pb2 import *
from powergrader_event_utils.events.proto_events.submission_pb2 import *
from powergrader_event_utils.events.proto_events.user_pb2 import *

from powergrader_event_utils.events.base import generate_event_uuid


T = TypeVar("T")


class ProtoLabelType(Enum):
    LABEL_OPTIONAL = 1
    LABEL_REQUIRED = 2
    LABEL_REPEATED = 3


def _is_proto_map(proto_field_descriptor) -> bool:
    if proto_field_descriptor.message_type:
        if "Entry" in proto_field_descriptor.message_type.name:
            if proto_field_descriptor.label == ProtoLabelType.LABEL_REPEATED.value:
                sub_fields = proto_field_descriptor.message_type.fields_by_name
                if "key" in sub_fields and "value" in sub_fields:
                    return True

    return False


def _is_proto_list(proto_field_descriptor) -> bool:
    if not _is_proto_map(proto_field_descriptor):
        if proto_field_descriptor.label == ProtoLabelType.LABEL_REPEATED.value:
            return True

    return False


def _is_proto_sub_message(proto_field_descriptor) -> bool:
    if proto_field_descriptor.message_type:
        return True

    return False


def _convert_proto_type_string_to_actual_type(proto_type_string: str) -> Any:
    proto_type = getattr(sys.modules[__name__], proto_type_string)

    return proto_type


def _handle_proto_scalar_type(proto_field_descriptor, proto_field_value):
    if _is_proto_list(proto_field_descriptor):
        if len(proto_field_value) == 0:
            return None

        return [value for value in proto_field_value]

    default_value = proto_field_descriptor.default_value
    return proto_field_value if proto_field_value != default_value else None


def _handle_message_type(wrapper_type, proto_field_descriptor, proto_field_value):
    if proto_field_descriptor.message_type:
        if _is_proto_map(proto_field_descriptor):
            # We want to return a dict of ProtoWrapper objects
            return_obj = {}
            map_fields = proto_field_descriptor.message_type.fields_by_name

            if _is_proto_sub_message(map_fields["value"]):
                value_proto_type = _convert_proto_type_string_to_actual_type(
                    map_fields["value"].message_type.name
                )
                for key, value in proto_field_value.items():
                    key_value = _handle_proto_scalar_type(map_fields["value"], key)
                    print(wrapper_type)
                    print(proto_field_value)
                    return_obj[key_value] = ProtoWrapper(value_proto_type, value)
            else:
                for key, value in proto_field_value.items():
                    key_value = _handle_proto_scalar_type(map_fields["value"], key)
                    value_value = _handle_proto_scalar_type(map_fields["value"], value)
                    return_obj[key_value] = value_value

        elif _is_proto_list(proto_field_descriptor):
            # We want to return a list of ProtoWrapper objects
            proto_type = _convert_proto_type_string_to_actual_type(
                proto_field_descriptor.message_type.name
            )
            return_obj = [
                ProtoWrapper(proto_type, value) for value in proto_field_value
            ]
        else:
            proto_type = _convert_proto_type_string_to_actual_type(
                proto_field_descriptor.message_type.name
            )
            return_obj = ProtoWrapper(proto_type, proto_field_value)

        return return_obj


class ProtoWrapper(Generic[T]):
    _RESERVED_FIELD_NAMES = ["proto", "proto_type", "_submessage_types"]
    _submessage_types: Dict[str, Any]
    proto_type: Type[T]
    proto: T

    """
    This class is used to dynamically write the logic for getting and setting proto message members.
    Additionally, this class will provide a deserialize method for converting a serialized proto message.
    """

    def __init__(self, proto_type) -> None:
        oneof_group_name = set()
        oneof_field_names = set()
        oneof_field_to_group_name = {}
        oneof_descriptors = proto_type.DESCRIPTOR.oneofs_by_name
        for oneof_name, oneof_descriptor in oneof_descriptors.items():
            oneof_group_name.add(oneof_name)
            for oneof_field_descriptor in oneof_descriptor.fields:
                oneof_field_names.add(oneof_field_descriptor.name)
                oneof_field_to_group_name[oneof_field_descriptor.name] = oneof_name

        self.oneof_group_name = oneof_group_name
        self.oneof_field_names = oneof_field_names
        self.oneof_field_to_group_name = oneof_field_to_group_name

        self.proto_type = proto_type
        self.proto = proto_type()

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self._RESERVED_FIELD_NAMES:
            super().__setattr__(__name, __value)
            return

        if isinstance(__value, Mapping):
            for sub_key, sub_value in __value.items():
                if hasattr(sub_value, "proto"):
                    sub_value = sub_value.proto
                getattr(
                    self.proto,
                    __name,
                )[
                    sub_key
                ].CopyFrom(sub_value)
            self._submessage_types[__name] = {
                "key": type(sub_key),
                "value": type(sub_value),
            }
        elif (
            isinstance(__value, Sequence)
            and not isinstance(__value, str)
            and not isinstance(__value, bytes)
        ):
            for sub_value in __value:
                if hasattr(sub_value, "proto"):
                    sub_value = sub_value.proto
                getattr(
                    self.proto,
                    __name,
                ).append(sub_value)
            self._submessage_types[__name] = [type(sub_value)]
        elif isinstance(__value, Enum):
            setattr(self.proto, __name, __value.value)
        else:
            if hasattr(__value, "proto"):
                getattr(self.proto, __name).CopyFrom(__value.proto)
                self._submessage_types[__name] = type(__value)
            else:
                setattr(self.proto, __name, __value)

    def __getattr__(self, __name: str) -> Any:
        if __name in self._RESERVED_FIELD_NAMES:
            raise AttributeError(f"ProtoWrapper is not yet initialized!")

        return self._unpack_proto_field(__name)

    def _unpack_proto_field(self, __name: str) -> Any:
        if __name in self._submessage_types:
            submessage_type = self._submessage_types[__name]
            if isinstance(submessage_type, dict):
                key_type = submessage_type["key"]
                value_type = submessage_type["value"]
                if isinstance(value_type, ProtoWrapper):
                    value_type = value_type.from_proto
                return {
                    key: value_type(value)
                    for key, value in getattr(self.proto, __name).items()
                }
            elif isinstance(submessage_type, list):
                item_type = submessage_type[0]
                if isinstance(item_type, ProtoWrapper):
                    item_type = item_type.from_proto
                return [item_type(item) for item in getattr(self.proto, __name)]
            else:
                if isinstance(submessage_type, ProtoWrapper):
                    submessage_type = submessage_type.from_proto
                return submessage_type(getattr(self.proto, __name))
        else:
            return getattr(self.proto, __name)

    @classmethod
    def from_proto(cls, proto: T) -> "ProtoWrapper[T]":
        new_instance = cls.__new__(cls)
        new_instance.proto = proto
        return new_instance


def _convert_proto_type_string_to_actual_type(proto_type_string: str) -> Any:
    proto_type = getattr(sys.modules[__name__], proto_type_string)
    return proto_type


# def general_proto_type_init(
#     object_to_initialize,
#     proto_type,
#     key_field_name: str,
#     is_powergrader_event: bool = True,
#     **kwargs: Dict[str, Any],
# ):
#     proto = general_proto_type_packing(object_to_initialize, proto_type, **kwargs)

#     if not key_field_name in kwargs and key_field_name is not None:
#         setattr(
#             proto,
#             key_field_name,
#             generate_event_uuid(object_to_initialize.__class__.__name__),
#         )

#     ProtoWrapper.__init__(object_to_initialize, proto_type, proto)
#     if is_powergrader_event:
#         PowerGraderEvent.__init__(
#             object_to_initialize,
#             key=getattr(proto, key_field_name),
#             event_type=object_to_initialize.__class__.__name__,
#         )


def general_deserialization(proto_type, cls, event_bytes, key_field_name) -> T:
    proto_message = proto_type()
    proto_message.ParseFromString(event_bytes)

    new_event_instance = cls.__new__(cls)
    ProtoWrapper.__init__(new_event_instance, proto_type, proto_message)
    PowerGraderEvent.__init__(
        new_event_instance,
        key=getattr(proto_message, key_field_name),
        event_type=new_event_instance.__class__.__name__,
    )

    return new_event_instance
