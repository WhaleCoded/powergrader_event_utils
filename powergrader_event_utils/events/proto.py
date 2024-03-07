from typing import Any, Mapping, Sequence, Dict, Type, Self, Optional, Tuple
from enum import _EnumDict, Enum, EnumMeta, FlagBoundary

from powergrader_event_utils.events.proto_events.assignment_pb2 import *
from powergrader_event_utils.events.proto_events.course_pb2 import *
from powergrader_event_utils.events.proto_events.grade_pb2 import *
from powergrader_event_utils.events.proto_events.publish_pb2 import *
from powergrader_event_utils.events.proto_events.relationship_pb2 import *
from powergrader_event_utils.events.proto_events.submission_pb2 import *
from powergrader_event_utils.events.proto_events.user_pb2 import *

import google.protobuf.message
import google.protobuf.descriptor

PROTO_TO_PROTO_WRAPPER_MAP: Dict[str, Type["ProtoWrapper"]] = {}


class ProtoWrapperMeta(type):
    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)
        if cls.__name__ in [
            "ProtoWrapper",
            "ProtoPowerGraderEvent",
        ]:
            return

        if not hasattr(cls, "proto_type"):
            raise NotImplementedError(
                "Implementations of the ProtoWrapper class must have a proto_type class attribute set."
            )
        proto_type = cls.proto_type.DESCRIPTOR.full_name
        if (
            proto_type in PROTO_TO_PROTO_WRAPPER_MAP
            and PROTO_TO_PROTO_WRAPPER_MAP[proto_type].__name__ != cls.__name__
        ):
            raise ValueError(
                f"Proto type {proto_type} is already mapped to {PROTO_TO_PROTO_WRAPPER_MAP[proto_type].__name__}."
            )
        PROTO_TO_PROTO_WRAPPER_MAP[proto_type] = cls

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        try:
            new_proto_wrapper_instance = super().__call__(*args, **kwds)
        # Remove some of the unnecessary stack trace by raising a new exception
        except TypeError as e:
            raise TypeError(f"{e}") from None
        except ValueError as e:
            raise ValueError(f"{e}") from None
        except AttributeError as e:
            raise AttributeError(f"{e}") from None

        new_proto_wrapper_instance._ProtoWrapper__frozen = True
        return new_proto_wrapper_instance


class ProtoEnumWrapperMeta(EnumMeta):
    def __new__(
        metacls: type[Self],
        cls: str,
        bases: Tuple[Type],
        classdict: _EnumDict,
        *,
        boundary: FlagBoundary | None = None,
        _simple: bool = False,
        **kwds: Any,
    ) -> Self:
        enum_dict = super().__prepare__(cls, bases, **kwds)
        for k, v in classdict.items():
            if k == "proto_type":
                continue
            enum_dict[k] = v
        return super().__new__(
            metacls,
            cls,
            bases,
            enum_dict,
            boundary=boundary,
            _simple=_simple,
            **kwds,
        )

    def __init__(cls, name, bases, clsdict):
        if cls.__name__ in ["ProtoEnumWrapper"]:
            super().__init__(name, bases, clsdict)
            return

        proto_type = clsdict.get("proto_type")
        if proto_type is None:
            raise NotImplementedError(
                "Implementations of the ProtoEnumWrapper class must have a proto_type class attribute set."
            )
        super().__init__(name, bases, clsdict)
        cls.proto_type = proto_type

        proto_type = cls.proto_type.DESCRIPTOR.full_name
        if (
            proto_type in PROTO_TO_PROTO_WRAPPER_MAP
            and PROTO_TO_PROTO_WRAPPER_MAP[proto_type].__name__ != cls.__name__
        ):
            raise ValueError(
                f"Proto type {proto_type} is already mapped to {PROTO_TO_PROTO_WRAPPER_MAP[proto_type].__name__}."
            )
        PROTO_TO_PROTO_WRAPPER_MAP[proto_type] = cls


