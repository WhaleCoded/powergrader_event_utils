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

valid_assignment_parameters = generate_all_permutations(VALID_UUIDS, VALID_STRS)
invalid_assignment_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_STRS], [INVALID_UUIDS, INVALID_STRS]
)


@pytest.mark.parametrize("artifact_version_uuid, log", valid_assignment_parameters)
def test_valid_artifact_log_creation(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    ArtifactLogEvent(
        artifact_version_uuid=artifact_version_uuid,
        log=log,
    )
    ArtifactLogEvent(
        artifact_version_uuid,
        log,
    )


@pytest.mark.parametrize("artifact_version_uuid, log", invalid_assignment_parameters)
def test_invalid_artifact_log_creation(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    with pytest.raises((TypeError, ValueError)):
        ArtifactLogEvent(
            artifact_version_uuid=artifact_version_uuid,
            log=log,
        )
    with pytest.raises((TypeError, ValueError)):
        ArtifactLogEvent(
            artifact_version_uuid,
            log,
        )


@pytest.mark.parametrize("artifact_version_uuid, log", valid_assignment_parameters)
def test_getting_artifact_log_fields(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    event = ArtifactLogEvent(
        artifact_version_uuid=artifact_version_uuid,
        log=log,
    )
    assert event.artifact_version_uuid == artifact_version_uuid
    assert event.log == log


@pytest.mark.parametrize("artifact_version_uuid, log", valid_assignment_parameters)
def test_setting_artifact_log_fields(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    event = ArtifactLogEvent(
        artifact_version_uuid=artifact_version_uuid,
        log=log,
    )
    with pytest.raises(AttributeError):
        event.artifact_version_uuid = artifact_version_uuid
    with pytest.raises(AttributeError):
        event.log = log


@pytest.mark.parametrize("artifact_version_uuid, log", valid_assignment_parameters)
def test_serializing_artifact_log_event(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    event = ArtifactLogEvent(
        artifact_version_uuid=artifact_version_uuid,
        log=log,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)


@pytest.mark.parametrize("artifact_version_uuid, log", valid_assignment_parameters)
def test_deserializing_artifact_log_event(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    event = ArtifactLogEvent(
        artifact_version_uuid=artifact_version_uuid,
        log=log,
    )
    serialized = event.serialize()
    deserialized = ArtifactLogEvent.deserialize(serialized)
    assert deserialized is not None
    assert isinstance(deserialized, ArtifactLogEvent)
    assert deserialized.artifact_version_uuid == artifact_version_uuid
    assert deserialized.log == log


@pytest.mark.parametrize("artifact_version_uuid, log", valid_assignment_parameters)
def test_str_artifact_log_event(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    event = ArtifactLogEvent(
        artifact_version_uuid=artifact_version_uuid,
        log=log,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize("artifact_version_uuid, log", valid_assignment_parameters)
def test_publish_artifact_log_event(artifact_version_uuid, log):
    from powergrader_event_utils.events.artifact import ArtifactLogEvent

    event = ArtifactLogEvent(
        artifact_version_uuid=artifact_version_uuid,
        log=log,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_artifact_log_event_type():
    from powergrader_event_utils.events.artifact import ArtifactLogEvent
    from powergrader_event_utils.events.event import EventType

    event = ArtifactLogEvent(
        artifact_version_uuid="123",
        log="log",
    )
    assert event.event_type == EventType.ARTIFACT_LOG
    deserialized = ArtifactLogEvent.deserialize(event.serialize())
    assert deserialized.event_type == EventType.ARTIFACT_LOG
