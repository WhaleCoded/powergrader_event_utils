import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
    VALID_INTS,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
    MockProducer,
)

from powergrader_event_utils.events.assignment import CriterionLevel, RubricCriterion

criterion_levels = [
    CriterionLevel(s, d) for s, d in generate_all_permutations(VALID_INTS, VALID_STRS)
]
rubric_criterion_parameters = generate_all_permutations(
    VALID_STRS,
    [criterion_levels[:2], criterion_levels],
)
rubric_criterion = [
    RubricCriterion(name, levels) for name, levels in rubric_criterion_parameters
]

invalid_rubric_criterion = [
    -1,
    [],
    [1, 2, 3],
    {"a": "b"},
    rubric_criterion[0],
]
valid_rubric_criteria = [
    list({criterion.name: criterion for criterion in rubric_criterion[:5]}.values()),
    list({criterion.name: criterion for criterion in rubric_criterion[5:]}.values()),
    {criterion.name: criterion for criterion in rubric_criterion},
    {rubric_criterion[0].name: rubric_criterion[0]},
    [rubric_criterion[0]],
]

valid_rubric_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_STRS, valid_rubric_criteria, VALID_TIMESTAMPS
)
invalid_rubric_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_STRS, valid_rubric_criteria, VALID_TIMESTAMPS],
    [
        INVALID_UUIDS,
        INVALID_UUIDS,
        INVALID_STRS,
        invalid_rubric_criterion,
        INVALID_TIMESTAMPS,
    ],
)


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    valid_rubric_parameters,
)
def test_valid_rubric_creation(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
        version_timestamp=version_timestamp,
    )
    RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
    )
    RubricEvent(
        public_uuid,
        instructor_public_uuid,
        name,
        rubric_criteria,
        version_timestamp,
    )
    RubricEvent(public_uuid, instructor_public_uuid, name, rubric_criteria)


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    invalid_rubric_parameters,
)
def test_invalid_rubric_creation(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    with pytest.raises((TypeError, ValueError)):
        RubricEvent(
            public_uuid=public_uuid,
            instructor_public_uuid=instructor_public_uuid,
            name=name,
            rubric_criteria=rubric_criteria,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        RubricEvent(
            public_uuid,
            instructor_public_uuid,
            name,
            rubric_criteria,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    valid_rubric_parameters,
)
def test_getting_rubric_fields(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    rubric = RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
        version_timestamp=version_timestamp,
    )
    assert rubric.public_uuid == public_uuid
    assert rubric.instructor_public_uuid == instructor_public_uuid
    assert rubric.name == name
    if isinstance(rubric_criteria, dict):
        rubric_criteria = list(rubric_criteria.values())
    print(len(rubric_criteria))
    if len(rubric_criteria) == 3:
        print(rubric_criteria[1])
        print(
            "\n".join([str(criterion) for criterion in rubric.rubric_criteria.values()])
        )
    assert all(
        [criterion in rubric.rubric_criteria.values() for criterion in rubric_criteria]
    )
    assert rubric.version_timestamp == version_timestamp
    assert rubric.version_uuid is not None

    rubric = RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
    )
    assert rubric.public_uuid == public_uuid
    assert rubric.instructor_public_uuid == instructor_public_uuid
    assert rubric.name == name
    if isinstance(rubric_criteria, dict):
        rubric_criteria = list(rubric_criteria.values())
    print(len(rubric_criteria))
    if len(rubric_criteria) == 3:
        print(rubric_criteria[1])
        print(
            "\n".join([str(criterion) for criterion in rubric.rubric_criteria.values()])
        )
    assert all(
        [criterion in rubric.rubric_criteria.values() for criterion in rubric_criteria]
    )
    assert rubric.version_timestamp is not None
    assert rubric.version_uuid is not None


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    valid_rubric_parameters,
)
def test_setting_rubric_fields(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    rubric = RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        rubric.public_uuid = public_uuid
    with pytest.raises(AttributeError):
        rubric.instructor_public_uuid = instructor_public_uuid
    with pytest.raises(AttributeError):
        rubric.name = name
    with pytest.raises(AttributeError):
        rubric.rubric_criteria = rubric_criteria
    with pytest.raises(AttributeError):
        rubric.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        rubric.version_uuid = rubric.version_uuid


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    valid_rubric_parameters,
)
def test_serializing_rubric(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    rubric = RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
        version_timestamp=version_timestamp,
    )
    serialized = rubric.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    valid_rubric_parameters,
)
def test_deserializing_rubric(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    rubric = RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
        version_timestamp=version_timestamp,
    )
    serialized = rubric.serialize()
    deserialized = RubricEvent.deserialize(serialized)
    assert rubric.version_uuid == deserialized.version_uuid
    assert rubric.public_uuid == deserialized.public_uuid
    assert rubric.instructor_public_uuid == deserialized.instructor_public_uuid
    assert rubric.name == deserialized.name
    assert all(
        [
            criterion in deserialized.rubric_criteria.values()
            for criterion in rubric.rubric_criteria.values()
        ]
    )
    assert rubric.version_timestamp == deserialized.version_timestamp
    assert rubric.version_uuid == deserialized.version_uuid


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    valid_rubric_parameters,
)
def test_str_rubric(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    rubric = RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(rubric), str)


@pytest.mark.parametrize(
    "public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp",
    valid_rubric_parameters,
)
def test_publish_rubric(
    public_uuid, instructor_public_uuid, name, rubric_criteria, version_timestamp
):
    from powergrader_event_utils.events.assignment import RubricEvent

    event = RubricEvent(
        public_uuid=public_uuid,
        instructor_public_uuid=instructor_public_uuid,
        name=name,
        rubric_criteria=rubric_criteria,
        version_timestamp=version_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_assignment_event_type():
    from powergrader_event_utils.events.assignment import RubricEvent
    from powergrader_event_utils.events.event import EventType

    event = RubricEvent(
        public_uuid="uuid",
        instructor_public_uuid="uuid",
        name="name",
        rubric_criteria=[rubric_criterion[0]],
        version_timestamp=0,
    )
    assert event.event_type == EventType.RUBRIC
    deserialized = RubricEvent.deserialize(event.serialize())
    assert deserialized.event_type == EventType.RUBRIC
