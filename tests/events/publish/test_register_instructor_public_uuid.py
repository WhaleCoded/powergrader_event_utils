import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    MockProducer,
)

from powergrader_event_utils.events.publish import LMSInstructorType

valid_instructor_types = [
    LMSInstructorType.UNSPECIFIED,
    LMSInstructorType.TA,
    LMSInstructorType.FACULTY,
]
valid_register_instructor_public_uuid_parameters = generate_all_permutations(
    VALID_UUIDS, valid_instructor_types, VALID_UUIDS
)

invalid_instructor_types = ["invalid", 5, None, 0.4, [1, 2, 3]]
invalid_register_instructor_public_uuid_parameters = (
    generate_singularly_invalid_permutations(
        [VALID_UUIDS, valid_instructor_types, VALID_UUIDS],
        [INVALID_UUIDS, invalid_instructor_types, INVALID_UUIDS],
    )
)


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    valid_register_instructor_public_uuid_parameters,
)
def test_valid_register_instructor_public_uuid_creation(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    RegisterInstructorPublicUUIDEvent(
        lms_id=lms_id,
        user_type=user_type,
        organization_public_uuid=organization_public_uuid,
    )
    RegisterInstructorPublicUUIDEvent(
        lms_id,
        user_type,
        organization_public_uuid,
    )


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    invalid_register_instructor_public_uuid_parameters,
)
def test_invalid_register_instructor_public_uuid_creation(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    with pytest.raises((TypeError, ValueError)):
        RegisterInstructorPublicUUIDEvent(
            lms_id=lms_id,
            user_type=user_type,
            organization_public_uuid=organization_public_uuid,
        )
    with pytest.raises((TypeError, ValueError)):
        RegisterInstructorPublicUUIDEvent(
            lms_id,
            user_type,
            organization_public_uuid,
        )


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    valid_register_instructor_public_uuid_parameters,
)
def test_getting_register_instructor_public_uuid_fields(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    register_instructor_public_uuid_event = RegisterInstructorPublicUUIDEvent(
        lms_id=lms_id,
        user_type=user_type,
        organization_public_uuid=organization_public_uuid,
    )
    assert register_instructor_public_uuid_event.lms_id == lms_id
    assert register_instructor_public_uuid_event.user_type == user_type
    assert (
        register_instructor_public_uuid_event.organization_public_uuid
        == organization_public_uuid
    )
    assert register_instructor_public_uuid_event.public_uuid is not None


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    valid_register_instructor_public_uuid_parameters,
)
def test_setting_register_instructor_public_uuid_fields(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    register_instructor_public_uuid_event = RegisterInstructorPublicUUIDEvent(
        lms_id=lms_id,
        user_type=user_type,
        organization_public_uuid=organization_public_uuid,
    )
    with pytest.raises(AttributeError):
        register_instructor_public_uuid_event.lms_id = lms_id
    with pytest.raises(AttributeError):
        register_instructor_public_uuid_event.user_type = user_type
    with pytest.raises(AttributeError):
        register_instructor_public_uuid_event.organization_public_uuid = (
            organization_public_uuid
        )
    with pytest.raises(AttributeError):
        register_instructor_public_uuid_event.public_uuid = "new_uuid"


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    valid_register_instructor_public_uuid_parameters,
)
def test_serialize_register_instructor_public_uuid_event(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    register_instructor_public_uuid_event = RegisterInstructorPublicUUIDEvent(
        lms_id=lms_id,
        user_type=user_type,
        organization_public_uuid=organization_public_uuid,
    )
    serialized = register_instructor_public_uuid_event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    valid_register_instructor_public_uuid_parameters,
)
def test_deserialize_register_instructor_public_uuid_event(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    register_instructor_public_uuid_event = RegisterInstructorPublicUUIDEvent(
        lms_id=lms_id,
        user_type=user_type,
        organization_public_uuid=organization_public_uuid,
    )
    serialized = register_instructor_public_uuid_event.serialize()
    deserialized = RegisterInstructorPublicUUIDEvent.deserialize(serialized)
    assert deserialized.lms_id == lms_id
    assert deserialized.user_type == user_type
    assert deserialized.organization_public_uuid == organization_public_uuid
    assert deserialized.public_uuid == register_instructor_public_uuid_event.public_uuid


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    valid_register_instructor_public_uuid_parameters,
)
def test_str_register_instructor_public_uuid_event(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    register_instructor_public_uuid_event = RegisterInstructorPublicUUIDEvent(
        lms_id=lms_id,
        user_type=user_type,
        organization_public_uuid=organization_public_uuid,
    )
    assert isinstance(str(register_instructor_public_uuid_event), str)


@pytest.mark.parametrize(
    "lms_id, user_type, organization_public_uuid",
    valid_register_instructor_public_uuid_parameters,
)
def test_publish_register_instructor_public_uuid_event(
    lms_id, user_type, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent

    event = RegisterInstructorPublicUUIDEvent(
        lms_id=lms_id,
        user_type=user_type,
        organization_public_uuid=organization_public_uuid,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_register_instructor_public_uuid_event_type():
    from powergrader_event_utils.events.publish import RegisterInstructorPublicUUIDEvent
    from powergrader_event_utils.events.event import EventType

    event = RegisterInstructorPublicUUIDEvent(
        lms_id="lms_id",
        user_type=LMSInstructorType.UNSPECIFIED,
        organization_public_uuid="organization_public_uuid",
    )
    assert event.event_type == EventType.REGISTER_INSTRUCTOR_PUBLIC_UUID
