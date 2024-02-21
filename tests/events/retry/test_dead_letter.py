import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
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
valid_dead_letter_parameters = generate_all_permutations(
    VALID_STRS, VALID_STRS, valid_events
)

invalid_events = [
    1,
    None,
    [],
    {"public_uuid": "public_uuid"},
]
invalid_dead_letter_parameters = generate_singularly_invalid_permutations(
    [VALID_STRS, VALID_STRS, valid_events],
    [INVALID_STRS, INVALID_STRS, invalid_events],
)


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    valid_dead_letter_parameters,
)
def test_valid_dead_letter_creation(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    DeadLetterEvent(
        dead_letter_reason=dead_letter_reason,
        instance_name=instance_name,
        event=event,
    )
    DeadLetterEvent(
        dead_letter_reason,
        instance_name,
        event,
    )


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    invalid_dead_letter_parameters,
)
def test_invalid_dead_letter_creation(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    with pytest.raises((TypeError, ValueError)):
        DeadLetterEvent(
            dead_letter_reason=dead_letter_reason,
            instance_name=instance_name,
            event=event,
        )
    with pytest.raises((TypeError, ValueError)):
        DeadLetterEvent(
            dead_letter_reason,
            instance_name,
            event,
        )


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    valid_dead_letter_parameters,
)
def test_getting_dead_letter_attributes(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    dead_letter = DeadLetterEvent(
        dead_letter_reason=dead_letter_reason,
        instance_name=instance_name,
        event=event,
    )
    assert dead_letter.dead_letter_reason == dead_letter_reason
    assert dead_letter.instance_name == instance_name
    assert dead_letter.event == event


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    valid_dead_letter_parameters,
)
def test_setting_dead_letter_attributes(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    dead_letter = DeadLetterEvent(
        dead_letter_reason=dead_letter_reason,
        instance_name=instance_name,
        event=event,
    )
    with pytest.raises(AttributeError):
        dead_letter.dead_letter_reason = "new_dead_letter_reason"
    with pytest.raises(AttributeError):
        dead_letter.instance_name = "new_instance_name"
    with pytest.raises(AttributeError):
        dead_letter.event = valid_events[0]


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    valid_dead_letter_parameters,
)
def test_serialize_dead_letter(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    dead_letter = DeadLetterEvent(
        dead_letter_reason=dead_letter_reason,
        instance_name=instance_name,
        event=event,
    )
    serialized = dead_letter.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    valid_dead_letter_parameters,
)
def test_deserialize_dead_letter(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    dead_letter = DeadLetterEvent(
        dead_letter_reason=dead_letter_reason,
        instance_name=instance_name,
        event=event,
    )
    serialized = dead_letter.serialize()
    deserialized = DeadLetterEvent.deserialize(serialized)
    assert deserialized.dead_letter_reason == dead_letter_reason
    assert deserialized.instance_name == instance_name
    assert deserialized.event == event


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    valid_dead_letter_parameters,
)
def test_str_dead_letter(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    dead_letter = DeadLetterEvent(
        dead_letter_reason=dead_letter_reason,
        instance_name=instance_name,
        event=event,
    )
    assert isinstance(str(dead_letter), str)


@pytest.mark.parametrize(
    "dead_letter_reason, instance_name, event",
    valid_dead_letter_parameters,
)
def test_publish_dead_letter(dead_letter_reason, instance_name, event):
    from powergrader_event_utils.events.retry import DeadLetterEvent

    event = DeadLetterEvent(
        dead_letter_reason=dead_letter_reason,
        instance_name=instance_name,
        event=event,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_dead_letter_event_type():
    from powergrader_event_utils.events.retry import DeadLetterEvent
    from powergrader_event_utils.events.event import EventType

    dead_letter = DeadLetterEvent(
        dead_letter_reason="dead_letter_reason",
        instance_name="instance_name",
        event=valid_events[0],
    )
    assert dead_letter.event_type == EventType.DEAD_LETTER
    deserialized = DeadLetterEvent.deserialize(dead_letter.serialize())
    assert deserialized.event_type == EventType.DEAD_LETTER
