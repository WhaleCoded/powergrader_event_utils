import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_STRS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
    VALID_INTS,
    MockProducer,
)


from powergrader_event_utils.events.grade import Grade

valid_grade_parameters = generate_all_permutations(VALID_INTS, VALID_STRS)
VALID_GRADES = [Grade(*params) for params in valid_grade_parameters][:4]
INVALID_GRADES = [10, "10", [], {"a": "b"}]

valid_ai_criterion_grade_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_GRADES, VALID_TIMESTAMPS
)
invalid_ai_criterion_grade_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_GRADES, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_UUIDS, INVALID_GRADES, INVALID_TIMESTAMPS],
)


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    valid_ai_criterion_grade_parameters,
)
def test_valid_ai_criterion_grade_creation(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent, Grade

    AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    AICriterionGradeEvent(
        grading_started_version_uuid, grading_method_uuid, grade, time_finished
    )
    AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
    )
    AICriterionGradeEvent(
        grading_started_version_uuid,
        grading_method_uuid,
        grade,
    )


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    invalid_ai_criterion_grade_parameters,
)
def test_invalid_ai_criterion_grade_creation(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent

    with pytest.raises((TypeError, ValueError)):
        AICriterionGradeEvent(
            grading_started_version_uuid=grading_started_version_uuid,
            grading_method_uuid=grading_method_uuid,
            grade=grade,
            time_finished=time_finished,
        )
    with pytest.raises((TypeError, ValueError)):
        AICriterionGradeEvent(
            grading_started_version_uuid, grading_method_uuid, grade, time_finished
        )


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    valid_ai_criterion_grade_parameters,
)
def test_getting_ai_criterion_grade_fields(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent, Grade

    event = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    assert event.grading_started_version_uuid == grading_started_version_uuid
    assert event.grading_method_uuid == grading_method_uuid
    assert event.grade == grade
    assert event.time_finished == time_finished

    event = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
    )
    assert event.grading_started_version_uuid == grading_started_version_uuid
    assert event.grading_method_uuid == grading_method_uuid
    assert event.grade == grade
    assert event.time_finished is not None


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    valid_ai_criterion_grade_parameters,
)
def test_setting_ai_criterion_grade_fields(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent, Grade

    event = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    with pytest.raises(AttributeError):
        event.grading_started_version_uuid = grading_started_version_uuid
    with pytest.raises(AttributeError):
        event.grading_method_uuid = grading_method_uuid
    with pytest.raises(AttributeError):
        event.grade = grade
    with pytest.raises(AttributeError):
        event.time_finished = time_finished


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    valid_ai_criterion_grade_parameters,
)
def test_serializing_ai_criterion_grade(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent, Grade

    event = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    valid_ai_criterion_grade_parameters,
)
def test_deserializing_ai_criterion_grade(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent

    event = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    serialized = event.serialize()
    deserialized = AICriterionGradeEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, AICriterionGradeEvent)
    assert deserialized.grading_started_version_uuid == grading_started_version_uuid
    assert deserialized.grading_method_uuid == grading_method_uuid
    assert deserialized.grade == grade
    assert deserialized.time_finished == time_finished


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    valid_ai_criterion_grade_parameters,
)
def test_str_ai_criterion_grade(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent

    event = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, grade, time_finished",
    valid_ai_criterion_grade_parameters,
)
def test_publish_ai_criterion_grade(
    grading_started_version_uuid, grading_method_uuid, grade, time_finished
):
    from powergrader_event_utils.events.grade import AICriterionGradeEvent

    event = AICriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_criterion_grade_event_type():
    from powergrader_event_utils.events.grade import AICriterionGradeEvent
    from powergrader_event_utils.events.event import EventType

    event = AICriterionGradeEvent(
        grading_started_version_uuid="uuid",
        grading_method_uuid="uuid",
        grade=Grade(10, "10"),
        time_finished=10,
    )
    assert event.event_type == EventType.AI_CRITERION_GRADE
    deserialized = AICriterionGradeEvent.deserialize(event.serialize())
    assert deserialized.event_type == EventType.AI_CRITERION_GRADE
