import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
    MockProducer,
)

valid_relationship_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_TIMESTAMPS
)
invalid_relationship_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_UUIDS, INVALID_TIMESTAMPS],
)

from powergrader_event_utils.events.relationship import (
    AssignmentAddedToCourseEvent,
    AssignmentRemovedFromCourseEvent,
    StudentAddedToSectionEvent,
    StudentRemovedFromSectionEvent,
    InstructorAddedToCourseEvent,
    InstructorRemovedFromCourseEvent,
)
from powergrader_event_utils.events.event import EventType

relationship_types = [
    AssignmentAddedToCourseEvent,
    AssignmentRemovedFromCourseEvent,
    StudentAddedToSectionEvent,
    StudentRemovedFromSectionEvent,
    InstructorAddedToCourseEvent,
    InstructorRemovedFromCourseEvent,
]
relationship_type_parameter_names = [
    ("assignment_public_uuid", "course_public_uuid", "timestamp"),
    ("assignment_public_uuid", "course_public_uuid", "timestamp"),
    ("student_public_uuid", "section_public_uuid", "timestamp"),
    ("student_public_uuid", "section_public_uuid", "timestamp"),
    ("instructor_public_uuid", "course_public_uuid", "timestamp"),
    ("instructor_public_uuid", "course_public_uuid", "timestamp"),
]

event_types = [
    EventType.ASSIGNMENT_ADDED_TO_COURSE,
    EventType.ASSIGNMENT_REMOVED_FROM_COURSE,
    EventType.STUDENT_ADDED_TO_SECTION,
    EventType.STUDENT_REMOVED_FROM_SECTION,
    EventType.INSTRUCTOR_ADDED_TO_COURSE,
    EventType.INSTRUCTOR_REMOVED_FROM_COURSE,
]

new_valid_relationship_parameters = []
valid_relationship_parameters_with_parameter_names = []
new_invalid_relationship_parameters = []
for relationship_type, parameter_names in zip(
    relationship_types, relationship_type_parameter_names
):
    for valid in valid_relationship_parameters:
        valid = tuple(list(valid) + [relationship_type])
        new_valid_relationship_parameters.append(valid)
        valid_with_paramter_names = tuple(list(valid) + [parameter_names])
        valid_relationship_parameters_with_parameter_names.append(
            valid_with_paramter_names
        )
    for invalid in invalid_relationship_parameters:
        invalid = tuple(list(invalid) + [relationship_type])
        new_invalid_relationship_parameters.append(invalid)
valid_relationship_parameters = new_valid_relationship_parameters
invalid_relationship_parameters = new_invalid_relationship_parameters


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type",
    valid_relationship_parameters,
)
def test_valid_relationship_creation(
    uuid1, uuid2, version_timestamp, relationship_event_type
):
    relationship_event_type(
        uuid1,
        uuid2,
        version_timestamp,
    )
    relationship_event_type(
        uuid1,
        uuid2,
    )


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type",
    invalid_relationship_parameters,
)
def test_invalid_relationship_creation(
    uuid1, uuid2, version_timestamp, relationship_event_type
):
    with pytest.raises((TypeError, ValueError)):
        relationship_event_type(
            uuid1,
            uuid2,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type, parameter_names",
    valid_relationship_parameters_with_parameter_names,
)
def test_getting_relationship_attributes(
    uuid1, uuid2, version_timestamp, relationship_event_type, parameter_names
):
    relationship_event = relationship_event_type(
        uuid1,
        uuid2,
        version_timestamp,
    )
    for parameter_name, parameter_value in zip(
        parameter_names, [uuid1, uuid2, version_timestamp]
    ):
        assert getattr(relationship_event, parameter_name) == parameter_value

    relationship_event = relationship_event_type(uuid1, uuid2)
    assert relationship_event.timestamp is not None


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type, parameter_names",
    valid_relationship_parameters_with_parameter_names,
)
def test_setting_relationship_fields(
    uuid1, uuid2, version_timestamp, relationship_event_type, parameter_names
):
    relationship_event = relationship_event_type(
        uuid1,
        uuid2,
        version_timestamp,
    )
    for parameter_name, parameter_value in zip(
        parameter_names, [uuid1, uuid2, version_timestamp]
    ):
        with pytest.raises(AttributeError):
            setattr(relationship_event, parameter_name, parameter_value)


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type",
    valid_relationship_parameters,
)
def test_serialize_relationship(
    uuid1, uuid2, version_timestamp, relationship_event_type
):
    relationship_event = relationship_event_type(
        uuid1,
        uuid2,
        version_timestamp,
    )
    serialized = relationship_event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type, parameter_names",
    valid_relationship_parameters_with_parameter_names,
)
def test_deserialize_relationship(
    uuid1, uuid2, version_timestamp, relationship_event_type, parameter_names
):
    relationship_event = relationship_event_type(
        uuid1,
        uuid2,
        version_timestamp,
    )
    serialized = relationship_event.serialize()
    deserialized = relationship_event_type.deserialize(serialized)
    for parameter_name, parameter_value in zip(
        parameter_names, [uuid1, uuid2, version_timestamp]
    ):
        assert getattr(deserialized, parameter_name) == parameter_value


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type",
    valid_relationship_parameters,
)
def test_str_relationship(uuid1, uuid2, version_timestamp, relationship_event_type):
    relationship_event = relationship_event_type(
        uuid1,
        uuid2,
        version_timestamp,
    )
    assert isinstance(str(relationship_event), str)


@pytest.mark.parametrize(
    "uuid1, uuid2, version_timestamp, relationship_event_type",
    valid_relationship_parameters,
)
def test_publish_relationship(uuid1, uuid2, version_timestamp, relationship_event_type):
    event = relationship_event_type(
        uuid1,
        uuid2,
        version_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


@pytest.mark.parametrize(
    "relationship_event_type, event_type",
    zip(relationship_types, event_types),
)
def test_relationship_event_type(relationship_event_type, event_type):
    event = relationship_event_type(
        "uuid1",
        "uuid2",
        123,
    )
    assert event.event_type == event_type
    deserialized = relationship_event_type.deserialize(event.serialize())
    assert deserialized.event_type == event_type
