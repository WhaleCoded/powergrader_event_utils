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
valid_criterion_grade_embedding_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_EMBEDDINGS
)
invalid_criterion_grade_embedding_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_EMBEDDINGS],
    [INVALID_UUIDS, INVALID_UUIDS, INVALID_EMBEDDINGS],
)


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    valid_criterion_grade_embedding_parameters,
)
def test_valid_criterion_grade_embedding_creation(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid=criterion_grade_version_uuid,
        embedder_uuid=embedder_uuid,
        embedding=embedding,
    )
    CriterionGradeEmbeddingEvent(criterion_grade_version_uuid, embedder_uuid, embedding)


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    invalid_criterion_grade_embedding_parameters,
)
def test_invalid_criterion_grade_embedding_creation(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    with pytest.raises((TypeError, ValueError)):
        CriterionGradeEmbeddingEvent(
            criterion_grade_version_uuid=criterion_grade_version_uuid,
            embedder_uuid=embedder_uuid,
            embedding=embedding,
        )
    with pytest.raises((TypeError, ValueError)):
        CriterionGradeEmbeddingEvent(
            criterion_grade_version_uuid, embedder_uuid, embedding
        )


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    valid_criterion_grade_embedding_parameters,
)
def test_getting_criterion_grade_embedding_fields(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    event = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid=criterion_grade_version_uuid,
        embedder_uuid=embedder_uuid,
        embedding=embedding,
    )
    assert event.criterion_grade_version_uuid == criterion_grade_version_uuid
    assert event.embedder_uuid == embedder_uuid
    # Error of floating point precision
    epsilon = 1e-6
    assert [abs(a - b) < epsilon for a, b in zip(event.embedding, embedding)]
    assert event.version_uuid is not None


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    valid_criterion_grade_embedding_parameters,
)
def test_setting_criterion_grade_embedding_fields(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    event = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid=criterion_grade_version_uuid,
        embedder_uuid=embedder_uuid,
        embedding=embedding,
    )
    with pytest.raises(AttributeError):
        event.criterion_grade_version_uuid = criterion_grade_version_uuid
    with pytest.raises(AttributeError):
        event.embedder_uuid = embedder_uuid
    with pytest.raises(AttributeError):
        event.embedding = embedding
    with pytest.raises(AttributeError):
        event.version_uuid = "123"


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    valid_criterion_grade_embedding_parameters,
)
def test_serializing_criterion_grade_embedding(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    event = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid=criterion_grade_version_uuid,
        embedder_uuid=embedder_uuid,
        embedding=embedding,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    valid_criterion_grade_embedding_parameters,
)
def test_deserializing_criterion_grade_embedding(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    event = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid=criterion_grade_version_uuid,
        embedder_uuid=embedder_uuid,
        embedding=embedding,
    )
    serialized = event.serialize()
    deserialized = CriterionGradeEmbeddingEvent.deserialize(serialized)
    assert deserialized.criterion_grade_version_uuid == criterion_grade_version_uuid
    assert deserialized.embedder_uuid == embedder_uuid
    # Error of floating point precision
    epsilon = 1e-6
    assert [abs(a - b) < epsilon for a, b in zip(deserialized.embedding, embedding)]
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    valid_criterion_grade_embedding_parameters,
)
def test_str_criterion_grade_embedding(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    event = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid=criterion_grade_version_uuid,
        embedder_uuid=embedder_uuid,
        embedding=embedding,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "criterion_grade_version_uuid, embedder_uuid, embedding",
    valid_criterion_grade_embedding_parameters,
)
def test_publish_criterion_grade_embedding(
    criterion_grade_version_uuid, embedder_uuid, embedding
):
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent

    event = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid=criterion_grade_version_uuid,
        embedder_uuid=embedder_uuid,
        embedding=embedding,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_criterion_grade_embeddings_event_type():
    from powergrader_event_utils.events.grade import CriterionGradeEmbeddingEvent
    from powergrader_event_utils.events.event import EventType

    event = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid="uuid",
        embedder_uuid="uuid",
        embedding=[0, 0, 0],
    )
    assert event.event_type == EventType.CRITERION_GRADE_EMBEDDING
