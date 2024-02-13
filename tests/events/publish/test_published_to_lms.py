import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
)

valid_published_to_lms_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_TIMESTAMPS
)
invalid_published_to_lms_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_TIMESTAMPS],
)


@pytest.mark.parametrize(
    "published_entity_version_uuid, publish_timestamp",
    valid_published_to_lms_parameters,
)
def test_valid_published_to_lms_creation(
    published_entity_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedToLMSEvent

    PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    PublishedToLMSEvent(
        published_entity_version_uuid,
        publish_timestamp,
    )
    PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
    )
    PublishedToLMSEvent(
        published_entity_version_uuid,
    )


@pytest.mark.parametrize(
    "published_entity_version_uuid, publish_timestamp",
    invalid_published_to_lms_parameters,
)
def test_invalid_published_to_lms_creation(
    published_entity_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedToLMSEvent

    with pytest.raises((TypeError, ValueError)):
        PublishedToLMSEvent(
            published_entity_version_uuid=published_entity_version_uuid,
            publish_timestamp=publish_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        PublishedToLMSEvent(
            published_entity_version_uuid,
            publish_timestamp,
        )


@pytest.mark.parametrize(
    "published_entity_version_uuid, publish_timestamp",
    valid_published_to_lms_parameters,
)
def test_getting_published_to_lms_fields(
    published_entity_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedToLMSEvent

    event = PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    assert event.published_entity_version_uuid == published_entity_version_uuid
    assert event.publish_timestamp == publish_timestamp

    event = PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
    )
    assert event.published_entity_version_uuid == published_entity_version_uuid
    assert event.publish_timestamp is not None


@pytest.mark.parametrize(
    "published_entity_version_uuid, publish_timestamp",
    valid_published_to_lms_parameters,
)
def test_setting_published_to_lms_fields(
    published_entity_version_uuid, publish_timestamp
):
    from powergrader_event_utils.events.publish import PublishedToLMSEvent

    event = PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    with pytest.raises(AttributeError):
        event.published_entity_version_uuid = published_entity_version_uuid
    with pytest.raises(AttributeError):
        event.publish_timestamp = publish_timestamp


@pytest.mark.parametrize(
    "published_entity_version_uuid, publish_timestamp",
    valid_published_to_lms_parameters,
)
def test_serialize_published_to_lms(published_entity_version_uuid, publish_timestamp):
    from powergrader_event_utils.events.publish import PublishedToLMSEvent

    event = PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)


@pytest.mark.parametrize(
    "published_entity_version_uuid, publish_timestamp",
    valid_published_to_lms_parameters,
)
def test_deserialize_published_to_lms(published_entity_version_uuid, publish_timestamp):
    from powergrader_event_utils.events.publish import PublishedToLMSEvent

    event = PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    serialized = event.serialize()
    deserialized = PublishedToLMSEvent.deserialize(serialized)
    assert deserialized.published_entity_version_uuid == published_entity_version_uuid
    assert deserialized.publish_timestamp == publish_timestamp


@pytest.mark.parametrize(
    "published_entity_version_uuid, publish_timestamp",
    valid_published_to_lms_parameters,
)
def test_str_published_to_lms(published_entity_version_uuid, publish_timestamp):
    from powergrader_event_utils.events.publish import PublishedToLMSEvent

    event = PublishedToLMSEvent(
        published_entity_version_uuid=published_entity_version_uuid,
        publish_timestamp=publish_timestamp,
    )
    assert isinstance(str(event), str)


def test_published_to_lms_event_type():
    from powergrader_event_utils.events.publish import PublishedToLMSEvent
    from powergrader_event_utils.events.event import EventType

    event = PublishedToLMSEvent(
        published_entity_version_uuid=VALID_UUIDS[0],
        publish_timestamp=VALID_TIMESTAMPS[0],
    )
    assert event.event_type == EventType.PUBLISHED_TO_LMS
