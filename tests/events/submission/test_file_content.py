import pytest
from helpers.utils import (
    generate_all_permutations,
    generate_singularly_invalid_permutations,
    VALID_STRS,
    INVALID_STRS,
)

valid_content = [
    "This is a valid content",
    "This is another valid content",
    "This is yet another valid content",
    b"This is a valid content",
    [14, 25, 255, 16],
]
invalid_content = [
    14,
    {"key": "value"},
    None,
    20.5,
    [14, 25, 427, 16],
]

valid_file_content_parameters = generate_all_permutations(
    VALID_STRS, VALID_STRS, valid_content
)
invalid_file_content_parameters = generate_singularly_invalid_permutations(
    [VALID_STRS, VALID_STRS, valid_content],
    [INVALID_STRS, INVALID_STRS, invalid_content],
)


@pytest.mark.parametrize(
    "file_name, file_type, content",
    valid_file_content_parameters,
)
def test_valid_file_content_creation(file_name, file_type, content):
    from powergrader_event_utils.events.submission import FileContent

    FileContent(
        file_name=file_name,
        file_type=file_type,
        content=content,
    )
    FileContent(file_name, file_type, content)


@pytest.mark.parametrize(
    "file_name, file_type, content",
    invalid_file_content_parameters,
)
def test_invalid_file_content_creation(file_name, file_type, content):
    from powergrader_event_utils.events.submission import FileContent

    with pytest.raises((TypeError, ValueError)):
        FileContent(
            file_name=file_name,
            file_type=file_type,
            content=content,
        )
    with pytest.raises((TypeError, ValueError)):
        FileContent(file_name, file_type, content)


@pytest.mark.parametrize(
    "file_name, file_type, content",
    valid_file_content_parameters,
)
def test_getting_file_content_fields(file_name, file_type, content):
    from powergrader_event_utils.events.submission import FileContent

    event = FileContent(
        file_name=file_name,
        file_type=file_type,
        content=content,
    )
    assert event.file_name == file_name
    assert event.file_type == file_type
    if isinstance(content, bytes):
        assert event.content == content
    elif isinstance(content, str):
        assert event.content == content.encode("utf-8")
    else:
        assert event.content == bytes(content)


@pytest.mark.parametrize(
    "file_name, file_type, content",
    valid_file_content_parameters,
)
def test_setting_file_content_fields(file_name, file_type, content):
    from powergrader_event_utils.events.submission import FileContent

    event = FileContent(
        file_name=file_name,
        file_type=file_type,
        content=content,
    )
    with pytest.raises(AttributeError):
        event.file_name = file_name
    with pytest.raises(AttributeError):
        event.file_type = file_type
    with pytest.raises(AttributeError):
        event.content = content


@pytest.mark.parametrize(
    "file_name, file_type, content",
    valid_file_content_parameters,
)
def test_str_file_content(file_name, file_type, content):
    from powergrader_event_utils.events.submission import FileContent

    event = FileContent(
        file_name=file_name,
        file_type=file_type,
        content=content,
    )
    assert isinstance(str(event), str)
