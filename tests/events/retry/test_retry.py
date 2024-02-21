import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
    VALID_INTS,
    INVALID_INTS,
    MockProducer,
)

from powergrader_event_utils.events import (
    AssignmentEvent,
    SectionEvent,
    RegisterAssignmentPublicUUIDEvent,
)

valid_events = [
    AssignmentEvent(
        public_uuid="public_uuid",
        instructor_public_uuid="instructor_public_uuid",
        rubric_version_uuid="rubric_version_uuid",
        name="name",
        description="description",
        version_timestamp=1234567890,
    ),
    SectionEvent(
        public_uuid="public_uuid",
        course_public_uuid="course_public_uuid",
        name="name",
        closed=True,
        version_timestamp=1234567890,
    ),
    RegisterAssignmentPublicUUIDEvent(
        lms_id="lms_id",
        organization_public_uuid="organization_public_uuid",
    ),
]
valid_retry_parameters = generate_all_permutations(
    VALID_INTS, VALID_STRS, VALID_STRS, valid_events
)

invalid_events = [
    1,
    None,
    [],
    {"public_uuid": "public_uuid"},
]
invalid_retry_parameters = generate_singularly_invalid_permutations(
    [VALID_INTS, VALID_STRS, VALID_STRS, valid_events],
    [INVALID_INTS, INVALID_STRS, INVALID_STRS, invalid_events],
)


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    valid_retry_parameters,
)
def test_valid_retry_creation(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    RetryEvent(
        retry_number=retry_number,
        retry_reason=retry_reason,
        instance_name=instance_name,
        event=event,
    )
    RetryEvent(
        retry_number,
        retry_reason,
        instance_name,
        event,
    )


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    invalid_retry_parameters,
)
def test_invalid_retry_creation(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    with pytest.raises((TypeError, ValueError)):
        RetryEvent(
            retry_number=retry_number,
            retry_reason=retry_reason,
            instance_name=instance_name,
            event=event,
        )
    with pytest.raises((TypeError, ValueError)):
        RetryEvent(
            retry_number,
            retry_reason,
            instance_name,
            event,
        )


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    valid_retry_parameters,
)
def test_getting_retry_attributes(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    retry = RetryEvent(
        retry_number=retry_number,
        retry_reason=retry_reason,
        instance_name=instance_name,
        event=event,
    )
    assert retry.retry_number == retry_number
    assert retry.retry_reason == retry_reason
    assert retry.instance_name == instance_name
    assert retry.event == event


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    valid_retry_parameters,
)
def test_setting_retry_attributes(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    retry = RetryEvent(
        retry_number=retry_number,
        retry_reason=retry_reason,
        instance_name=instance_name,
        event=event,
    )
    with pytest.raises(AttributeError):
        retry.retry_number = retry_number
    with pytest.raises(AttributeError):
        retry.retry_reason = retry_reason
    with pytest.raises(AttributeError):
        retry.instance_name = instance_name
    with pytest.raises(AttributeError):
        retry.event = event


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    valid_retry_parameters,
)
def test_serialize_retry(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    event = RetryEvent(
        retry_number=retry_number,
        retry_reason=retry_reason,
        instance_name=instance_name,
        event=event,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    valid_retry_parameters,
)
def test_deserialize_retry(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    retry = RetryEvent(
        retry_number=retry_number,
        retry_reason=retry_reason,
        instance_name=instance_name,
        event=event,
    )
    serialized = retry.serialize()
    deserialized = RetryEvent.deserialize(serialized)
    assert deserialized.retry_number == retry_number
    assert deserialized.retry_reason == retry_reason
    assert deserialized.instance_name == instance_name
    assert deserialized.event == event


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    valid_retry_parameters,
)
def test_str_retry(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    event = RetryEvent(
        retry_number=retry_number,
        retry_reason=retry_reason,
        instance_name=instance_name,
        event=event,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "retry_number, retry_reason, instance_name, event",
    valid_retry_parameters,
)
def test_publish_retry(retry_number, retry_reason, instance_name, event):
    from powergrader_event_utils.events.retry import RetryEvent

    event = RetryEvent(
        retry_number=retry_number,
        retry_reason=retry_reason,
        instance_name=instance_name,
        event=event,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_retry_event_type():
    from powergrader_event_utils.events.retry import RetryEvent
    from powergrader_event_utils.events.event import EventType

    event = RetryEvent(
        retry_number=1,
        retry_reason="some_reason",
        instance_name="some_instance",
        event=valid_events[0],
    )
    assert event.event_type == EventType.RETRY
    deserialized = RetryEvent.deserialize(event.serialize())
    assert deserialized.event_type == EventType.RETRY
