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

valid_ai_grading_started_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_TIMESTAMPS
)
invalid_ai_grading_started_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_UUIDS, INVALID_TIMESTAMPS],
)


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    valid_ai_grading_started_parameters,
)
def test_valid_ai_grading_started_creation(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        time_started=time_started,
    )
    AICriterionGradingStartedEvent(
        criterion_uuid, submission_version_uuid, time_started
    )
    AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
    )
    AICriterionGradingStartedEvent(criterion_uuid, submission_version_uuid)


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    invalid_ai_grading_started_parameters,
)
def test_invalid_ai_grading_started_creation(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    with pytest.raises((TypeError, ValueError)):
        AICriterionGradingStartedEvent(
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            time_started=time_started,
        )
    with pytest.raises((TypeError, ValueError)):
        AICriterionGradingStartedEvent(
            criterion_uuid, submission_version_uuid, time_started
        )


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    valid_ai_grading_started_parameters,
)
def test_getting_ai_grading_started_fields(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    event = AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        time_started=time_started,
    )
    assert event.criterion_uuid == criterion_uuid
    assert event.submission_version_uuid == submission_version_uuid
    assert event.time_started == time_started

    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    event = AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
    )
    assert event.criterion_uuid == criterion_uuid
    assert event.submission_version_uuid == submission_version_uuid
    assert event.time_started is not None


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    valid_ai_grading_started_parameters,
)
def test_setting_ai_grading_started_fields(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    event = AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        time_started=time_started,
    )
    with pytest.raises(AttributeError):
        event.criterion_uuid = criterion_uuid
    with pytest.raises(AttributeError):
        event.submission_version_uuid = submission_version_uuid
    with pytest.raises(AttributeError):
        event.time_started = time_started
    with pytest.raises(AttributeError):
        event.version_uuid = "123"


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    valid_ai_grading_started_parameters,
)
def test_serializing_ai_grading_started(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    event = AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        time_started=time_started,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    valid_ai_grading_started_parameters,
)
def test_deserializing_ai_grading_started(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    event = AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        time_started=time_started,
    )
    serialized = event.serialize()
    deserialized = AICriterionGradingStartedEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, AICriterionGradingStartedEvent)
    assert deserialized.criterion_uuid == criterion_uuid
    assert deserialized.submission_version_uuid == submission_version_uuid
    assert deserialized.time_started == time_started
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    valid_ai_grading_started_parameters,
)
def test_str_ai_criterion_grading_started(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    event = AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        time_started=time_started,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, time_started",
    valid_ai_grading_started_parameters,
)
def test_publish_ai_criterion_grading_started(
    criterion_uuid, submission_version_uuid, time_started
):
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )

    event = AICriterionGradingStartedEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        time_started=time_started,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_ai_criterion_grading_started_event_type():
    from powergrader_event_utils.events.grade import (
        AICriterionGradingStartedEvent,
    )
    from powergrader_event_utils.events.event import EventType

    event = AICriterionGradingStartedEvent(
        criterion_uuid="123",
        submission_version_uuid="123",
        time_started=123,
    )
    assert event.event_type == EventType.AI_CRITERION_GRADING_STARTED
