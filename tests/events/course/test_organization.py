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

valid_organization_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_STRS, VALID_TIMESTAMPS
)
invalid_organization_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_STRS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_STRS, INVALID_TIMESTAMPS],
)


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", valid_organization_parameters
)
def test_valid_organization_creation(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
        version_timestamp=version_timestamp,
    )
    OrganizationEvent(
        public_uuid,
        name,
        version_timestamp,
    )
    OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
    )
    OrganizationEvent(
        public_uuid,
        name,
    )


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", invalid_organization_parameters
)
def test_invalid_organization_creation(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    with pytest.raises((TypeError, ValueError)):
        OrganizationEvent(
            public_uuid=public_uuid,
            name=name,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        OrganizationEvent(
            public_uuid,
            name,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", valid_organization_parameters
)
def test_getting_organization_attributes(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    organization = OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
        version_timestamp=version_timestamp,
    )
    assert organization.public_uuid == public_uuid
    assert organization.name == name
    assert organization.version_timestamp == version_timestamp
    assert organization.version_uuid is not None

    organization = OrganizationEvent(public_uuid=public_uuid, name=name)
    assert organization.public_uuid == public_uuid
    assert organization.name == name
    assert organization.version_timestamp is not None
    assert organization.version_uuid is not None


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", valid_organization_parameters
)
def test_setting_organization_attributes(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    organization = OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        organization.public_uuid = public_uuid
    with pytest.raises(AttributeError):
        organization.name = name
    with pytest.raises(AttributeError):
        organization.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        organization.version_uuid = "some_uuid"


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", valid_organization_parameters
)
def test_serialize_organization(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    organization = OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
        version_timestamp=version_timestamp,
    )
    serialized = organization.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", valid_organization_parameters
)
def test_deserialize_organization(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    organization = OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
        version_timestamp=version_timestamp,
    )
    serialized = organization.serialize()
    deserialized = OrganizationEvent.deserialize(serialized)
    assert deserialized.public_uuid == public_uuid
    assert deserialized.name == name
    assert deserialized.version_timestamp == version_timestamp
    assert deserialized.version_uuid == organization.version_uuid


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", valid_organization_parameters
)
def test_str_organization(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    organization = OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(organization), str)


@pytest.mark.parametrize(
    "public_uuid, name, version_timestamp", valid_organization_parameters
)
def test_publish_organization(public_uuid, name, version_timestamp):
    from powergrader_event_utils.events.course import OrganizationEvent

    event = OrganizationEvent(
        public_uuid=public_uuid,
        name=name,
        version_timestamp=version_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_organization_event_type():
    from powergrader_event_utils.events.course import OrganizationEvent
    from powergrader_event_utils.events.event import EventType

    event = OrganizationEvent(
        public_uuid="some_uuid",
        name="some_name",
        version_timestamp=1234567890,
    )
    assert event.event_type == EventType.ORGANIZATION
