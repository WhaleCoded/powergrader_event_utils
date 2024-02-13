import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_TIMESTAMPS,
    INVALID_TIMESTAMPS,
)

valid_submission_parameters = generate_all_permutations(
    VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_TIMESTAMPS
)
invalid_submission_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_UUIDS, VALID_TIMESTAMPS],
    [INVALID_UUIDS, INVALID_UUIDS, INVALID_UUIDS, INVALID_UUIDS, INVALID_TIMESTAMPS],
)


@pytest.mark.parametrize(
    "public_uuid, student_public_uuid, assignment_version_uuid, submission_file_group_uuid, version_timestamp",
    valid_submission_parameters,
)
def test_valid_submission_creation(
    public_uuid,
    student_public_uuid,
    assignment_version_uuid,
    submission_file_group_uuid,
    version_timestamp,
):
    from powergrader_event_utils.events.submission import SubmissionEvent

    SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
        version_timestamp=version_timestamp,
    )
    SubmissionEvent(
        public_uuid,
        student_public_uuid,
        assignment_version_uuid,
        submission_file_group_uuid,
        version_timestamp,
    )
    SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
    )
    SubmissionEvent(
        public_uuid,
        student_public_uuid,
        assignment_version_uuid,
        submission_file_group_uuid,
    )


@pytest.mark.parametrize(
    "public_uuid, student_public_uuid, assignment_version_uuid, submission_file_group_uuid, version_timestamp",
    invalid_submission_parameters,
)
def test_invalid_submission_creation(
    public_uuid,
    student_public_uuid,
    assignment_version_uuid,
    submission_file_group_uuid,
    version_timestamp,
):
    from powergrader_event_utils.events.submission import SubmissionEvent

    with pytest.raises((TypeError, ValueError)):
        SubmissionEvent(
            public_uuid=public_uuid,
            student_public_uuid=student_public_uuid,
            assignment_version_uuid=assignment_version_uuid,
            submission_file_group_uuid=submission_file_group_uuid,
            version_timestamp=version_timestamp,
        )
    with pytest.raises((TypeError, ValueError)):
        SubmissionEvent(
            public_uuid,
            student_public_uuid,
            assignment_version_uuid,
            submission_file_group_uuid,
            version_timestamp,
        )


@pytest.mark.parametrize(
    "public_uuid, student_public_uuid, assignment_version_uuid, submission_file_group_uuid, version_timestamp",
    valid_submission_parameters,
)
def test_getting_submission_fields(
    public_uuid,
    student_public_uuid,
    assignment_version_uuid,
    submission_file_group_uuid,
    version_timestamp,
):
    from powergrader_event_utils.events.submission import SubmissionEvent

    event = SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
        version_timestamp=version_timestamp,
    )
    assert event.public_uuid == public_uuid
    assert event.student_public_uuid == student_public_uuid
    assert event.assignment_version_uuid == assignment_version_uuid
    assert event.submission_file_group_uuid == submission_file_group_uuid
    assert event.version_timestamp == version_timestamp
    assert event.version_uuid is not None

    event = SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
    )
    assert event.public_uuid == public_uuid
    assert event.student_public_uuid == student_public_uuid
    assert event.assignment_version_uuid == assignment_version_uuid
    assert event.submission_file_group_uuid == submission_file_group_uuid
    assert event.version_timestamp is not None
    assert event.version_uuid is not None


@pytest.mark.parametrize(
    "public_uuid, student_public_uuid, assignment_version_uuid, submission_file_group_uuid, version_timestamp",
    valid_submission_parameters,
)
def test_setting_submission_fields(
    public_uuid,
    student_public_uuid,
    assignment_version_uuid,
    submission_file_group_uuid,
    version_timestamp,
):
    from powergrader_event_utils.events.submission import SubmissionEvent

    event = SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
        version_timestamp=version_timestamp,
    )
    with pytest.raises(AttributeError):
        event.public_uuid = public_uuid
    with pytest.raises(AttributeError):
        event.student_public_uuid = student_public_uuid
    with pytest.raises(AttributeError):
        event.assignment_version_uuid = assignment_version_uuid
    with pytest.raises(AttributeError):
        event.submission_file_group_uuid = submission_file_group_uuid
    with pytest.raises(AttributeError):
        event.version_timestamp = version_timestamp
    with pytest.raises(AttributeError):
        event.version_uuid = "123"


@pytest.mark.parametrize(
    "public_uuid, student_public_uuid, assignment_version_uuid, submission_file_group_uuid, version_timestamp",
    valid_submission_parameters,
)
def test_serialize_submission(
    public_uuid,
    student_public_uuid,
    assignment_version_uuid,
    submission_file_group_uuid,
    version_timestamp,
):
    from powergrader_event_utils.events.submission import SubmissionEvent

    event = SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
        version_timestamp=version_timestamp,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "public_uuid, student_public_uuid, assignment_version_uuid, submission_file_group_uuid, version_timestamp",
    valid_submission_parameters,
)
def test_deserialize_submission(
    public_uuid,
    student_public_uuid,
    assignment_version_uuid,
    submission_file_group_uuid,
    version_timestamp,
):
    from powergrader_event_utils.events.submission import SubmissionEvent

    event = SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
        version_timestamp=version_timestamp,
    )
    serialized = event.serialize()
    deserialized = SubmissionEvent.deserialize(serialized)
    assert deserialized.public_uuid == public_uuid
    assert deserialized.student_public_uuid == student_public_uuid
    assert deserialized.assignment_version_uuid == assignment_version_uuid
    assert deserialized.submission_file_group_uuid == submission_file_group_uuid
    assert deserialized.version_timestamp == version_timestamp


@pytest.mark.parametrize(
    "public_uuid, student_public_uuid, assignment_version_uuid, submission_file_group_uuid, version_timestamp",
    valid_submission_parameters,
)
def test_str_submission(
    public_uuid,
    student_public_uuid,
    assignment_version_uuid,
    submission_file_group_uuid,
    version_timestamp,
):
    from powergrader_event_utils.events.submission import SubmissionEvent

    event = SubmissionEvent(
        public_uuid=public_uuid,
        student_public_uuid=student_public_uuid,
        assignment_version_uuid=assignment_version_uuid,
        submission_file_group_uuid=submission_file_group_uuid,
        version_timestamp=version_timestamp,
    )
    assert isinstance(str(event), str)


def test_submission_event_type():
    from powergrader_event_utils.events.submission import SubmissionEvent
    from powergrader_event_utils.events.event import EventType

    event = SubmissionEvent(
        public_uuid="public_uuid",
        student_public_uuid="student_public_uuid",
        assignment_version_uuid="assignment_version_uuid",
        submission_file_group_uuid="submission_file_group_uuid",
        version_timestamp=123,
    )
    assert event.event_type == EventType.SUBMISSION