class ProtoEnumWrapper(metaclass=ProtoEnumWrapperMeta):
    """
    Wrapper for protobuf enums. This class handles all packing and unpacking for
    protobuf enums, allowing for easy deserialization when used with ProtoWrapper
    subclasses. This class should be subclassed and the proto_type class attribute
    should be set to the protobuf enum type. Only one instance of this class may
    be created for each protobuf enum type.

    For example:
    ```
    class ExampleProtoEnumWrapper(ProtoEnumWrapper):
        proto_type = ExampleProtoEnum

        VALUE1 = 0
        VALUE2 = 1
    ```
    """

    proto_type: Type[google.protobuf.message.Message]

    @classmethod
    def from_proto(cls, proto: google.protobuf.message.Message) -> Self:
        """
        Creates a new instance of the ProtoEnumWrapper subclass from a protobuf enum.

        Args:
            proto (google.protobuf.message.Message): The protobuf enum to convert.

        Returns:
            ProtoEnumWrapper: The new instance of the ProtoEnumWrapper subclass.

        Raises:
            ValueError: If the proto does not match the expected type
        """
        for member in cls:
            if member.value == proto:
                return member
        raise ValueError(
            f"No matching enum value for proto {proto} found in {cls.__name__}."
        )

    @property
    def name(self) -> str:
        return self._name_

    @property
    def value(self) -> Any:
        return self._value_


