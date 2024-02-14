import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    MockProducer,
)

valid_register_parameters = generate_all_permutations(VALID_UUIDS, VALID_UUIDS)
invalid_register_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS], [INVALID_UUIDS, INVALID_UUIDS]
)

from powergrader_event_utils.events.publish import (
    RegisterCoursePublicUUIDEvent,
    RegisterSectionPublicUUIDEvent,
    RegisterStudentPublicUUIDEvent,
    RegisterAssignmentPublicUUIDEvent,
    RegisterRubricPublicUUIDEvent,
)
from powergrader_event_utils.events.event import EventType

register_types = [
    RegisterCoursePublicUUIDEvent,
    RegisterSectionPublicUUIDEvent,
    RegisterStudentPublicUUIDEvent,
    RegisterAssignmentPublicUUIDEvent,
    RegisterRubricPublicUUIDEvent,
]
event_types = [
    EventType.REGISTER_COURSE_PUBLIC_UUID,
    EventType.REGISTER_SECTION_PUBLIC_UUID,
    EventType.REGISTER_STUDENT_PUBLIC_UUID,
    EventType.REGISTER_ASSIGNMENT_PUBLIC_UUID,
    EventType.REGISTER_RUBRIC_PUBLIC_UUID,
]

new_valid_register_parameters = []
new_invalid_register_parameters = []
for register_type in register_types:
    for valid in valid_register_parameters:
        valid = tuple(list(valid) + [register_type])
        new_valid_register_parameters.append(valid)
    for invalid in invalid_register_parameters:
        invalid = tuple(list(invalid) + [register_type])
        new_invalid_register_parameters.append(invalid)
valid_register_parameters = new_valid_register_parameters
invalid_register_parameters = new_invalid_register_parameters


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    valid_register_parameters,
)
def test_valid_register_type_creation(
    lms_id, organization_public_uuid, register_event_type
):
    register_event_type(
        lms_id=lms_id,
        organization_public_uuid=organization_public_uuid,
    )
    register_event_type(
        lms_id,
        organization_public_uuid,
    )


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    invalid_register_parameters,
)
def test_invalid_register_type_creation(
    lms_id, organization_public_uuid, register_event_type
):
    with pytest.raises((TypeError, ValueError)):
        register_event_type(
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )
    with pytest.raises((TypeError, ValueError)):
        register_event_type(
            lms_id,
            organization_public_uuid,
        )


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    valid_register_parameters,
)
def test_getting_register_type_attributes(
    lms_id, organization_public_uuid, register_event_type
):
    register_event = register_event_type(
        lms_id=lms_id,
        organization_public_uuid=organization_public_uuid,
    )
    assert register_event.lms_id == lms_id
    assert register_event.organization_public_uuid == organization_public_uuid
    assert register_event.public_uuid is not None


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    valid_register_parameters,
)
def test_setting_register_type_attributes(
    lms_id, organization_public_uuid, register_event_type
):
    register_event = register_event_type(
        lms_id=lms_id,
        organization_public_uuid=organization_public_uuid,
    )
    with pytest.raises(AttributeError):
        register_event.lms_id = lms_id
    with pytest.raises(AttributeError):
        register_event.organization_public_uuid = organization_public_uuid
    with pytest.raises(AttributeError):
        register_event.public_uuid = "1234-5678-91011-1213"


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    valid_register_parameters,
)
def test_serialize_register_type(lms_id, organization_public_uuid, register_event_type):
    register_event = register_event_type(
        lms_id=lms_id,
        organization_public_uuid=organization_public_uuid,
    )
    serialized = register_event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    valid_register_parameters,
)
def test_deserialize_register_type(
    lms_id, organization_public_uuid, register_event_type
):
    register_event = register_event_type(
        lms_id=lms_id,
        organization_public_uuid=organization_public_uuid,
    )
    serialized = register_event.serialize()
    deserialized = register_event_type.deserialize(serialized)
    assert deserialized.lms_id == lms_id
    assert deserialized.organization_public_uuid == organization_public_uuid
    assert deserialized.public_uuid == register_event.public_uuid


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    valid_register_parameters,
)
def test_str_register_type(lms_id, organization_public_uuid, register_event_type):
    register_event = register_event_type(
        lms_id=lms_id,
        organization_public_uuid=organization_public_uuid,
    )
    assert isinstance(str(register_event), str)


@pytest.mark.parametrize(
    "lms_id, organization_public_uuid, register_event_type",
    valid_register_parameters,
)
def test_publish_register_type(lms_id, organization_public_uuid, register_event_type):
    event = register_event_type(
        lms_id=lms_id,
        organization_public_uuid=organization_public_uuid,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


@pytest.mark.parametrize(
    "register_event_type, event_type",
    zip(register_types, event_types),
)
def test_register_type_event_type(register_event_type, event_type):
    register_event = register_event_type(
        lms_id="lms_id",
        organization_public_uuid="organization_public_uuid",
    )
    assert register_event.event_type == event_type
