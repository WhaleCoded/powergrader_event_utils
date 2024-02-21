import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_STRS,
    INVALID_STRS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
    MockProducer,
)

valid_assignment_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_STRS, VALID_STRS, VALID_TIMESTAMPS
)
invalid_assignment_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_STRS, VALID_STRS, VALID_TIMESTAMPS],
    [
        INVALID_UUIDS,
        INVALID_UUIDS,
        INVALID_UUIDS,
        INVALID_STRS,
        INVALID_STRS,
        INVALID_TIMESTAMPS,
    ],
)


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    valid_assignment_parameters,
)
def test_valid_assignment_creation(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
    )
    AssignmentEvent(
        public_uuid,
        instructor_public_uuid,
        rubric_version_uuid,
        name,
        description,
        version_timestamp,
    )
    AssignmentEvent(
        public_uuid,
        instructor_public_uuid,
        rubric_version_uuid,
        name,
        description,
    )


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    invalid_assignment_parameters,
)
def test_invalid_assignment_creation(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    with pytest.raises((TypeError, ValueError)):
        AssignmentEvent(
            public_uuid=public_uuid,
            instructor_public_uuid=instructor_public_uuid,
            rubric_version_uuid=rubric_version_uuid,
            name=name,
            description=description,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        AssignmentEvent(
            public_uuid,
            instructor_public_uuid,
            rubric_version_uuid,
            name,
            description,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    valid_assignment_parameters,
)
def test_getting_assignment_fields(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    event = AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    assert event.public_uuid == public_uuid
    assert event.instructor_public_uuid == instructor_public_uuid
    assert event.rubric_version_uuid == rubric_version_uuid
    assert event.name == name
    assert event.description == description
    assert event.version_timestamp == version_timestamp
    assert event.version_uuid is not None

    event = AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
    )
    assert event.public_uuid == public_uuid
    assert event.instructor_public_uuid == instructor_public_uuid
    assert event.rubric_version_uuid == rubric_version_uuid
    assert event.name == name
    assert event.description == description
    assert event.version_timestamp is not None
    assert event.version_uuid is not None


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    valid_assignment_parameters,
)
def test_setting_assignment_fields(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    event = AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        event.public_uuid = public_uuid
    with pytest.raises(AttributeError):
        event.instructor_public_uuid = instructor_public_uuid
    with pytest.raises(AttributeError):
        event.rubric_version_uuid = rubric_version_uuid
    with pytest.raises(AttributeError):
        event.name = name
    with pytest.raises(AttributeError):
        event.description = description
    with pytest.raises(AttributeError):
        event.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        event.version_uuid = "123"


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    valid_assignment_parameters,
)
def test_serializing_assignment(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    event = AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    valid_assignment_parameters,
)
def test_deserializing_assignment(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    event = AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    serialized = event.serialize()
    deserialized = AssignmentEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, AssignmentEvent)
    assert deserialized.public_uuid == public_uuid
    assert deserialized.instructor_public_uuid == instructor_public_uuid
    assert deserialized.rubric_version_uuid == rubric_version_uuid
    assert deserialized.name == name
    assert deserialized.description == description
    assert deserialized.version_timestamp == version_timestamp
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    valid_assignment_parameters,
)
def test_str_assignment(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    event = AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, rubric_version_uuid, name, description, version_timestamp",
    valid_assignment_parameters,
)
def test_publish_assignment(
    public_uuid,
    instructor_public_uuid,
    rubric_version_uuid,
    name,
    description,
    version_timestamp,
):
    from powergrader_event_utils.events.assignment import AssignmentEvent

    event = AssignmentEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        rubric_version_uuid=rubric_version_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_assignment_event_type():
    from powergrader_event_utils.events.assignment import AssignmentEvent
    from powergrader_event_utils.events.event import EventType

    event = AssignmentEvent(
        public_uuid="123",
        instructor_public_uuid="123",
        rubric_version_uuid="123",
        name="123",
        description="123",
        version_timestamp=123,
    )
    assert event.event_type == EventType.ASSIGNMENT
