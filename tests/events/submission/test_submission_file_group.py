import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_UUIDS,
    INVALID_UUIDS,
    VALID_STRS,
    MockProducer,
)

from powergrader_event_utils.events.submission import FileContent

content = [
    "This is a valid content",
    "This is another valid content",
    "This is yet another valid content",
    b"This is a valid content",
    [14, 25, 255, 16],
]
file_content_parameters = generate_all_permutations(VALID_STRS, VALID_STRS, content)
file_contents = [FileContent(*params) for params in file_content_parameters][:4]

valid_file_contents = [file_contents, file_contents[:3], [file_contents[0]]]

invalid_content = [
    14,
    {"key": "value"},
    None,
    20.5,
    [14, 25, 427, 16],
    valid_file_contents[0][0],
]

valid_submission_file_group_parameters = generate_all_permutations(
    VALID_UUIDS, valid_file_contents
)
invalid_submission_file_group_parameters = generate_singularly_invalid_permutations(
    [VALID_UUIDS, valid_file_contents],
    [INVALID_UUIDS, invalid_content],
)


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    valid_submission_file_group_parameters,
)
def test_valid_submission_file_group_creation(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=file_contents,
    )
    SubmissionFileGroupEvent(student_public_uuid, file_contents)


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    invalid_submission_file_group_parameters,
)
def test_invalid_submission_file_group_creation(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    with pytest.raises((TypeError, ValueError)):
        SubmissionFileGroupEvent(
            student_public_uuid=student_public_uuid,
            file_contents=file_contents,
        )


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    valid_submission_file_group_parameters,
)
def test_getting_submission_file_group_fields(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    event = SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=file_contents,
    )
    assert event.student_public_uuid == student_public_uuid
    assert all(file_content in event.file_contents for file_content in file_contents)
    assert event.uuid is not None


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    valid_submission_file_group_parameters,
)
def test_setting_submission_file_group_fields(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    event = SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=file_contents,
    )
    with pytest.raises(AttributeError):
        event.student_public_uuid = student_public_uuid
    with pytest.raises(AttributeError):
        event.file_contents = file_contents


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    valid_submission_file_group_parameters,
)
def test_serialize_submission_file_group(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    event = SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=file_contents,
    )
    serialized = event.serialize()
    assert serialized is not None
    assert isinstance(serialized, bytes)
    assert len(serialized) > 0


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    valid_submission_file_group_parameters,
)
def test_deserialize_submission_file_group(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    event = SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=file_contents,
    )
    serialized = event.serialize()
    deserialized = SubmissionFileGroupEvent.deserialize(serialized)
    assert deserialized.student_public_uuid == student_public_uuid
    assert all(
        file_content in deserialized.file_contents for file_content in file_contents
    )
    assert deserialized.uuid == event.uuid


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    valid_submission_file_group_parameters,
)
def test_str_submission_file_group(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    event = SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=file_contents,
    )
    assert isinstance(str(event), str)


@pytest.mark.parametrize(
    "student_public_uuid, file_contents",
    valid_submission_file_group_parameters,
)
def test_publish_submission_file_group(student_public_uuid, file_contents):
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent

    event = SubmissionFileGroupEvent(
        student_public_uuid=student_public_uuid,
        file_contents=file_contents,
    )
    producer = MockProducer()
    event.publish(producer)
    event.publish(producer, secondary_publishing_topics=["one", "two"])
    assert producer.was_called


def test_submission_file_group_event_type():
    from powergrader_event_utils.events.submission import SubmissionFileGroupEvent
    from powergrader_event_utils.events.event import EventType

    event = SubmissionFileGroupEvent(
        student_public_uuid="student_public_uuid",
        file_contents=[FileContent("file_name", "file_type", "content")],
    )
    assert event.event_type == EventType.SUBMISSION_FILE_GROUP
