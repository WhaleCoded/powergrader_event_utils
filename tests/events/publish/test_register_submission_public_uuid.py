import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    MockProducer,
)

valid_register_submission_public_uuid_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_UUIDS
)
invalid_register_submission_public_uuid_parameters = (
    generate_singularly_invalid_permutations(
        [VALID_UUIDS, VALID_UUIDS, VALID_UUIDS],
        [INVALID_UUIDS, INVALID_UUIDS, INVALID_UUIDS],
    )
)


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    valid_register_submission_public_uuid_parameters,
)
def test_valid_register_submission_public_uuid_creation(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id=lms_assignment_id,
        lms_student_id=lms_student_id,
        organization_public_uuid=organization_public_uuid,
    )
    RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id,
        lms_student_id,
        organization_public_uuid,
    )


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    invalid_register_submission_public_uuid_parameters,
)
def test_invalid_register_submission_public_uuid_creation(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    with pytest.raises((TypeError, ValueError)):
        RegisterSubmissionPublicUUIDEvent(
            lms_assignment_id=lms_assignment_id,
            lms_student_id=lms_student_id,
            organization_public_uuid=organization_public_uuid,
        )
    with pytest.raises((TypeError, ValueError)):
        RegisterSubmissionPublicUUIDEvent(
            lms_assignment_id,
            lms_student_id,
            organization_public_uuid,
        )


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    valid_register_submission_public_uuid_parameters,
)
def test_getting_register_submission_public_uuid_fields(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    event = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id=lms_assignment_id,
        lms_student_id=lms_student_id,
        organization_public_uuid=organization_public_uuid,
    )
    assert event.lms_assignment_id == lms_assignment_id
    assert event.lms_student_id == lms_student_id
    assert event.organization_public_uuid == organization_public_uuid
    assert event.public_uuid is not None


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    valid_register_submission_public_uuid_parameters,
)
def test_setting_register_submission_public_uuid_fields(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    event = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id=lms_assignment_id,
        lms_student_id=lms_student_id,
        organization_public_uuid=organization_public_uuid,
    )
    with pytest.raises(AttributeError):
        event.lms_assignment_id = lms_assignment_id
    with pytest.raises(AttributeError):
        event.lms_student_id = lms_student_id
    with pytest.raises(AttributeError):
        event.organization_public_uuid = organization_public_uuid
    with pytest.raises(AttributeError):
        event.public_uuid = "some_uuid"


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    valid_register_submission_public_uuid_parameters,
)
def test_serialize_register_submission_public_uuid(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    event = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id=lms_assignment_id,
        lms_student_id=lms_student_id,
        organization_public_uuid=organization_public_uuid,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    valid_register_submission_public_uuid_parameters,
)
def test_deserialize_register_submission_public_uuid(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    event = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id=lms_assignment_id,
        lms_student_id=lms_student_id,
        organization_public_uuid=organization_public_uuid,
    )
    serialized = event.serialize()
    deserialized = RegisterSubmissionPublicUUIDEvent.deserialize(serialized)
    assert deserialized.lms_assignment_id == lms_assignment_id
    assert deserialized.lms_student_id == lms_student_id
    assert deserialized.organization_public_uuid == organization_public_uuid
    assert deserialized.public_uuid == event.public_uuid


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    valid_register_submission_public_uuid_parameters,
)
def test_str_register_submission_public_uuid(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    event = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id=lms_assignment_id,
        lms_student_id=lms_student_id,
        organization_public_uuid=organization_public_uuid,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "lms_assignment_id, lms_student_id, organization_public_uuid",
    valid_register_submission_public_uuid_parameters,
)
def test_publish_register_submission_public_uuid(
    lms_assignment_id, lms_student_id, organization_public_uuid
):
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent

    event = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id=lms_assignment_id,
        lms_student_id=lms_student_id,
        organization_public_uuid=organization_public_uuid,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_register_submission_public_uuid_event_type():
    from powergrader_event_utils.events.publish import RegisterSubmissionPublicUUIDEvent
    from powergrader_event_utils.events.event import EventType

    event = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id="1234-5678-91011-1213",
        lms_student_id="1234-5678-91011-1213",
        organization_public_uuid="1234-5678-91011-1213",
    )
    assert event.event_type == EventType.REGISTER_SUBMISSION_PUBLIC_UUID
    deserialized = RegisterSubmissionPublicUUIDEvent.deserialize(event.serialize())
    assert deserialized.event_type == EventType.REGISTER_SUBMISSION_PUBLIC_UUID
