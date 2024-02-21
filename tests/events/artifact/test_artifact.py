import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_STRS,
    INVALID_STRS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
    MockProducer,
)

valid_artifact_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_STRS, VALID_TIMESTAMPS
)
invalid_artifact_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_STRS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_STRS, INVALID_TIMESTAMPS],
)

from powergrader_event_utils.events.artifact import (
    AssignmentArtifactEvent,
    SubmissionArtifactEvent,
    CriterionArtifactEvent,
    CriterionGradeArtifactEvent,
)
from powergrader_event_utils.events.event import EventType

artifact_types = [
    AssignmentArtifactEvent,
    SubmissionArtifactEvent,
    CriterionArtifactEvent,
    CriterionGradeArtifactEvent,
]
uuid_parameter_names = [
    "assignment_version_uuid",
    "submission_version_uuid",
    "criterion_version_uuid",
    "ai_grading_started_version_uuid",
]
event_types = [
    EventType.ASSIGNMENT_ARTIFACT,
    EventType.SUBMISSION_ARTIFACT,
    EventType.CRITERION_ARTIFACT,
    EventType.CRITERION_GRADE_ARTIFACT,
]

new_valid_artifact_parameters = []
new_invalid_artifact_parameters = []
for artifact_type, uuid_parameter_name in zip(artifact_types, uuid_parameter_names):
    for valid_artifact_parameter in valid_artifact_parameters:
        new_valid_artifact_parameters.append(
            (*valid_artifact_parameter, artifact_type, uuid_parameter_name)
        )
    for invalid_artifact_parameter in invalid_artifact_parameters:
        new_invalid_artifact_parameters.append(
            (*invalid_artifact_parameter, artifact_type, uuid_parameter_name)
        )
valid_artifact_parameters = new_valid_artifact_parameters
invalid_artifact_parameters = new_invalid_artifact_parameters


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    valid_artifact_parameters,
)
def test_valid_criterion_grade_artifact_creation(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
            "version_timestamp": version_timestamp,
        }
    )
    artifact_type(uuid_parameter, artifact, version_timestamp)
    artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
        }
    )
    artifact_type(uuid_parameter, artifact)


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    invalid_artifact_parameters,
)
def test_invalid_criterion_grade_artifact_creation(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    with pytest.raises((TypeError, ValueError)):
        artifact_type(
            **{
                uuid_parameter_name: uuid_parameter,
                "artifact": artifact,
                "version_timestamp": version_timestamp,
            }
        )
    with pytest.raises((TypeError, ValueError)):
        artifact_type(uuid_parameter, artifact, version_timestamp)


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    valid_artifact_parameters,
)
def test_getting_criterion_grade_artifact_fields(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    event = artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
            "version_timestamp": version_timestamp,
        }
    )
    assert getattr(event, uuid_parameter_name) == uuid_parameter
    assert event.artifact == artifact
    assert event.version_timestamp == version_timestamp
    assert event.version_uuid is not None


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    valid_artifact_parameters,
)
def test_setting_criterion_grade_artifact_fields(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    event = artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
            "version_timestamp": version_timestamp,
        }
    )
    with pytest.raises(AttributeError):
        setattr(event, uuid_parameter_name, uuid_parameter)
    with pytest.raises(AttributeError):
        event.artifact = artifact
    with pytest.raises(AttributeError):
        event.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        event.version_uuid = 1245


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    valid_artifact_parameters,
)
def test_serializing_criterion_grade_artifact(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    event = artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
            "version_timestamp": version_timestamp,
        }
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    valid_artifact_parameters,
)
def test_deserializing_criterion_grade_artifact(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    event = artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
            "version_timestamp": version_timestamp,
        }
    )
    serialized = event.serialize()
    deserialized = artifact_type.deserialize(serialized)
    assert getattr(deserialized, uuid_parameter_name) == uuid_parameter
    assert deserialized.artifact == artifact
    assert deserialized.version_timestamp == version_timestamp
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    valid_artifact_parameters,
)
def test_str_criterion_grade_artifact(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    event = artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
            "version_timestamp": version_timestamp,
        }
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name",
    valid_artifact_parameters,
)
def test_publish_criterion_grade_artifact(
    uuid_parameter, artifact, version_timestamp, artifact_type, uuid_parameter_name
):
    event = artifact_type(
        **{
            uuid_parameter_name: uuid_parameter,
            "artifact": artifact,
            "version_timestamp": version_timestamp,
        }
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


@pytest.mark.parametrize(
    "artifact_type, uuid_parameter_name, event_type",
    zip(artifact_types, uuid_parameter_names, event_types),
)
def test_criterion_grade_artifacts_event_type(
    artifact_type, uuid_parameter_name, event_type
):
    event = artifact_type(
        **{
            uuid_parameter_name: "some_uuid",
            "artifact": "some_artifact",
            "version_timestamp": 1234567890,
        }
    )
    assert event.event_type == event_type
    deserialized = artifact_type.deserialize(event.serialize())
    assert deserialized.event_type == event_type
