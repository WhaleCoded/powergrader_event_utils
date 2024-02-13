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
)


from powergrader_event_utils.events.grade import Grade

valid_grade_parameters = generate_all_permutations(VALID_INTS, VALID_STRS)
VALID_GRADES = [Grade(*params) for params in valid_grade_parameters][:4]
INVALID_GRADES = [10, "10", [], {"a": "b"}]

valid_ai_inferred_criterion_grade_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_GRADES, VALID_TIMESTAMPS
)
invalid_ai_inferred_criterion_grade_parameters = (
    generate_singularly_invalid_permutations(
        [
            VALID_UUIDS,
            VALID_UUIDS,
            VALID_UUIDS,
            VALID_UUIDS,
            VALID_GRADES,
            VALID_TIMESTAMPS,
        ],
        [
            INVALID_UUIDS,
            INVALID_UUIDS,
            INVALID_UUIDS,
            INVALID_UUIDS,
            INVALID_GRADES,
            INVALID_TIMESTAMPS,
        ],
    )
)


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, previous_criterion_grade_version_uuid, faculty_override_criterion_grade_version_uuid, grade, time_finished",
    valid_ai_inferred_criterion_grade_parameters,
)
def test_valid_ai_inferred_criterion_grade_creation(
    grading_started_version_uuid,
    grading_method_uuid,
    previous_criterion_grade_version_uuid,
    faculty_override_criterion_grade_version_uuid,
    grade,
    time_finished,
):
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent

    AIInferredCriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    AIInferredCriterionGradeEvent(
        grading_started_version_uuid,
        grading_method_uuid,
        previous_criterion_grade_version_uuid,
        faculty_override_criterion_grade_version_uuid,
        grade,
        time_finished,
    )


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, previous_criterion_grade_version_uuid, faculty_override_criterion_grade_version_uuid, grade, time_finished",
    invalid_ai_inferred_criterion_grade_parameters,
)
def test_invalid_ai_inferred_criterion_grade_creation(
    grading_started_version_uuid,
    grading_method_uuid,
    previous_criterion_grade_version_uuid,
    faculty_override_criterion_grade_version_uuid,
    grade,
    time_finished,
):
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent

    with pytest.raises((TypeError, ValueError)):
        AIInferredCriterionGradeEvent(
            grading_started_version_uuid=grading_started_version_uuid,
            grading_method_uuid=grading_method_uuid,
            previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
            faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
            grade=grade,
            time_finished=time_finished,
        )
    with pytest.raises((TypeError, ValueError)):
        AIInferredCriterionGradeEvent(
            grading_started_version_uuid,
            grading_method_uuid,
            previous_criterion_grade_version_uuid,
            faculty_override_criterion_grade_version_uuid,
            grade,
            time_finished,
        )


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, previous_criterion_grade_version_uuid, faculty_override_criterion_grade_version_uuid, grade, time_finished",
    valid_ai_inferred_criterion_grade_parameters,
)
def test_getting_ai_inferred_criterion_grade_fields(
    grading_started_version_uuid,
    grading_method_uuid,
    previous_criterion_grade_version_uuid,
    faculty_override_criterion_grade_version_uuid,
    grade,
    time_finished,
):
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent

    event = AIInferredCriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    assert event.grading_started_version_uuid == grading_started_version_uuid
    assert event.grading_method_uuid == grading_method_uuid
    assert (
        event.previous_criterion_grade_version_uuid
        == previous_criterion_grade_version_uuid
    )
    assert (
        event.faculty_override_criterion_grade_version_uuid
        == faculty_override_criterion_grade_version_uuid
    )
    assert event.grade == grade
    assert event.time_finished == time_finished


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, previous_criterion_grade_version_uuid, faculty_override_criterion_grade_version_uuid, grade, time_finished",
    valid_ai_inferred_criterion_grade_parameters,
)
def test_setting_ai_inferred_criterion_grade_fields(
    grading_started_version_uuid,
    grading_method_uuid,
    previous_criterion_grade_version_uuid,
    faculty_override_criterion_grade_version_uuid,
    grade,
    time_finished,
):
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent

    event = AIInferredCriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    with pytest.raises(AttributeError):
        event.grading_started_version_uuid = grading_started_version_uuid
    with pytest.raises(AttributeError):
        event.grading_method_uuid = grading_method_uuid
    with pytest.raises(AttributeError):
        event.previous_criterion_grade_version_uuid = (
            previous_criterion_grade_version_uuid
        )
    with pytest.raises(AttributeError):
        event.faculty_override_criterion_grade_version_uuid = (
            faculty_override_criterion_grade_version_uuid
        )
    with pytest.raises(AttributeError):
        event.grade = grade
    with pytest.raises(AttributeError):
        event.time_finished = time_finished


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, previous_criterion_grade_version_uuid, faculty_override_criterion_grade_version_uuid, grade, time_finished",
    valid_ai_inferred_criterion_grade_parameters,
)
def test_serializing_ai_inferred_criterion_grade(
    grading_started_version_uuid,
    grading_method_uuid,
    previous_criterion_grade_version_uuid,
    faculty_override_criterion_grade_version_uuid,
    grade,
    time_finished,
):
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent

    event = AIInferredCriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, previous_criterion_grade_version_uuid, faculty_override_criterion_grade_version_uuid, grade, time_finished",
    valid_ai_inferred_criterion_grade_parameters,
)
def test_deserializing_ai_inferred_criterion_grade(
    grading_started_version_uuid,
    grading_method_uuid,
    previous_criterion_grade_version_uuid,
    faculty_override_criterion_grade_version_uuid,
    grade,
    time_finished,
):
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent

    event = AIInferredCriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    serialized = event.serialize()
    deserialized = AIInferredCriterionGradeEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, AIInferredCriterionGradeEvent)
    assert deserialized.grading_started_version_uuid == grading_started_version_uuid
    assert deserialized.grading_method_uuid == grading_method_uuid
    assert (
        deserialized.previous_criterion_grade_version_uuid
        == previous_criterion_grade_version_uuid
    )
    assert (
        deserialized.faculty_override_criterion_grade_version_uuid
        == faculty_override_criterion_grade_version_uuid
    )
    assert deserialized.grade == grade
    assert deserialized.time_finished == time_finished


@pytest.mark.parametrize(
    "grading_started_version_uuid, grading_method_uuid, previous_criterion_grade_version_uuid, faculty_override_criterion_grade_version_uuid, grade, time_finished",
    valid_ai_inferred_criterion_grade_parameters,
)
def test_str_ai_inferred_criterion_grade(
    grading_started_version_uuid,
    grading_method_uuid,
    previous_criterion_grade_version_uuid,
    faculty_override_criterion_grade_version_uuid,
    grade,
    time_finished,
):
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent

    event = AIInferredCriterionGradeEvent(
        grading_started_version_uuid=grading_started_version_uuid,
        grading_method_uuid=grading_method_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
        grade=grade,
        time_finished=time_finished,
    )
    assert isinstance(str(event), str)


def test_ai_inferred_criterion_grade_event_type():
    from powergrader_event_utils.events.grade import AIInferredCriterionGradeEvent
    from powergrader_event_utils.events.event import EventType

    event = AIInferredCriterionGradeEvent(
        grading_started_version_uuid="uuid",
        grading_method_uuid="uuid",
        previous_criterion_grade_version_uuid="uuid",
        faculty_override_criterion_grade_version_uuid="uuid",
        grade=Grade(10, "10"),
        time_finished=10,
    )
    assert event.event_type == EventType.AI_INFERRED_CRITERION_GRADE
