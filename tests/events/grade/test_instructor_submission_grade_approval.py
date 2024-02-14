import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
    MockProducer,
)

valid_criterion_grade_version_uuids = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS
)
invalid_criteria_grade_version_uuids = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS], [INVALID_UUIDS, INVALID_UUIDS]
)

valid_instructor_submission_grade_approval_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, valid_criterion_grade_version_uuids, VALID_TIMESTAMPS
)
invalid_instructor_submission_grade_approval_parameters = (
    generate_singularly_invalid_permutations(
        [
            VALID_UUIDS,
            VALID_UUIDS,
            valid_criterion_grade_version_uuids,
            VALID_TIMESTAMPS,
        ],
        [
            INVALID_UUIDS,
            INVALID_UUIDS,
            invalid_criteria_grade_version_uuids,
            INVALID_TIMESTAMPS,
        ],
    )
)


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    valid_instructor_submission_grade_approval_parameters,
)
def test_valid_instructor_submission_grade_approval_creation(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
        version_timestamp=version_timestamp,
    )
    InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid,
        instructor_public_uuid,
        criterion_grade_version_uuids,
        version_timestamp,
    )
    InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid,
        instructor_public_uuid,
        criterion_grade_version_uuids,
    )


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    invalid_instructor_submission_grade_approval_parameters,
)
def test_invalid_instructor_submission_grade_approval_creation(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    with pytest.raises((TypeError, ValueError)):
        InstructorSubmissionGradeApprovalEvent(
            submission_version_uuid=submission_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            criterion_grade_version_uuids=criterion_grade_version_uuids,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        InstructorSubmissionGradeApprovalEvent(
            submission_version_uuid,
            instructor_public_uuid,
            criterion_grade_version_uuids,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    valid_instructor_submission_grade_approval_parameters,
)
def test_getting_instructor_submission_grade_approval_fields(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
        version_timestamp=version_timestamp,
    )
    assert event.submission_version_uuid == submission_version_uuid
    assert event.instructor_public_uuid == instructor_public_uuid
    assert set(event.criterion_grade_version_uuids) == set(
        criterion_grade_version_uuids
    )
    assert event.version_timestamp == version_timestamp
    assert event.version_uuid is not None

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
    )
    assert event.submission_version_uuid == submission_version_uuid
    assert event.instructor_public_uuid == instructor_public_uuid
    assert set(event.criterion_grade_version_uuids) == set(
        criterion_grade_version_uuids
    )
    assert event.version_timestamp is not None
    assert event.version_uuid is not None


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    valid_instructor_submission_grade_approval_parameters,
)
def test_setting_instructor_submission_grade_approval_fields(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        event.submission_version_uuid = submission_version_uuid
    with pytest.raises(AttributeError):
        event.instructor_public_uuid = instructor_public_uuid
    with pytest.raises(AttributeError):
        event.criterion_grade_version_uuids = criterion_grade_version_uuids
    with pytest.raises(AttributeError):
        event.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        event.version_uuid = "123"


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    valid_instructor_submission_grade_approval_parameters,
)
def test_serializing_instructor_submission_grade_approval(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
        version_timestamp=version_timestamp,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    valid_instructor_submission_grade_approval_parameters,
)
def test_deserializing_instructor_submission_grade_approval(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
        version_timestamp=version_timestamp,
    )
    serialized = event.serialize()
    deserialized = InstructorSubmissionGradeApprovalEvent.deserialize(serialized)
    assert deserialized.submission_version_uuid == submission_version_uuid
    assert deserialized.instructor_public_uuid == instructor_public_uuid
    assert set(deserialized.criterion_grade_version_uuids) == set(
        criterion_grade_version_uuids
    )
    assert deserialized.version_timestamp == version_timestamp
    assert deserialized.version_uuid == event.version_uuid


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    valid_instructor_submission_grade_approval_parameters,
)
def test_str_instructor_submission_grade_approval(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "submission_version_uuid, instructor_public_uuid, criterion_grade_version_uuids, version_timestamp",
    valid_instructor_submission_grade_approval_parameters,
)
def test_publish_instructor_submission_grade_approval(
    submission_version_uuid,
    instructor_public_uuid,
    criterion_grade_version_uuids,
    version_timestamp,
):
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid=submission_version_uuid,
        instructor_public_uuid=instructor_public_uuid,
        criterion_grade_version_uuids=criterion_grade_version_uuids,
        version_timestamp=version_timestamp,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_instructor_submission_grade_approval_event_type():
    from powergrader_event_utils.events.grade import (
        InstructorSubmissionGradeApprovalEvent,
    )
    from powergrader_event_utils.events.event import EventType

    event = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid="123",
        instructor_public_uuid="123",
        criterion_grade_version_uuids=["123"],
        version_timestamp=123,
    )
    assert event.event_type == EventType.INSTRUCTOR_SUBMISSION_GRADE_APPROVAL
