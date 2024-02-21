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

valid_published_grade_to_lms_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_TIMESTAMPS
)
invalid_published_grade_to_lms_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_TIMESTAMPS],
)


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    valid_published_grade_to_lms_parameters,
)
def test_valid_published_grade_to_lms_creation(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid,
        publish_timestamp,
    )
    PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
    )
    PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid,
    )


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    invalid_published_grade_to_lms_parameters,
)
def test_invalid_published_grade_to_lms_creation(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    with pytest.raises((TypeError, ValueError)):
        PublishedGradeToLMSEvent(
            instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
            publish_timestamp=publish_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        PublishedGradeToLMSEvent(
            instructor_grade_approval_version_uuid,
            publish_timestamp,
        )


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    valid_published_grade_to_lms_parameters,
)
def test_gettting_published_grade_to_lms_fields(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    assert (
        event.instructor_grade_approval_version_uuid
        == instructor_grade_approval_version_uuid
    )
    assert event.publish_timestamp == publish_timestamp

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
    )
    assert (
        event.instructor_grade_approval_version_uuid
        == instructor_grade_approval_version_uuid
    )
    assert event.publish_timestamp is not None


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    valid_published_grade_to_lms_parameters,
)
def test_setting_published_grade_to_lms_fields(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    with pytest.raises(AttributeError):
        event.instructor_grade_approval_version_uuid = (
            instructor_grade_approval_version_uuid
        )
    with pytest.raises(AttributeError):
        event.publish_timestamp = publish_timestamp


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    valid_published_grade_to_lms_parameters,
)
def test_serialize_published_grade_to_lms(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    serialized = event.serialize()
    print(serialized)
    assert serialized is not None
    assert isinstance(serialized, bytes)


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    valid_published_grade_to_lms_parameters,
)
def test_deserialize_published_grade_to_lms(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    serialized = event.serialize()
    deserialized = PublishedGradeToLMSEvent.deserialize(serialized)
    assert (
        deserialized.instructor_grade_approval_version_uuid
        == instructor_grade_approval_version_uuid
    )
    assert deserialized.publish_timestamp == publish_timestamp


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    valid_published_grade_to_lms_parameters,
)
def test_str_published_grade_to_lms(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "instructor_grade_approval_version_uuid, publish_timestamp",
    valid_published_grade_to_lms_parameters,
)
def test_publish_published_grade_to_lms(
    instructor_grade_approval_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_publish_grade_to_lms_event_type():
    from powergrader_event_utils.events.publish import PublishedGradeToLMSEvent
    from powergrader_event_utils.events.event import EventType

    event = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid="123e4567-e89b-12d3-a456-426614174000",
        publish_timestamp=1615766400,
    )
    assert event.event_type == EventType.PUBLISHED_GRADE_TO_LMS
