import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_STRS,
    VALID_INTS,
    MockProducer,
)

from powergrader_event_utils.events.grade import Grade

valid_grade_parameters = generate_all_permutations(VALID_INTS, VALID_STRS)
VALID_GRADES = [Grade(*params) for params in valid_grade_parameters][:4]
INVALID_GRADES = [10, "10", [], {"a": "b"}]

valid_instructor_criterion_grade_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_GRADES
)
invalid_instructor_criterion_grade_parameters = (
    generate_singularly_invalid_permutations(
        [VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_GRADES],
        [INVALID_UUIDS, INVALID_UUIDS, INVALID_UUIDS, INVALID_GRADES],
    )
)


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    valid_instructor_criterion_grade_parameters,
)
def test_valid_instructor_criterion_grade_creation(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    InstructorCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    InstructorCriterionGradeEvent(
        criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
    )


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    invalid_instructor_criterion_grade_parameters,
)
def test_invalid_instructor_criterion_grade_creation(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    with pytest.raises((TypeError, ValueError)):
        InstructorCriterionGradeEvent(
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            grade=grade,
        )
    with pytest.raises((TypeError, ValueError)):
        InstructorCriterionGradeEvent(
            criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
        )


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    valid_instructor_criterion_grade_parameters,
)
def test_getting_instructor_criterion_grade_fields(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    event = InstructorCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )

    assert event.criterion_uuid == criterion_uuid
    assert event.submission_version_uuid == submission_version_uuid
    assert event.instructor_public_uuid == instructor_public_uuid
    assert event.grade == grade
    assert event.version_uuid is not None


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    valid_instructor_criterion_grade_parameters,
)
def test_setting_instructor_criterion_grade_fields(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    event = InstructorCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )

    with pytest.raises(AttributeError):
        event.criterion_uuid = criterion_uuid
    with pytest.raises(AttributeError):
        event.submission_version_uuid = submission_version_uuid
    with pytest.raises(AttributeError):
        event.instructor_public_uuid = instructor_public_uuid
    with pytest.raises(AttributeError):
        event.grade = grade
    with pytest.raises(AttributeError):
        event.version_uuid = "123"


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    valid_instructor_criterion_grade_parameters,
)
def test_serializing_instructor_criterion_grade(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    event = InstructorCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    valid_instructor_criterion_grade_parameters,
)
def test_deserializing_instructor_criterion_grade(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    event = InstructorCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    serialized = event.serialize()
    deserialized = InstructorCriterionGradeEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, InstructorCriterionGradeEvent)
    assert deserialized.criterion_uuid == criterion_uuid
    assert deserialized.submission_version_uuid == submission_version_uuid
    assert deserialized.instructor_public_uuid == instructor_public_uuid
    assert deserialized.grade == grade
    assert deserialized.version_uuid == event.version_uuid
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    valid_instructor_criterion_grade_parameters,
)
def test_str_instructor_criterion_grade(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    event = InstructorCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "criterion_uuid, submission_version_uuid, instructor_public_uuid, grade",
    valid_instructor_criterion_grade_parameters,
)
def test_publish_instructor_criterion_grade(
    criterion_uuid, submission_version_uuid, instructor_public_uuid, grade
):
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )

    event = InstructorCriterionGradeEvent(
        criterion_uuid=criterion_uuid,
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        grade=grade,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_instructor_criterion_grade_event_type():
    from powergrader_event_utils.events.grade import (
        InstructorCriterionGradeEvent,
    )
    from powergrader_event_utils.events.event import EventType

    event = InstructorCriterionGradeEvent(
        criterion_uuid="123",
        submission_version_uuid="123",
        instructor_public_uuid="123",
        grade=Grade(10, "10"),
    )
    assert event.event_type == EventType.INSTRUCTOR_CRITERION_GRADE
