import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
)


valid_grading_method_parameters = generate_all_permutations(
    VALID_STRS, VALID_STRS, VALID_STRS
)
invalid_grading_method_parameters = generate_singularly_invalid_permutations(
    [VALID_STRS, VALID_STRS, VALID_STRS],
    [INVALID_STRS, INVALID_STRS, INVALID_STRS],
)


@pytest.mark.parametrize(
    "model_name, method_name, git_hash",
    valid_grading_method_parameters,
)
def test_valid_grading_method_creation(model_name, method_name, git_hash):
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )

    GradingMethodEvent(
        model_name=model_name,
        method_name=method_name,
        git_hash=git_hash,
    )
    GradingMethodEvent(model_name, method_name, git_hash)


@pytest.mark.parametrize(
    "model_name, method_name, git_hash",
    invalid_grading_method_parameters,
)
def test_invalid_grading_method_creation(model_name, method_name, git_hash):
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )

    with pytest.raises((TypeError, ValueError)):
        GradingMethodEvent(
            model_name=model_name,
            method_name=method_name,
            git_hash=git_hash,
        )
    with pytest.raises((TypeError, ValueError)):
        GradingMethodEvent(model_name, method_name, git_hash)


@pytest.mark.parametrize(
    "model_name, method_name, git_hash",
    valid_grading_method_parameters,
)
def test_getting_grading_method_fields(model_name, method_name, git_hash):
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )

    event = GradingMethodEvent(
        model_name=model_name,
        method_name=method_name,
        git_hash=git_hash,
    )
    assert event.model_name == model_name
    assert event.method_name == method_name
    assert event.git_hash == git_hash


@pytest.mark.parametrize(
    "model_name, method_name, git_hash",
    valid_grading_method_parameters,
)
def test_setting_grading_method_fields(model_name, method_name, git_hash):
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )

    event = GradingMethodEvent(
        model_name=model_name,
        method_name=method_name,
        git_hash=git_hash,
    )
    with pytest.raises(AttributeError):
        event.model_name = model_name
    with pytest.raises(AttributeError):
        event.method_name = method_name
    with pytest.raises(AttributeError):
        event.git_hash = git_hash
    with pytest.raises(AttributeError):
        event.uuid = "123"


@pytest.mark.parametrize(
    "model_name, method_name, git_hash",
    valid_grading_method_parameters,
)
def test_serializing_grading_method(model_name, method_name, git_hash):
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )

    event = GradingMethodEvent(
        model_name=model_name,
        method_name=method_name,
        git_hash=git_hash,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "model_name, method_name, git_hash",
    valid_grading_method_parameters,
)
def test_deserializing_grading_method(model_name, method_name, git_hash):
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )

    event = GradingMethodEvent(
        model_name=model_name,
        method_name=method_name,
        git_hash=git_hash,
    )
    serialized = event.serialize()
    deserialized = GradingMethodEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, GradingMethodEvent)
    assert deserialized.model_name == model_name
    assert deserialized.method_name == method_name
    assert deserialized.git_hash == git_hash
    assert deserialized.uuid == event.uuid


@pytest.mark.parametrize(
    "model_name, method_name, git_hash",
    valid_grading_method_parameters,
)
def test_str_grading_method(model_name, method_name, git_hash):
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )

    event = GradingMethodEvent(
        model_name=model_name,
        method_name=method_name,
        git_hash=git_hash,
    )
    assert isinstance(str(event), str)


def test_grading_method_event_type():
    from powergrader_event_utils.events.grade import (
        GradingMethodEvent,
    )
    from powergrader_event_utils.events.event import EventType

    event = GradingMethodEvent(
        model_name="model_name",
        method_name="method_name",
        git_hash="git_hash",
    )
    assert event.event_type == EventType.GRADING_METHOD
    deserialized = GradingMethodEvent.deserialize(event.serialize())
    assert deserialized.event_type == EventType.GRADING_METHOD
