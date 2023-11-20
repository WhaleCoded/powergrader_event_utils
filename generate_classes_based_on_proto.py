import os
import subprocess
from typing import List, Dict, Tuple, Self
from dataclasses import dataclass

# Generate Proto Python Classes
subprocess.run("./generate_proto.sh", shell=True)

# Generate Python Structs for all the proto messages
PROTO_SCHEMA_PATH = os.path.join("powergrader_event_utils", "events", "schema")
STRUCT_DESTINATION_PATH = os.path.join(
    "powergrader_event_utils", "events", "event_types"
)


def parse_and_clean_proto_object(curr_index: int, lines: List[str]) -> Tuple[int, str]:
    finished_parsing = False
    parsing_started = False
    num_braces = 0
    cleaned_object = ""
    line = lines[curr_index]
    while not finished_parsing:
        for char in line:
            if char == "\n":
                # Skip white space
                continue
            elif char == "\t":
                char = " "
            elif char == "{":
                if parsing_started == False:
                    parsing_started = True

                num_braces += 1
            elif char == "}":
                num_braces -= 1
                if num_braces == 0:
                    finished_parsing = True

            cleaned_object += char

        if not finished_parsing:
            curr_index += 1
            line = lines[curr_index]

    return curr_index, cleaned_object


def split_proto_file_into_messages(
    proto_file_path: os.PathLike,
) -> Dict[str, List[str]]:
    with open(proto_file_path, "r") as f:
        lines = f.readlines()

    messages = []
    enums = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("enum"):
            # This is the start of an enum
            i, cleaned_enum = parse_and_clean_proto_object(i, lines)
            enums.append(cleaned_enum)

        elif line.startswith("message"):
            # This is the start of a message

            i, cleaned_message = parse_and_clean_proto_object(i, lines)
            messages.append(cleaned_message)

        i += 1
    return {"messages": messages, "enums": enums}


@dataclass
class ProtoEnumField:
    name: str
    value: int


@dataclass
class ProtoEnum:
    name: str
    values: List[ProtoEnumField]


@dataclass
class ProtoMessageField:
    field_type: type
    name: str
    is_oneof: bool = False
    oneof_field_options: List[Self] = None
    is_repeated: bool = False
    is_map: bool = False
    map_value_type: type = None


@dataclass
class ProtoMessage:
    name: str
    fields: List[ProtoMessageField]


def convert_enum_string_to_enum_object(enum_string: str) -> ProtoEnum:
    # Replcae multiple spaces with single space
    enum_string = enum_string.replace("  ", " ").replace("enum ", "")
    print(f"ENUM STRING: {enum_string}")

    # Get enum name
    enum_name = enum_string.split(" ")[0]
    print(f"ENUM NAME: {enum_name}")

    enum_string = enum_string[enum_string.find("{") + 1 :]

    def fill_enum_field(enum_string) -> Tuple[str, ProtoEnumField]:
        field_name = ""
        field_value = ""

        if ";" not in enum_string:
            return "", None

        next_field_string = enum_string[: enum_string.find(";") - 1]
        field_tokens = next_field_string.split(" ")

        field_name = field_tokens[0]
        if field_tokens[1] != "=":
            print("ERROR: Invalid enum field")
        field_value = field_tokens[2]

        new_enum_field = ProtoEnumField(field_name, int(field_value))
        new_enum_string = enum_string[enum_string.find(";") + 1 :]

        return new_enum_string, new_enum_field

    enum_fields = []
    while enum_string != "":
        enum_string, new_enum_field = fill_enum_field(enum_string)
        if new_enum_field != None:
            print(f"ENUM FIELD: {new_enum_field}")
            enum_fields.append(new_enum_field)

    return ProtoEnum(enum_name, enum_fields)


if __name__ == "__main__":
    proto_file_paths_and_names = [
        (name, os.path.join(PROTO_SCHEMA_PATH, name))
        for name in os.listdir(PROTO_SCHEMA_PATH)
        if name.endswith(".proto")
    ]
    for proto_file_name, proto_file_path in proto_file_paths_and_names:
        parsed_proto_objects = split_proto_file_into_messages(proto_file_path)

        print(f"ENUMS: {parsed_proto_objects['enums']}")

        print(f"MESSAGES: {parsed_proto_objects['messages'][0]}")

        break
