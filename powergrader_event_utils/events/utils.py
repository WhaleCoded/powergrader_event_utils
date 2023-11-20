from typing import Any, List, Dict, TypeVar, Generic, Type
from enum import Enum
import sys

from powergrader_event_utils.events import PowerGraderEvent

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


def _convert_proto_type_string_to_acutal_type(proto_type_string: str) -> Any:
    proto_type = getattr(sys.modules[__name__], proto_type_string)

    return proto_type


def _handle_proto_scalar_type(proto_field_descriptor, proto_field_value):
    if _is_proto_list(proto_field_descriptor):
        if len(proto_field_value) == 0:
            return None

        return [value for value in proto_field_value]

    default_value = proto_field_descriptor.default_value
    return proto_field_value if proto_field_value != default_value else None


def _handle_message_type(proto_field_descriptor, proto_field_value):
    if proto_field_descriptor.message_type:
        if _is_proto_map(proto_field_descriptor):
            # We want to return a dict of ProtoWrapper objects
            return_obj = {}
            map_fields = proto_field_descriptor.message_type.fields_by_name

            if _is_proto_sub_message(map_fields["value"]):
                value_proto_type = _convert_proto_type_string_to_acutal_type(
                    map_fields["value"].message_type.name
                )
                for key, value in proto_field_value.items():
                    key_value = _handle_proto_scalar_type(map_fields["value"], key)
                    return_obj[key_value] = ProtoWrapper(value_proto_type, value)
            else:
                for key, value in proto_field_value.items():
                    key_value = _handle_proto_scalar_type(map_fields["value"], key)
                    value_value = _handle_proto_scalar_type(map_fields["value"], value)
                    return_obj[key_value] = value_value

        elif _is_proto_list(proto_field_descriptor):
            # We want to return a list of ProtoWrapper objects
            proto_type = _convert_proto_type_string_to_acutal_type(
                proto_field_descriptor.message_type.name
            )
            return_obj = [
                ProtoWrapper(proto_type, value) for value in proto_field_value
            ]
        else:
            proto_type = _convert_proto_type_string_to_acutal_type(
                proto_field_descriptor.message_type.name
            )
            return_obj = ProtoWrapper(proto_type, proto_field_value)

        return return_obj


class ProtoWrapper(Generic[T]):
    """
    This class is used to dynamically write the logic for getting and setting proto message members.
    Additionally, this class will provide a deserialize method for converting a serialized proto message.
    """

    def __init__(self, proto_type: Type[T], proto_message) -> None:
        if not isinstance(proto_message, proto_type):
            raise ValueError(
                f"proto_message must be of type {T.__name__}, not {type(proto_message).__name__}."
            )

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

        self.proto = proto_message
        self.proto_type = proto_type

    def __getattribute__(self, __name: str) -> Any:
        try:
            proto_object = object.__getattribute__(self, "proto")
        except AttributeError:
            # Prevent infinite recursion if the proto object has not been initialized yet.
            return object.__getattribute__(self, __name)

        # Figure out if we are trying to access a oneof or optional field
        one_of_group_name = None
        if __name in object.__getattribute__(self, "oneof_group_name"):
            one_of_group_name = __name
        elif __name in object.__getattribute__(self, "oneof_field_names"):
            # This means that we are trying to access an optional field
            # If the field is not set, return None.
            # In this case, the default value is valid and should not be returned as none
            oneof_group_name = object.__getattribute__(
                self, "oneof_field_to_group_name"
            )[__name]

        if one_of_group_name is not None:
            oneof_field_name = proto_object.WhichOneof(oneof_group_name)

            if oneof_field_name is None:
                return None

            # Check if the oneof field is a sub message
            oneof_field_descriptor = (
                object.__getattribute__(self, "proto_type")
                .DESCRIPTOR.oneofs_by_name[one_of_group_name]
                .fields_by_name[oneof_field_name]
            )
            proto_field_value = getattr(proto_object, oneof_field_name)
            if oneof_field_descriptor.message_type:
                # Return a ProtoWrapper object
                return _handle_message_type(oneof_field_descriptor, proto_field_value)

            return proto_field_value

        # Check the attribute is a member of the proto message.
        proto_fields = object.__getattribute__(
            self, "proto_type"
        ).DESCRIPTOR.fields_by_name

        if not __name in proto_fields:
            # If the attribute is not a member of the proto message, follow normal functionality.
            return object.__getattribute__(self, __name)

        # The attribute is a member of the proto message, so handle it according to its type.
        proto_field_descriptor = proto_fields[__name]
        proto_field_value = getattr(object.__getattribute__(self, "proto"), __name)

        if proto_field_descriptor.message_type:
            return _handle_message_type(proto_field_descriptor, proto_field_value)
        else:
            return _handle_proto_scalar_type(proto_field_descriptor, proto_field_value)


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
