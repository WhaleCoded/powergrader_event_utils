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
)


valid_section_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_STRS, [True, False], VALID_TIMESTAMPS
)
invalid_bools = [1, "True", None, [1, 2, 3]]
invalid_section_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_STRS, [True, False], VALID_TIMESTAMPS],
    [
        INVALID_UUIDS,
        INVALID_UUIDS,
        INVALID_STRS,
        invalid_bools,
        INVALID_TIMESTAMPS,
    ],
)


@pytest.mark.parametrize(
    "public_uuid, course_public_uuid, name, closed, version_timestamp",
    valid_section_parameters,
)
def test_valid_section_creation(
    public_uuid, course_public_uuid, name, closed, version_timestamp
):
    from powergrader_event_utils.events.course import SectionEvent

    SectionEvent(
        public_uuid=public_uuid,
        course_public_uuid=course_public_uuid,
        name=name,
        closed=closed,
        version_timestamp=version_timestamp,
    )
    SectionEvent(
        public_uuid,
        course_public_uuid,
        name,
        closed,
        version_timestamp,
    )


@pytest.mark.parametrize(
    "public_uuid, course_public_uuid, name, closed, version_timestamp",
    invalid_section_parameters,
)
def test_invalid_section_creation(
    public_uuid, course_public_uuid, name, closed, version_timestamp
):
    from powergrader_event_utils.events.course import SectionEvent

    with pytest.raises((TypeError, ValueError)):
        SectionEvent(
            public_uuid=public_uuid,
            course_public_uuid=course_public_uuid,
            name=name,
            closed=closed,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        SectionEvent(
            public_uuid,
            course_public_uuid,
            name,
            closed,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "public_uuid, course_public_uuid, name, closed, version_timestamp",
    valid_section_parameters,
)
def test_getting_section_attributes(
    public_uuid, course_public_uuid, name, closed, version_timestamp
):
    from powergrader_event_utils.events.course import SectionEvent

    section = SectionEvent(
        public_uuid=public_uuid,
        course_public_uuid=course_public_uuid,
        name=name,
        closed=closed,
        version_timestamp=version_timestamp,
    )
    assert section.public_uuid == public_uuid
    assert section.course_public_uuid == course_public_uuid
    assert section.name == name
    assert section.closed == closed
    assert section.version_timestamp == version_timestamp
    assert section.version_uuid is not None


@pytest.mark.parametrize(
    "public_uuid, course_public_uuid, name, closed, version_timestamp",
    valid_section_parameters,
)
def test_setting_section_attributes(
    public_uuid, course_public_uuid, name, closed, version_timestamp
):
    from powergrader_event_utils.events.course import SectionEvent

    section = SectionEvent(
        public_uuid=public_uuid,
        course_public_uuid=course_public_uuid,
        name=name,
        closed=closed,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        section.public_uuid = public_uuid
    with pytest.raises(AttributeError):
        section.course_public_uuid = course_public_uuid
    with pytest.raises(AttributeError):
        section.name = name
    with pytest.raises(AttributeError):
        section.closed = closed
    with pytest.raises(AttributeError):
        section.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        section.version_uuid = "123"


@pytest.mark.parametrize(
    "public_uuid, course_public_uuid, name, closed, version_timestamp",
    valid_section_parameters,
)
def test_serialize_section(
    public_uuid, course_public_uuid, name, closed, version_timestamp
):
    from powergrader_event_utils.events.course import SectionEvent

    section = SectionEvent(
        public_uuid=public_uuid,
        course_public_uuid=course_public_uuid,
        name=name,
        closed=closed,
        version_timestamp=version_timestamp,
    )
    serialized = section.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "public_uuid, course_public_uuid, name, closed, version_timestamp",
    valid_section_parameters,
)
def test_deserialize_section(
    public_uuid, course_public_uuid, name, closed, version_timestamp
):
    from powergrader_event_utils.events.course import SectionEvent

    section = SectionEvent(
        public_uuid=public_uuid,
        course_public_uuid=course_public_uuid,
        name=name,
        closed=closed,
        version_timestamp=version_timestamp,
    )
    serialized = section.serialize()
    deserialized = SectionEvent.deserialize(serialized)
    assert deserialized.public_uuid == public_uuid
    assert deserialized.course_public_uuid == course_public_uuid
    assert deserialized.name == name
    assert deserialized.closed == closed
    assert deserialized.version_timestamp == version_timestamp
    assert deserialized.version_uuid == section.version_uuid


@pytest.mark.parametrize(
    "public_uuid, course_public_uuid, name, closed, version_timestamp",
    valid_section_parameters,
)
def test_str_section(public_uuid, course_public_uuid, name, closed, version_timestamp):
    from powergrader_event_utils.events.course import SectionEvent

    section = SectionEvent(
        public_uuid=public_uuid,
        course_public_uuid=course_public_uuid,
        name=name,
        closed=closed,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(section), str)


def test_section_event_type():
    from powergrader_event_utils.events.course import SectionEvent
    from powergrader_event_utils.events.event import EventType

    event = SectionEvent(
        public_uuid="123",
        course_public_uuid="456",
        name="section",
        closed=True,
        version_timestamp=1234567890,
    )
    assert event.event_type == EventType.SECTION
