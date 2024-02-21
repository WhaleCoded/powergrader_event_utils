import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
    MockProducer,
)

valid_user_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_STRS, VALID_STRS, VALID_TIMESTAMPS
)
invalid_user_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_STRS, VALID_STRS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_STRS, INVALID_STRS, INVALID_TIMESTAMPS],
)

from powergrader_event_utils.events.user import StudentEvent, InstructorEvent
from powergrader_event_utils.events.event import EventType

user_types = [StudentEvent, InstructorEvent]
event_types = [EventType.STUDENT, EventType.INSTRUCTOR]

new_valid_user_parameters = []
new_invalid_user_parameters = []
for user_type, event_type in zip(user_types, event_types):
    for valid_user_parameter in valid_user_parameters:
        new_valid_user_parameters.append((*valid_user_parameter, user_type))
    for invalid_user_parameter in invalid_user_parameters:
        new_invalid_user_parameters.append((*invalid_user_parameter, user_type))
valid_user_parameters = new_valid_user_parameters
invalid_user_parameters = new_invalid_user_parameters


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    valid_user_parameters,
)
def test_valid_user_creation(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    user_type(
        public_uuid=public_uuid,
        name=name,
        email=email,
        version_timestamp=version_timestamp,
    )
    user_type(public_uuid, name, email, version_timestamp)
    user_type(public_uuid=public_uuid, name=name, email=email)
    user_type(public_uuid, name, email)


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    invalid_user_parameters,
)
def test_invalid_user_creation(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    with pytest.raises((TypeError, ValueError)):
        user_type(
            public_uuid=public_uuid,
            name=name,
            email=email,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        user_type(
            public_uuid,
            name,
            email,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    valid_user_parameters,
)
def test_getting_user_fields(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    user = user_type(
        public_uuid=public_uuid,
        name=name,
        email=email,
        version_timestamp=version_timestamp,
    )
    assert user.public_uuid == public_uuid
    assert user.name == name
    assert user.email == email
    assert user.version_timestamp == version_timestamp
    assert user.version_uuid is not None

    user = user_type(public_uuid=public_uuid, name=name, email=email)
    assert user.public_uuid == public_uuid
    assert user.name == name
    assert user.email == email
    assert user.version_timestamp is not None
    assert user.version_uuid is not None


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    valid_user_parameters,
)
def test_setting_user_fields(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    user = user_type(
        public_uuid=public_uuid,
        name=name,
        email=email,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        user.public_uuid = public_uuid
    with pytest.raises(AttributeError):
        user.name = name
    with pytest.raises(AttributeError):
        user.email = email
    with pytest.raises(AttributeError):
        user.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        user.version_uuid = "1234-5678-91011-1213"


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    valid_user_parameters,
)
def test_serialize_user(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    user = user_type(
        public_uuid=public_uuid,
        name=name,
        email=email,
        version_timestamp=version_timestamp,
    )
    serialized = user.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    valid_user_parameters,
)
def test_deserialize_user(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    user = user_type(
        public_uuid=public_uuid,
        name=name,
        email=email,
        version_timestamp=version_timestamp,
    )
    serialized = user.serialize()
    deserialized = user_type.deserialize(serialized)
    assert deserialized.public_uuid == public_uuid
    assert deserialized.name == name
    assert deserialized.email == email
    assert deserialized.version_timestamp == version_timestamp
    assert deserialized.version_uuid == user.version_uuid


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    valid_user_parameters,
)
def test_str_user(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    user = user_type(
        public_uuid=public_uuid,
        name=name,
        email=email,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(user), str)


@pytest.mark.parametrize(
    "public_uuid, name, email, version_timestamp, user_type",
    valid_user_parameters,
)
def test_publish_user(
    public_uuid,
    name,
    email,
    version_timestamp,
    user_type,
):
    event = user_type(
        public_uuid=public_uuid,
        name=name,
        email=email,
        version_timestamp=version_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


@pytest.mark.parametrize(
    "user_type, event_type",
    zip(user_types, event_types),
)
def test_user_event_type(
    user_type,
    event_type,
):
    user = user_type(
        public_uuid="1234-5678-91011-1213",
        name="John Doe",
        email="johndoe@gmail.com",
        version_timestamp=1245,
    )
    assert user.event_type == event_type
    deserialized = user_type.deserialize(user.serialize())
    assert deserialized.event_type == event_type
