import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    VALID_INTS,
)

valid_criterion_level_parameters = generate_all_permutations(VALID_INTS, VALID_STRS)
invalid_criterion_level_parameters = generate_singularly_invalid_permutations(
    [VALID_INTS, VALID_STRS],
    [VALID_STRS, VALID_INTS],
)


@pytest.mark.parametrize(
    "score, description",
    valid_criterion_level_parameters,
)
def test_valid_criterion_level_creation(score, description):
    from powergrader_event_utils.events.assignment import CriterionLevel

    CriterionLevel(
        score=score,
        description=description,
    )
    CriterionLevel(score, description)


@pytest.mark.parametrize(
    "score, description",
    invalid_criterion_level_parameters,
)
def test_invalid_criterion_level_creation(score, description):
    from powergrader_event_utils.events.assignment import CriterionLevel

    with pytest.raises((TypeError, ValueError)):
        CriterionLevel(
            score=score,
            description=description,
        )
    with pytest.raises((TypeError, ValueError)):
        CriterionLevel(score, description)


@pytest.mark.parametrize(
    "score, description",
    valid_criterion_level_parameters,
)
def test_getting_criterion_level_fields(score, description):
    from powergrader_event_utils.events.assignment import CriterionLevel

    event = CriterionLevel(
        score=score,
        description=description,
    )
    assert event.score == score
    assert event.description == description


@pytest.mark.parametrize(
    "score, description",
    valid_criterion_level_parameters,
)
def test_setting_criterion_level_fields(score, description):
    from powergrader_event_utils.events.assignment import CriterionLevel

    event = CriterionLevel(
        score=score,
        description=description,
    )
    with pytest.raises(AttributeError):
        event.score = score
    with pytest.raises(AttributeError):
        event.description = description


@pytest.mark.parametrize(
    "score, description",
    valid_criterion_level_parameters,
)
def test_criterion_level_str(score, description):
    from powergrader_event_utils.events.assignment import CriterionLevel

    event = CriterionLevel(
        score=score,
        description=description,
    )
    assert isinstance(str(event), str)