class ProtoWrapper(metaclass=ProtoWrapperMeta):
    """
    Wrapper for protobuf messages. This class handles all packing and unpacking for
    protobuf messages, allowing for easy manipulation of protobuf messages with intuitive
    python typing. This class should be subclassed and the proto_type class attribute
    should be set to the protobuf message type. Only one instance of this class may be
    created for each protobuf message type.

    This makes the creation of new instances of your messages easy, even if you need
    to implement instantiaion logic.

    For example:
    ```
    class ExampleProtoWrapper(ProtoWrapper):
        proto_type = ExampleProto

        my_str_field: str
        my_int_field: int
        my_hidden_field: str

        def __init__(self, my_str_field: str, my_int_field: int) -> None:
            super().__init__()
            self.my_str_field = my_str_field
            self.my_int_field = my_int_field
            self.my_hidden_field = "hidden"
    ```
    """

    proto_type: Type[google.protobuf.message.Message]
    proto: google.protobuf.message.Message

    def __init__(self) -> None:
        if self.proto_type is None:
            raise NotImplementedError(
                "Implementations of the ProtoWrapper class must have a proto_type class attribute set."
            )
        self.__frozen = False
        field_names, one_of_type_map, one_of_names = (
            self.__class__._get_proto_field_names_and_one_of_map()
        )
        self.__proto_field_names = field_names
        self.__one_of_type_map = one_of_type_map
        self.__one_of_names = one_of_names
        self.proto = self.proto_type()

    def __setattr__(self, __name: str, __value: Any) -> None:
        def _set_proto_field(__name: str, __value: Any) -> None:
            if not __name in self.__proto_field_names:
                raise AttributeError(
                    f"{self.__class__.__name__} proto does not have a field named {__name}."
                )

            if __value is None:
                return

            if __name in self.__one_of_names and hasattr(__value, "proto_type"):
                __name = self.__one_of_type_map[__value.proto_type.DESCRIPTOR.full_name]

            if isinstance(__value, Mapping):
                for sub_key, sub_value in __value.items():
                    if hasattr(sub_value, "proto"):
                        sub_value = sub_value.proto
                    try:
                        getattr(
                            self.proto,
                            __name,
                        )[
                            sub_key
                        ].CopyFrom(sub_value)
                    except TypeError:
                        raise TypeError(
                            f"{self.__class__.__name__}.{__name} is not a map field. {__name} must be of type {_get_proto_type_for_error_messages(getattr(self.proto, __name))}."
                        )
            elif (
                isinstance(__value, Sequence)
                and not isinstance(__value, str)
                and not isinstance(__value, bytes)
            ):
                for sub_value in __value:
                    if hasattr(sub_value, "proto"):
                        sub_value = sub_value.proto
                    try:
                        getattr(
                            self.proto,
                            __name,
                        ).append(sub_value)
                    except AttributeError:
                        raise TypeError(
                            f"{self.__class__.__name__}.{__name} is not a repeated field. {__name} must be of type {_get_proto_type_for_error_messages(getattr(self.proto, __name))}."
                        )
            elif hasattr(__value, "proto"):
                try:
                    getattr(self.proto, __name).CopyFrom(__value.proto)
                except AttributeError:
                    raise TypeError(
                        f"{self.__class__.__name__}.{__name} cannot be set to type {type(__value)}. {__name} must be of type {_get_proto_type_for_error_messages(getattr(self.proto, __name))}."
                    )
            elif isinstance(__value, (ProtoEnumWrapper, Enum)):
                setattr(self.proto, __name, __value.value)
            else:
                try:
                    setattr(self.proto, __name, __value)
                except TypeError:
                    raise TypeError(
                        f"Cannot set {self.__class__.__name__}.{__name} to {__value}. {__name} must be of type {_get_proto_type_for_error_messages(getattr(self.proto, __name))}."
                    )
                except ValueError:
                    raise ValueError(
                        f"Cannot set {self.__class__.__name__}.{__name} to {__value}. Invalid value for {__name}."
                    )
                except AttributeError:
                    raise TypeError(
                        f"Cannot set type {type(__value)} to {self.__class__.__name__}.{__name}."
                    )

        # __setattr__ should never be used on proto_type
        if __name == "proto_type":
            raise AttributeError(
                "proto_type is a class attribute and should be set accordingly."
            )

        # We check frozen when setting __proto_field_names, so we need to catch it here
        if __name == "_ProtoWrapper__frozen":
            super().__setattr__(__name, __value)
            return

        # We use __proto_field_names to set the proto fields, so we need to catch it here
        if __name == "_ProtoWrapper__proto_field_names":
            if self.__frozen:
                raise AttributeError(
                    "Setting __proto_field_names should only be done internally by the base ProtoWrapper class."
                )
            super().__setattr__(__name, __value)

        # So long as it isnt a proto field, we don't need to do anything special
        if (not hasattr(self, "_ProtoWrapper__proto_field_names")) or (
            __name not in self.__proto_field_names
        ):
            super().__setattr__(__name, __value)
        elif self.__frozen:
            raise AttributeError(
                "proto fields should not be set after the object has been created. ProtoWrapper objects are meant to be immutable."
            )
        else:
            _set_proto_field(__name, __value)

    def __getattr__(self, __name: str) -> Any:
        def _get_submessage_type(
            field_descriptor: google.protobuf.descriptor.FieldDescriptor,
        ) -> Optional[Type["ProtoWrapper"]]:
            proto_type_full_name = None
            if field_descriptor.message_type:
                proto_type_full_name = field_descriptor.message_type.full_name
            elif field_descriptor.enum_type:
                proto_type_full_name = field_descriptor.enum_type.full_name
            else:
                return None

            if proto_type_full_name in PROTO_TO_PROTO_WRAPPER_MAP:
                return PROTO_TO_PROTO_WRAPPER_MAP[proto_type_full_name]
            else:
                raise ValueError(
                    f"Proto type {proto_type_full_name} is not mapped to a ProtoWrapper class."
                )

        def _unpack_proto_field(__name: str) -> Any:
            if __name in self.__one_of_names:
                __name = self.proto.WhichOneof(__name)

            field = getattr(self.proto, __name)

            if field is None:
                return None

            if (
                isinstance(field, Sequence)
                and not isinstance(field, str)
                and not isinstance(field, bytes)
            ):
                proto_field_descriptor = self.proto_type.DESCRIPTOR.fields_by_name[
                    __name
                ]
                proto_wrapper_type = _get_submessage_type(proto_field_descriptor)
                if proto_wrapper_type is not None:
                    field = [proto_wrapper_type.from_proto(x) for x in field]
                else:
                    field = list(field)
            elif isinstance(field, Mapping):
                key_field_descriptor = self.proto_type.DESCRIPTOR.fields_by_name[
                    __name
                ].message_type.fields_by_name["key"]
                value_field_descriptor = self.proto_type.DESCRIPTOR.fields_by_name[
                    __name
                ].message_type.fields_by_name["value"]

                key_proto_type = _get_submessage_type(key_field_descriptor)
                value_proto_type = _get_submessage_type(value_field_descriptor)

                wrapped_map_field = {}
                for k, v in field.items():
                    if key_proto_type is not None:
                        k = key_proto_type.from_proto(k)
                    if value_proto_type is not None:
                        v = value_proto_type.from_proto(v)
                    wrapped_map_field[k] = v

                field = wrapped_map_field
            elif isinstance(field, google.protobuf.message.Message):
                proto_field_descriptor = self.proto_type.DESCRIPTOR.fields_by_name[
                    __name
                ]
                proto_wrapper_type = _get_submessage_type(proto_field_descriptor)
                if proto_wrapper_type is not None:
                    field = proto_wrapper_type.from_proto(field)
            else:
                proto_field_descriptor = self.proto_type.DESCRIPTOR.fields_by_name[
                    __name
                ]
                proto_wrapper_type = _get_submessage_type(proto_field_descriptor)
                if proto_wrapper_type is not None:
                    field = proto_wrapper_type(field)

            # Check to see if the field is optional, if not, return Nones as None
            one_of_descriptor = self.proto_type.DESCRIPTOR.oneofs_by_name.get(
                "_" + __name
            )
            if one_of_descriptor:
                for field_descriptor in one_of_descriptor.fields:
                    if field_descriptor.name == __name:
                        return field

            if (isinstance(field, str) and field == "") or (
                isinstance(field, int) and field == 0
            ):
                return None
            return field

        if __name in [
            "proto",
            "proto_type",
            "_ProtoWrapper__frozen",
            "_ProtoWrapper__proto_field_names",
        ]:
            raise AttributeError(f"{self.__class__.__name__} has not been initialized.")
        if __name in self.__proto_field_names:
            return _unpack_proto_field(__name)
        else:
            raise AttributeError(
                f"{self.__class__.__name__} proto does not have a field named {__name}."
            )

    # TODO: Create a more generalizable from_proto method, so that the __init__ and event deserialization are not copied
    @classmethod
    def from_proto(cls, proto: google.protobuf.message.Message) -> Self:
        """
        Creates a new instance of the ProtoWrapper subclass from a protobuf message.

        Args:
            proto (google.protobuf.message.Message): The protobuf message to convert.

        Returns:
            ProtoWrapper: The new instance of the ProtoWrapper subclass.

        Raises:
            ValueError: If the proto does not match the expected type, or if the subclass
                does not have a proto_type class attribute set.
        """
        new_instance = cls.__new__(cls)
        if new_instance.proto_type is None:
            raise NotImplementedError(
                "Implementations of the ProtoWrapper class must have a proto_type class attribute set."
            )
        new_instance.__frozen = False
        field_names, one_of_type_map, one_of_names = (
            cls._get_proto_field_names_and_one_of_map()
        )
        new_instance.__proto_field_names = field_names
        new_instance.__one_of_type_map = one_of_type_map
        new_instance.__one_of_names = one_of_names
        new_instance.proto = proto
        new_instance.__frozen = True
        return new_instance

    @classmethod
    def _get_proto_field_names_and_one_of_map(
        cls,
    ) -> Tuple[Sequence[str], Dict[str, str]]:
        base_field_names = set(
            [field.name for field in cls.proto_type.DESCRIPTOR.fields]
        )
        proto_type_full_name_to_oneof_field_map = {}
        oneof_names = set()
        oneof_and_optional_names = cls.proto_type.DESCRIPTOR.oneofs_by_name.keys()

        def _update_maps_from_potential_oneof_name(oneof_name: str) -> None:
            for field in cls.proto_type.DESCRIPTOR.oneofs_by_name[oneof_name].fields:
                field_name = field.name
                if field.message_type is None:
                    return
                proto_type_full_name = field.message_type.full_name
                proto_type_full_name_to_oneof_field_map[proto_type_full_name] = (
                    field_name
                )
                base_field_names.remove(field_name)
            base_field_names.add(oneof_name)
            oneof_names.add(oneof_name)

        for oneof_name in oneof_and_optional_names:
            _update_maps_from_potential_oneof_name(oneof_name)
        return (
            list(base_field_names),
            proto_type_full_name_to_oneof_field_map,
            set(oneof_names),
        )

    def __str__(self) -> str:
        def stringify_field(field: Any) -> str:
            if isinstance(field, ProtoWrapper):
                return str(field)
            elif (
                isinstance(field, Sequence)
                and not isinstance(field, str)
                and not isinstance(field, bytes)
            ):
                return f"[{', '.join(str(x) for x in field)}]"
            elif isinstance(field, Mapping):
                return (
                    "{"
                    + f"{', '.join(f'{str(k)}: {str(v)}' for k, v in field.items())}"
                    + "}"
                )
            elif isinstance(field, str):
                return repr(field)
            else:
                return str(field)

        s = ", ".join(
            f"{field_name}={stringify_field(getattr(self, field_name))}"
            for field_name in self.__proto_field_names
        )
        return f"{self.__class__.__name__}({s})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ProtoWrapper):
            return False
        return self.proto == __value.proto

    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)

    def __hash__(self) -> int:
        return hash(self.proto.SerializeToString())


def _get_proto_type_for_error_messages(
    proto_type: Any,
) -> str:
    if (
        isinstance(proto_type, Sequence)
        and not isinstance(proto_type, str)
        and not isinstance(proto_type, bytes)
    ):
        return str(type([]))
    elif isinstance(proto_type, Mapping):
        return str(type({}))
    else:
        return str(type(proto_type))
