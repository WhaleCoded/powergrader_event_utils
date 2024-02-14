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

valid_course_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_STRS, VALID_STRS, VALID_TIMESTAMPS
)
invalid_course_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_STRS, VALID_STRS, VALID_TIMESTAMPS],
    [
        INVALID_UUIDS,
        INVALID_UUIDS,
        INVALID_STRS,
        INVALID_STRS,
        INVALID_TIMESTAMPS,
    ],
)


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    valid_course_parameters,
)
def test_valid_course_creation(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
    )
    CourseEvent(
        public_uuid,
        instructor_public_uuid,
        name,
        description,
        version_timestamp,
    )
    CourseEvent(
        public_uuid,
        instructor_public_uuid,
        name,
        description,
    )


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    invalid_course_parameters,
)
def test_invalid_course_creation(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    with pytest.raises((TypeError, ValueError)):
        CourseEvent(
            public_uuid=public_uuid,
            instructor_public_uuid=instructor_public_uuid,
            name=name,
            description=description,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        CourseEvent(
            public_uuid,
            instructor_public_uuid,
            name,
            description,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    valid_course_parameters,
)
def test_getting_course_fields(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    course = CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    assert course.public_uuid == public_uuid
    assert course.instructor_public_uuid == instructor_public_uuid
    assert course.name == name
    assert course.description == description
    assert course.version_timestamp == version_timestamp
    assert course.version_uuid is not None

    course = CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
    )
    assert course.public_uuid == public_uuid
    assert course.instructor_public_uuid == instructor_public_uuid
    assert course.name == name
    assert course.description == description
    assert course.version_timestamp is not None
    assert course.version_uuid is not None


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    valid_course_parameters,
)
def test_setting_course_fields(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    course = CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        course.public_uuid = public_uuid
    with pytest.raises(AttributeError):
        course.instructor_public_uuid = instructor_public_uuid
    with pytest.raises(AttributeError):
        course.name = name
    with pytest.raises(AttributeError):
        course.description = description
    with pytest.raises(AttributeError):
        course.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        course.version_uuid = course.version_uuid


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    valid_course_parameters,
)
def test_serialize_course(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    course = CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    serialized = course.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    valid_course_parameters,
)
def test_deserialize_course(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    course = CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    serialized = course.serialize()
    deserialized = CourseEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, CourseEvent)
    assert deserialized.public_uuid == public_uuid
    assert deserialized.instructor_public_uuid == instructor_public_uuid
    assert deserialized.name == name
    assert deserialized.description == description
    assert deserialized.version_timestamp == version_timestamp
    assert deserialized.version_uuid == course.version_uuid


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    valid_course_parameters,
)
def test_str_course(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    course = CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(course), str)


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, description, version_timestamp",
    valid_course_parameters,
)
def test_publish_course(
    public_uuid, instructor_public_uuid, name, description, version_timestamp
):
    from powergrader_event_utils.events.course import CourseEvent

    event = CourseEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        description=description,
        version_timestamp=version_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_course_event_type():
    from powergrader_event_utils.events.course import CourseEvent
    from powergrader_event_utils.events.event import EventType

    event = CourseEvent(
        public_uuid="public_uuid",
        instructor_public_uuid="instructor_public_uuid",
        name="name",
        description="description",
        version_timestamp=1234567890,
    )
    assert event.event_type == EventType.COURSE
