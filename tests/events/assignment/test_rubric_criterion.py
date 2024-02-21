import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
    VALID_INTS,
)

from powergrader_event_utils.events.assignment import CriterionLevel

valid_criterion_levels = [
    CriterionLevel(s, d) for s, d in generate_all_permutations(VALID_INTS, VALID_STRS)
]
invalid_criterion_levels = [
    -1,
    [],
    [1, 2, 3],
    {"a": "b"},
    CriterionLevel(1, "a"),
    [CriterionLevel(1, "a")],
]

valid_rubric_criterion_parameters = generate_all_permutations(
    VALID_STRS,
    [valid_criterion_levels[:2], valid_criterion_levels],
)
invalid_rubric_criterion_parameters = generate_singularly_invalid_permutations(
    [VALID_STRS, [valid_criterion_levels[:2], valid_criterion_levels]],
    [INVALID_STRS, invalid_criterion_levels],
)


@pytest.mark.parametrize(
    "name, levels",
    valid_rubric_criterion_parameters,
)
def test_valid_rubric_criterion_creation(name, levels):
    from powergrader_event_utils.events.assignment import RubricCriterion

    RubricCriterion(
        name=name,
        levels=levels,
    )
    RubricCriterion(name, levels)


@pytest.mark.parametrize(
    "name, levels",
    invalid_rubric_criterion_parameters,
)
def test_invalid_rubric_criterion_creation(name, levels):
    from powergrader_event_utils.events.assignment import RubricCriterion

    with pytest.raises((TypeError, ValueError)):
        RubricCriterion(
            name=name,
            levels=levels,
        )
    with pytest.raises((TypeError, ValueError)):
        RubricCriterion(name, levels)


@pytest.mark.parametrize(
    "name, levels",
    valid_rubric_criterion_parameters,
)
def test_getting_rubric_criterion_fields(name, levels):
    from powergrader_event_utils.events.assignment import RubricCriterion

    event = RubricCriterion(
        name=name,
        levels=levels,
    )
    assert event.name == name
    assert event.levels == levels


@pytest.mark.parametrize(
    "name, levels",
    valid_rubric_criterion_parameters,
)
def test_setting_rubric_criterion_fields(name, levels):
    from powergrader_event_utils.events.assignment import RubricCriterion

    event = RubricCriterion(
        name=name,
        levels=levels,
    )
    with pytest.raises(AttributeError):
        event.name = name
    with pytest.raises(AttributeError):
        event.levels = levels
    with pytest.raises(AttributeError):
        event.uuid = "1234"


@pytest.mark.parametrize(
    "name, levels",
    valid_rubric_criterion_parameters,
)
def test_rubric_criterion_str(name, levels):
    from powergrader_event_utils.events.assignment import RubricCriterion

    event = RubricCriterion(
        name=name,
        levels=levels,
    )
    assert isinstance(str(event), str)
