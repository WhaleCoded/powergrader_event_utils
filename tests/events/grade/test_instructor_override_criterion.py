import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_STRS,
    VALID_INTS,
)

from powergrader_event_utils.events.grade import Grade

valid_grade_parameters = generate_all_permutations(VALID_INTS, VALID_STRS)
VALID_GRADES = [Grade(*params) for params in valid_grade_parameters][:4]
INVALID_GRADES = [10, "10", [], {"a": "b"}]

valid_instructor_override_criterion_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_GRADES
)
invalid_instructor_override_criterion_parameters = (
    generate_singularly_invalid_permutations(
        [VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_GRADES],
        [INVALID_UUIDS, INVALID_UUIDS, INVALID_UUIDS, INVALID_UUIDS, INVALID_GRADES],
    )
)


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, previous_criterion_grade_version_uuid, instructor_public_uuid, grade",
    valid_instructor_override_criterion_parameters,
)
def test_valid_instructor_override_criterion_creation(
    criterion_uuid,
    submission_version_uuid,
    previous_criterion_grade_version_uuid,
    instructor_public_uuid,
    grade,
):
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )

    InstructorOverrideCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    InstructorOverrideCriterionGradeEvent(
        criterion_uuid,
        submission_version_uuid,
        previous_criterion_grade_version_uuid,
        instructor_public_uuid,
        grade,
    )


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, previous_criterion_grade_version_uuid, instructor_public_uuid, grade",
    invalid_instructor_override_criterion_parameters,
)
def test_invalid_instructor_override_criterion_creation(
    criterion_uuid,
    submission_version_uuid,
    previous_criterion_grade_version_uuid,
    instructor_public_uuid,
    grade,
):
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )

    with pytest.raises((TypeError, ValueError)):
        InstructorOverrideCriterionGradeEvent(
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            grade=grade,
        )
    with pytest.raises((TypeError, ValueError)):
        InstructorOverrideCriterionGradeEvent(
            criterion_uuid,
            submission_version_uuid,
            previous_criterion_grade_version_uuid,
            instructor_public_uuid,
            grade,
        )


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, previous_criterion_grade_version_uuid, instructor_public_uuid, grade",
    valid_instructor_override_criterion_parameters,
)
def test_getting_instructor_override_criterion_fields(
    criterion_uuid,
    submission_version_uuid,
    previous_criterion_grade_version_uuid,
    instructor_public_uuid,
    grade,
):
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )

    event = InstructorOverrideCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    assert event.criterion_uuid == criterion_uuid
    assert event.submission_version_uuid == submission_version_uuid
    assert (
        event.previous_criterion_grade_version_uuid
        == previous_criterion_grade_version_uuid
    )
    assert event.instructor_public_uuid == instructor_public_uuid
    assert event.grade == grade
    assert event.version_uuid is not None


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, previous_criterion_grade_version_uuid, instructor_public_uuid, grade",
    valid_instructor_override_criterion_parameters,
)
def test_setting_instructor_override_criterion_fields(
    criterion_uuid,
    submission_version_uuid,
    previous_criterion_grade_version_uuid,
    instructor_public_uuid,
    grade,
):
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )

    event = InstructorOverrideCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    with pytest.raises(AttributeError):
        event.criterion_uuid = criterion_uuid
    with pytest.raises(AttributeError):
        event.submission_version_uuid = submission_version_uuid
    with pytest.raises(AttributeError):
        event.previous_criterion_grade_version_uuid = (
            previous_criterion_grade_version_uuid
        )
    with pytest.raises(AttributeError):
        event.instructor_public_uuid = instructor_public_uuid
    with pytest.raises(AttributeError):
        event.grade = grade
    with pytest.raises(AttributeError):
        event.version_uuid = "123"


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, previous_criterion_grade_version_uuid, instructor_public_uuid, grade",
    valid_instructor_override_criterion_parameters,
)
def test_serializing_instructor_override_criterion(
    criterion_uuid,
    submission_version_uuid,
    previous_criterion_grade_version_uuid,
    instructor_public_uuid,
    grade,
):
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )

    event = InstructorOverrideCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, previous_criterion_grade_version_uuid, instructor_public_uuid, grade",
    valid_instructor_override_criterion_parameters,
)
def test_deserializing_instructor_override_criterion(
    criterion_uuid,
    submission_version_uuid,
    previous_criterion_grade_version_uuid,
    instructor_public_uuid,
    grade,
):
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )

    event = InstructorOverrideCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    serialized = event.serialize()
    deserialized = InstructorOverrideCriterionGradeEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, InstructorOverrideCriterionGradeEvent)
    assert deserialized.criterion_uuid == criterion_uuid
    assert deserialized.submission_version_uuid == submission_version_uuid
    assert (
        deserialized.previous_criterion_grade_version_uuid
        == previous_criterion_grade_version_uuid
    )
    assert deserialized.instructor_public_uuid == instructor_public_uuid
    assert deserialized.grade == grade
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, previous_criterion_grade_version_uuid, instructor_public_uuid, grade",
    valid_instructor_override_criterion_parameters,
)
def test_str_instructor_override_criterion(
    criterion_uuid,
    submission_version_uuid,
    previous_criterion_grade_version_uuid,
    instructor_public_uuid,
    grade,
):
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )

    event = InstructorOverrideCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    assert isinstance(str(event), str)


def test_instructor_override_criterion_event_type():
    from powergrader_event_utils.events.grade import (
        InstructorOverrideCriterionGradeEvent,
    )
    from powergrader_event_utils.events.event import EventType

    event = InstructorOverrideCriterionGradeEvent(
        criterion_uuid="123",
        submission_version_uuid="123",
        previous_criterion_grade_version_uuid="123",
        instructor_public_uuid="123",
        grade=Grade(10, "10"),
    )
    assert event.event_type == EventType.INSTRUCTOR_OVERRIDE_CRITERION_GRADE
