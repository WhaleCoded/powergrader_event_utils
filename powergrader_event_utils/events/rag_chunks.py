from typing import Dict, List, Sequence, Union, Optional, Self

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.rag_chunks_pb2 import (
    Code as CodeProto,
    CodeBlock as CodeBlockProto,
    List as ListProto,
    Markdown as MarkdownProto,
    MarkdownSection as MarkdownSectionProto,
    PythonCode as PythonCodeProto,
    PythonFunction as PythonFunctionProto,
    PythonClass as PythonClassProto,
    PythonCodePassage as PythonCodePassageProto,
    Text as TextProto,
    Paragraph as ParagraphProto,
    TextPassage as TextPassageProto,
    Chunk as ChunkProto,
    DocumentRoot as DocumentRootProto,
)

from powergrader_event_utils.events.proto import ProtoWrapper, ProtoEnumWrapper


class DocumentRoot(ProtoWrapper):
    proto_type = DocumentRootProto

    uuid: str
    name: Optional[str]
    source_public_uuid: str
    content_uuid: str

    def __init__(
        self,
        source_public_uuid: str,
        name: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.source_public_uuid = source_public_uuid
        self.name = name

    def add_content(self, content: Union["Section", "Passage"]) -> None:
        if not isinstance(content, Section) and not isinstance(content, Passage):
            raise ValueError("Content must be a section or passage.")
        if isinstance(self, ProtoWrapper):
            self._ProtoWrapper__frozen = False
            self.content_uuid = content.uuid
            self._ProtoWrapper__frozen = True
        else:
            self.content_uuid = content.uuid


class Section:
    """Abstract class for a section of a document.

    A section is a part of a document that contains other sections or passages. This
    class is used for type hinting and instance checking."""

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def add_child(self, child: Union["Section", "Passage"]) -> None:
        if not isinstance(child, Passage) and not isinstance(child, Section):
            raise ValueError("Child must be a passage or section.")
        if isinstance(self, ProtoWrapper):
            self._ProtoWrapper__frozen = False
            current_child_uuids = self.child_uuids
            current_child_uuids.append(child.uuid)
            self.child_uuids = current_child_uuids
            self._ProtoWrapper__frozen = True
        else:
            self.child_uuids.append(child.uuid)


class Passage:
    """Abstract class for a passage of a document.

    A passage is a part of a document that contains text or code. This class is used
    for type hinting and instance checking."""

    uuid: str
    parent_uuid: str


Chunk = Union[Section, Passage]


class Code(ProtoWrapper, Section):
    proto_type = CodeProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid


class CodeBlock(ProtoWrapper, Passage):
    proto_type = CodeBlockProto

    uuid: str
    parent_uuid: str
    content: str

    def __init__(
        self,
        parent_uuid: Optional[str] = None,
        content: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid
        self.content = content


class ListSection(ProtoWrapper, Section):
    proto_type = ListProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid


class Markdown(ProtoWrapper, Section):
    proto_type = MarkdownProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid


class MarkdownSection(ProtoWrapper, Section):
    proto_type = MarkdownSectionProto

    uuid: str
    parent_uuid: str
    header: str
    child_uuids: List[str]

    def __init__(
        self,
        header: Optional[str] = None,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid
        self.header = header


class PythonCode(ProtoWrapper, Section):
    proto_type = PythonCodeProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid


class PythonFunction(ProtoWrapper, Section):
    proto_type = PythonFunctionProto

    uuid: str
    parent_uuid: str
    function_definition: str
    child_uuids: List[str]

    def __init__(
        self,
        function_definition: Optional[str] = None,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid
        self.function_definition = function_definition


class PythonClass(ProtoWrapper, Section):
    proto_type = PythonClassProto

    uuid: str
    parent_uuid: str
    class_definition: str
    child_uuids: List[str]

    def __init__(
        self,
        class_definition: Optional[str] = None,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid
        self.class_definition = class_definition


class PythonCodePassage(ProtoWrapper, Passage):
    proto_type = PythonCodePassageProto

    uuid: str
    parent_uuid: str
    content: str

    def __init__(
        self,
        content: Optional[str] = None,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid
        self.content = content


class Text(ProtoWrapper, Section):
    proto_type = TextProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid


class Paragraph(ProtoWrapper, Section):
    proto_type = ParagraphProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        child_uuids: Optional[List[str]] = None,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids


class TextPassage(ProtoWrapper, Passage):
    proto_type = TextPassageProto

    uuid: str
    parent_uuid: str
    content: str

    def __init__(
        self,
        content: Optional[str] = None,
        parent_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.parent_uuid = parent_uuid
        self.content = content


class ChunkOneOf(ProtoWrapper):
    proto_type = ChunkProto

    chunk: Union[
        Code,
        CodeBlock,
        ListSection,
        Markdown,
        MarkdownSection,
        PythonCode,
        PythonFunction,
        PythonClass,
        PythonCodePassage,
        Text,
        Paragraph,
        TextPassage,
        DocumentRoot,
    ]

    def __init__(
        self,
        chunk: Optional[
            Union[
                Code,
                CodeBlock,
                ListSection,
                Markdown,
                MarkdownSection,
                PythonCode,
                PythonFunction,
                PythonClass,
                PythonCodePassage,
                Text,
                Paragraph,
                TextPassage,
                DocumentRoot,
            ]
        ] = None,
    ) -> None:
        super().__init__()
        self.chunk = chunk


if __name__ == "__main__":
    python_code = PythonCode(parent_uuid="parent_uuid")
    python_function = PythonCodePassage(
        content="def function():\n    pass", parent_uuid=python_code.uuid
    )
    python_code.add_child(python_function)
    print(python_code)
