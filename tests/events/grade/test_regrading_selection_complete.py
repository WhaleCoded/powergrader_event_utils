import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_STRS,
    INVALID_STRS,
    MockProducer,
)

valid_criterion_grade_version_uuids = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_UUIDS
)
new_valid_criterion_grade_version_uuids = []
for a, b, c in valid_criterion_grade_version_uuids:
    new_valid_criterion_grade_version_uuids.extend([a, b, c])
valid_criterion_grade_version_uuids = list(new_valid_criterion_grade_version_uuids)
new_valid_criterion_grade_version_uuids = [
    valid_criterion_grade_version_uuids,
    valid_criterion_grade_version_uuids[:5],
    valid_criterion_grade_version_uuids[5:],
    [valid_criterion_grade_version_uuids[0]],
    [valid_criterion_grade_version_uuids[1]],
    [],
]
valid_criterion_grade_version_uuids = new_valid_criterion_grade_version_uuids

invalid_criterion_grade_version_uuids = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_UUIDS],
    [INVALID_UUIDS, INVALID_UUIDS, INVALID_UUIDS],
)
new_invalid_criterion_grade_version_uuids = [
    list(invalid_criterion_grade_version_uuids[0]),
    list(invalid_criterion_grade_version_uuids[1]),
    "",
    {"a": "b"},
    15,
    15.5,
]

valid_regrading_selection_complete_parameters = generate_all_permutations(
    VALID_UUIDS, valid_criterion_grade_version_uuids
)
invalid_regrading_selection_complete_parameters = (
    generate_singularly_invalid_permutations(
        [VALID_UUIDS, valid_criterion_grade_version_uuids],
        [INVALID_UUIDS, new_invalid_criterion_grade_version_uuids],
    )
)


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    valid_regrading_selection_complete_parameters,
)
def test_valid_regrading_selection_complete_creation(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids,
    )


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    invalid_regrading_selection_complete_parameters,
)
def test_invalid_regrading_selection_complete_creation(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    with pytest.raises((TypeError, ValueError)):
        RegradingSelectionCompleteEvent(
            instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
            criterion_grade_version_uuids=criterion_grade_version_uuids,
        )
    with pytest.raises((TypeError, ValueError)):
        RegradingSelectionCompleteEvent(
            instructor_override_criterion_grade_version_uuid,
            criterion_grade_version_uuids,
        )


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    valid_regrading_selection_complete_parameters,
)
def test_getting_regrading_selection_complete_fields(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    event = RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    assert (
        event.instructor_override_criterion_grade_version_uuid
        == instructor_override_criterion_grade_version_uuid
    )
    assert event.criterion_grade_version_uuids == criterion_grade_version_uuids


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    valid_regrading_selection_complete_parameters,
)
def test_setting_regrading_selection_complete_fields(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    event = RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    with pytest.raises(AttributeError):
        event.instructor_override_criterion_grade_version_uuid = (
            instructor_override_criterion_grade_version_uuid
        )
    with pytest.raises(AttributeError):
        event.criterion_grade_version_uuids = criterion_grade_version_uuids


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    valid_regrading_selection_complete_parameters,
)
def test_serializing_regrading_selection_complete(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    event = RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    valid_regrading_selection_complete_parameters,
)
def test_deserializing_regrading_selection_complete(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    event = RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    serialized = event.serialize()
    deserialized = RegradingSelectionCompleteEvent.deserialize(serialized)
    assert deserialized.instructor_override_criterion_grade_version_uuid == (
        instructor_override_criterion_grade_version_uuid
    )
    assert deserialized.criterion_grade_version_uuids == criterion_grade_version_uuids


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    valid_regrading_selection_complete_parameters,
)
def test_str_regrading_selection_complete(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    event = RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids",
    valid_regrading_selection_complete_parameters,
)
def test_publish_regrading_selection_complete(
    instructor_override_criterion_grade_version_uuid, criterion_grade_version_uuids
):
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent

    event = RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid=instructor_override_criterion_grade_version_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_regrading_selection_complete_event_type():
    from powergrader_event_utils.events.grade import RegradingSelectionCompleteEvent
    from powergrader_event_utils.events.event import EventType

    event = RegradingSelectionCompleteEvent(
        instructor_override_criterion_grade_version_uuid="uuid",
        criterion_grade_version_uuids=["uuid"],
    )
    assert event.event_type == EventType.REGRADING_SELECTION_COMPLETE
    deserialized = RegradingSelectionCompleteEvent.deserialize(event.serialize())
    assert deserialized.event_type == EventType.REGRADING_SELECTION_COMPLETE
