import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    MockProducer,
)

VALID_EMBEDDINGS = [[0, 0, 0], [0.4], [1203, -1.240, 1024, 0.0, 0.0, 0.0, 1.30]]
INVALID_EMBEDDINGS = [
    10,
    "10",
    [],
    {"a": "b"},
]
valid_embedding_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_EMBEDDINGS
)
invalid_embedding_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_EMBEDDINGS],
    [INVALID_UUIDS, INVALID_UUIDS, INVALID_EMBEDDINGS],
)

from powergrader_event_utils.events.embedding import (
    AssignmentEmbeddingEvent,
    CriterionEmbeddingEvent,
    CriterionGradeEmbeddingEvent,
    SubmissionEmbeddingEvent,
    ArtifactEmbeddingEvent,
)
from powergrader_event_utils.events.event import EventType

embedding_types = [
    AssignmentEmbeddingEvent,
    CriterionEmbeddingEvent,
    CriterionGradeEmbeddingEvent,
    SubmissionEmbeddingEvent,
    ArtifactEmbeddingEvent,
]
uuid_parameter_names = [
    "assignment_version_uuid",
    "criterion_version_uuid",
    "criterion_grade_version_uuid",
    "submission_version_uuid",
    "artifact_version_uuid",
]
event_types = [
    EventType.ASSIGNMENT_EMBEDDING,
    EventType.CRITERION_EMBEDDING,
    EventType.CRITERION_GRADE_EMBEDDING,
    EventType.SUBMISSION_EMBEDDING,
    EventType.ARTIFACT_EMBEDDING,
]

new_valid_embedding_parameters = []
new_invalid_embedding_parameters = []
for embedding_type, uuid_paramter_name in zip(embedding_types, uuid_parameter_names):
    for valid_embedding_parameter in valid_embedding_parameters:
        new_valid_embedding_parameters.append(
            (*valid_embedding_parameter, embedding_type, uuid_paramter_name)
        )
    for invalid_embedding_parameter in invalid_embedding_parameters:
        new_invalid_embedding_parameters.append(
            (*invalid_embedding_parameter, embedding_type, uuid_paramter_name)
        )
valid_embedding_parameters = new_valid_embedding_parameters
invalid_embedding_parameters = new_invalid_embedding_parameters


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    valid_embedding_parameters,
)
def test_valid_criterion_grade_embedding_creation(
    uuid_parameter,
    embedder_uuid,
    embedding,
    embedding_type,
    uuid_parameter_name,
):
    embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        **{uuid_parameter_name: uuid_parameter}
    )
    embedding_type(uuid_parameter, embedder_uuid, embedding)
    embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        version_timestamp=1234,
        **{uuid_parameter_name: uuid_parameter}
    )
    embedding_type(uuid_parameter, embedder_uuid, embedding, 1234)


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    invalid_embedding_parameters,
)
def test_invalid_criterion_grade_embedding_creation(
    uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name
):
    with pytest.raises((TypeError, ValueError)):
        embedding_type(
            embedder_uuid=embedder_uuid,
            embedding=embedding,
            **{uuid_parameter_name: uuid_parameter}
        )
    with pytest.raises((TypeError, ValueError)):
        embedding_type(uuid_parameter, embedder_uuid, embedding)


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    valid_embedding_parameters,
)
def test_getting_criterion_grade_embedding_fields(
    uuid_parameter,
    embedder_uuid,
    embedding,
    embedding_type,
    uuid_parameter_name,
):
    event = embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        **{uuid_parameter_name: uuid_parameter}
    )
    assert getattr(event, uuid_parameter_name) == uuid_parameter
    assert event.embedder_uuid == embedder_uuid
    # Error of floating point precision
    epsilon = 1e-6
    assert [abs(a - b) < epsilon for a, b in zip(event.embedding, embedding)]
    assert event.version_uuid is not None
    assert event.version_timestamp is not None


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    valid_embedding_parameters,
)
def test_setting_criterion_grade_embedding_fields(
    uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name
):
    event = embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        **{uuid_parameter_name: uuid_parameter}
    )
    with pytest.raises(AttributeError):
        setattr(event, uuid_parameter_name, uuid_parameter)
    with pytest.raises(AttributeError):
        event.embedder_uuid = embedder_uuid
    with pytest.raises(AttributeError):
        event.embedding = embedding
    with pytest.raises(AttributeError):
        event.version_uuid = "123"
    with pytest.raises(AttributeError):
        event.version_timestamp = 1234


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    valid_embedding_parameters,
)
def test_serializing_criterion_grade_embedding(
    uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name
):
    event = embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        **{uuid_parameter_name: uuid_parameter}
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    valid_embedding_parameters,
)
def test_deserializing_criterion_grade_embedding(
    uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name
):
    event = embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        **{uuid_parameter_name: uuid_parameter}
    )
    serialized = event.serialize()
    deserialized = embedding_type.deserialize(serialized)
    assert getattr(deserialized, uuid_parameter_name) == uuid_parameter
    assert deserialized.embedder_uuid == embedder_uuid
    # Error of floating point precision
    epsilon = 1e-6
    assert [abs(a - b) < epsilon for a, b in zip(deserialized.embedding, embedding)]
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    valid_embedding_parameters,
)
def test_str_criterion_grade_embedding(
    uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name
):
    event = embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        **{uuid_parameter_name: uuid_parameter}
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name",
    valid_embedding_parameters,
)
def test_publish_criterion_grade_embedding(
    uuid_parameter, embedder_uuid, embedding, embedding_type, uuid_parameter_name
):
    event = embedding_type(
        embedder_uuid=embedder_uuid,
        embedding=embedding,
        **{uuid_parameter_name: uuid_parameter}
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


@pytest.mark.parametrize(
    "embedding_type, uuid_parameter_name, event_type",
    zip(embedding_types, uuid_parameter_names, event_types),
)
def test_criterion_grade_embeddings_event_type(
    embedding_type, uuid_parameter_name, event_type
):
    event = embedding_type(
        embedder_uuid="uuid", embedding=[0, 0, 0], **{uuid_parameter_name: "uuid"}
    )
    assert event.event_type == event_type
    deserialized = embedding_type.deserialize(event.serialize())
    assert deserialized.event_type == event_type
