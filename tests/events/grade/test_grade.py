import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
    VALID_INTS,
    INVALID_INTS,
)


valid_grade_parameters = generate_all_permutations(VALID_INTS, VALID_STRS)
invalid_grade_parameters = generate_singularly_invalid_permutations(
    [VALID_INTS, VALID_STRS],
    [INVALID_INTS, INVALID_STRS],
)


@pytest.mark.parametrize(
    "score, assessment",
    valid_grade_parameters,
)
def test_valid_grade_creation(score, assessment):
    from powergrader_event_utils.events.grade import Grade

    Grade(
        score=score,
        assessment=assessment,
    )
    Grade(score, assessment)


@pytest.mark.parametrize(
    "score, assessment",
    invalid_grade_parameters,
)
def test_invalid_grade_creation(score, assessment):
    from powergrader_event_utils.events.grade import Grade

    with pytest.raises((TypeError, ValueError)):
        Grade(
            score=score,
            assessment=assessment,
        )
    with pytest.raises((TypeError, ValueError)):
        Grade(score, assessment)


@pytest.mark.parametrize(
    "score, assessment",
    valid_grade_parameters,
)
def test_getting_grade_fields(score, assessment):
    from powergrader_event_utils.events.grade import Grade

    event = Grade(
        score=score,
        assessment=assessment,
    )
    assert event.score == score
    assert event.assessment == assessment


@pytest.mark.parametrize(
    "score, assessment",
    valid_grade_parameters,
)
def test_setting_grade_fields(score, assessment):
    from powergrader_event_utils.events.grade import Grade

    event = Grade(
        score=score,
        assessment=assessment,
    )
    with pytest.raises(AttributeError):
        event.score = score
    with pytest.raises(AttributeError):
        event.assessment = assessment


@pytest.mark.parametrize(
    "score, assessment",
    valid_grade_parameters,
)
def test_str_grade(score, assessment):
    from powergrader_event_utils.events.grade import Grade

    event = Grade(
        score=score,
        assessment=assessment,
    )
    assert isinstance(str(event), str)
