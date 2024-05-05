from typing import Dict, List, Sequence, Union, Optional, Self

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
)
from powergrader_event_utils.events.proto_events.rag_pb2 import (
    DocumentSource,
    FileType as FileTypeProto,
    ScopeType as ScopeTypeProto,
    Document,
    ContentType as ContentTypeProto,
    RAGDivisionStarted,
    RAGDivision as RAGDivisionProto,
    DividedDocument,
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
    DocumentSummarizationStarted,
    DivisionSummary as DivisionSummaryProto,
    SummarizedDocument,
    DocumentEmbeddingStarted,
    Embedding as EmbeddingProto,
    PassageEmbedding as PassageEmbeddingProto,
    EmbeddedDocument,
    RegisterAssignmentInstruction,
    RegisterCriterionInstruction,
    AssignmentInstruction,
    CriterionInstruction,
    InvalidateInstruction,
    FlowNode as FlowNodeProto,
    FlowLog,
)

from powergrader_event_utils.events.proto import ProtoWrapper, ProtoEnumWrapper


class ScopeType(ProtoEnumWrapper):
    proto_type = ScopeTypeProto

    UNKNOWN_SCOPE = 0
    ASSIGNMENT_SCOPE = 1
    COURSE_SCOPE = 2
    ORG_SCOPE = 3
    ALL_SCOPE = 4


class FileType(ProtoEnumWrapper):
    proto_type = FileTypeProto

    UNKNOWN_FILE_TYPE = 0
    MARKDOWN = 1
    TEXT = 2
    PYTHON = 3


class DocumentStoreEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = DocumentSource

    public_uuid: str
    version_uuid: str
    name: str
    scope_uuid: str
    scope_type: ScopeType
    version_timestamp: int

    def __init__(
        self,
        name: Optional[str] = None,
        scope_uuid: Optional[str] = None,
        scope_type: Optional[ScopeType] = None,
        public_uuid: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)

        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp

        self.name = name
        self.scope_uuid = scope_uuid
        self.scope_type = scope_type


class DocumentEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = Document

    public_uuid: str
    version_uuid: str
    source_public_uuid: str
    name: str
    file_type: FileType
    content: str
    version_timestamp: int

    def __init__(
        self,
        source_public_uuid: Optional[str] = None,
        name: Optional[str] = None,
        file_type: Optional[FileType] = None,
        content: Optional[str] = None,
        public_uuid: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)

        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp

        self.name = name
        self.file_type = file_type
        self.content = content
        self.source_public_uuid = source_public_uuid


class ContentType(ProtoEnumWrapper):
    proto_type = ContentTypeProto

    UNKOWN_CONTENT = 0
    DOCUMENT = 1
    ASSIGNMENT = 2
    SUBMISSION = 3


class RAGDivisionStartedEvent(ProtoPowerGraderEvent):
    key_field_name: str = "uuid"
    proto_type = RAGDivisionStarted

    uuid: str
    document_version_uuid: str
    rag_method_info: str
    content_type: ContentType
    start_timestamp: int

    def __init__(
        self,
        document_version_uuid: Optional[str] = None,
        rag_method_info: Optional[str] = None,
        content_type: Optional[ContentType] = None,
        start_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.document_version_uuid = document_version_uuid
        self.rag_method_info = rag_method_info
        self.content_type = content_type

        if start_timestamp is None:
            start_timestamp = generate_event_timestamp()
        self.start_timestamp = start_timestamp


# Wrapper Classes for the different types of Document Divisions
# Section and Passage are abstract classes that are not directly used
class Section:
    def __init__(self):
        pass


class Passage:
    def __init__(self) -> None:
        pass


class Code(ProtoWrapper, Section):
    proto_type = CodeProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids


class CodeBlock(ProtoWrapper, Passage):
    proto_type = CodeBlockProto

    uuid: str
    parent_uuid: str
    content: str

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        content: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.content = content


class ListDivision(ProtoWrapper, Section):
    proto_type = ListProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids


class Markdown(ProtoWrapper, Section):
    proto_type = MarkdownProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids


class MarkdownSection(ProtoWrapper, Section):
    proto_type = MarkdownSectionProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]
    header: str

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
        header: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids
        self.header = header


class PythonCode(ProtoWrapper, Section):
    proto_type = PythonCodeProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids


class PythonFunction(ProtoWrapper, Section):
    proto_type = PythonFunctionProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]
    function_definition: str

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
        function_definition: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids
        self.function_definition = function_definition


class PythonClass(ProtoWrapper, Section):
    proto_type = PythonClassProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]
    class_definition: str

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
        class_definition: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids
        self.class_definition = class_definition


class PythonCodePassage(ProtoWrapper, Passage):
    proto_type = PythonCodePassageProto

    uuid: str
    parent_uuid: str
    content: str

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        content: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.content = content


class Text(ProtoWrapper, Section):
    proto_type = TextProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids


class Paragraph(ProtoWrapper, Section):
    proto_type = ParagraphProto

    uuid: str
    parent_uuid: str
    child_uuids: List[str]

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_uuids: Optional[List[str]] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_uuids = child_uuids


class TextPassage(ProtoWrapper, Passage):
    proto_type = TextPassageProto

    uuid: str
    parent_uuid: str
    content: str

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        content: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.content = content


class RAGDivision(ProtoWrapper):
    proto_type = RAGDivisionProto

    division: Union[
        Code,
        CodeBlock,
        ListDivision,
        Markdown,
        MarkdownSection,
        PythonCode,
        PythonFunction,
        PythonClass,
        PythonCodePassage,
        Text,
        Paragraph,
        TextPassage,
    ]

    def __init__(
        self,
        division: Optional[
            Union[
                Code,
                CodeBlock,
                ListDivision,
                Markdown,
                MarkdownSection,
                PythonCode,
                PythonFunction,
                PythonClass,
                PythonCodePassage,
                Text,
                Paragraph,
                TextPassage,
            ]
        ] = None,
    ) -> None:
        super().__init__()
        self.division = division


class DividedDocumentEvent(ProtoPowerGraderEvent):
    key_field_name: str = "rag_division_started_uuid"
    proto_type = DividedDocument

    rag_division_started_uuid: str
    divisions: List[RAGDivision]
    end_timestamp: int

    def __init__(
        self,
        rag_division_started_uuid: Optional[str] = None,
        divisions: Optional[List[RAGDivision]] = None,
        end_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.rag_division_started_uuid = rag_division_started_uuid
        self.divisions = divisions

        if end_timestamp is None:
            end_timestamp = generate_event_timestamp()
        self.end_timestamp = end_timestamp


# Summarization and Embedding Events
class DocumentSummarizationStartedEvent(ProtoPowerGraderEvent):
    key_field_name: str = "divided_document_uuid"
    proto_type = DocumentSummarizationStarted

    uuid: str
    divided_document_uuid: str
    summarization_method_info: str
    start_timestamp: int

    def __init__(
        self,
        divided_document_uuid: Optional[str] = None,
        summarization_method_info: Optional[str] = None,
        start_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.divided_document_uuid = divided_document_uuid
        self.summarization_method_info = summarization_method_info

        if start_timestamp is None:
            start_timestamp = generate_event_timestamp()
        self.start_timestamp = start_timestamp


class DivisionSummary(ProtoWrapper):
    proto_type = DivisionSummaryProto

    division_uuid: str
    version_uuid: str
    summary: str

    def __init__(
        self,
        division_uuid: Optional[str] = None,
        version_uuid: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.division_uuid = division_uuid
        self.version_uuid = version_uuid
        self.summary = summary


class SummarizedDocumentEvent(ProtoPowerGraderEvent):
    key_field_name: str = "document_summarization_started_uuid"
    proto_type = SummarizedDocument

    document_summarization_started_uuid: str
    summaries: List[DivisionSummary]
    end_timestamp: int

    def __init__(
        self,
        document_summarization_started_uuid: Optional[str] = None,
        summaries: Optional[List[DivisionSummary]] = None,
        end_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.document_summarization_started_uuid = document_summarization_started_uuid
        self.summaries = summaries

        if end_timestamp is None:
            end_timestamp = generate_event_timestamp()
        self.end_timestamp = end_timestamp


class DocumentEmbeddingStartedEvent(ProtoPowerGraderEvent):
    key_field_name: str = "divided_document_uuid"
    proto_type = DocumentEmbeddingStarted

    uuid: str
    divided_document_uuid: str
    embedding_method_info: str
    start_timestamp: int

    def __init__(
        self,
        divided_document_uuid: Optional[str] = None,
        embedding_method_info: Optional[str] = None,
        start_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.divided_document_uuid = divided_document_uuid
        self.embedding_method_info = embedding_method_info

        if start_timestamp is None:
            start_timestamp = generate_event_timestamp()
        self.start_timestamp = start_timestamp


class Embedding(ProtoWrapper):
    proto_type = EmbeddingProto

    embedding: List[float]

    def __init__(
        self,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super().__init__()
        self.embedding = embedding


class PassageEmbedding(ProtoWrapper):
    proto_type = PassageEmbeddingProto

    passage_uuid: str
    embeddings: List[Embedding]

    def __init__(
        self,
        passage_uuid: Optional[str] = None,
        embedding: Optional[List[Embedding]] = None,
    ) -> None:
        super().__init__()
        self.passage_uuid = passage_uuid
        self.embedding = embedding


class EmbeddedDocumentEvent(ProtoPowerGraderEvent):
    key_field_name: str = "document_embedding_started_uuid"
    proto_type = EmbeddedDocument

    document_embedding_started_uuid: str
    embeddings: List[PassageEmbedding]
    end_timestamp: int

    def __init__(
        self,
        document_embedding_started_uuid: Optional[str] = None,
        embeddings: Optional[List[PassageEmbedding]] = None,
        end_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.document_embedding_started_uuid = document_embedding_started_uuid
        self.embeddings = embeddings

        if end_timestamp is None:
            end_timestamp = generate_event_timestamp()
        self.end_timestamp = end_timestamp


# Instruction Events
class RegisterAssignmentInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterAssignmentInstruction

    public_uuid: str
    course_public_uuid: str
    assignment_version_uuid: str

    def __init__(
        self,
        course_public_uuid: Optional[str] = None,
        assignment_version_uuid: Optional[str] = None,
        public_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid

        self.course_public_uuid = course_public_uuid
        self.assignment_version_uuid = assignment_version_uuid


class RegisterCriterionInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterCriterionInstruction

    public_uuid: str
    course_public_uuid: str
    assignment_version_uuid: str
    criterion_uuid: str

    def __init__(
        self,
        course_public_uuid: Optional[str] = None,
        assignment_version_uuid: Optional[str] = None,
        criterion_uuid: Optional[str] = None,
        public_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid

        self.course_public_uuid = course_public_uuid
        self.assignment_version_uuid = assignment_version_uuid
        self.criterion_uuid = criterion_uuid


class AssignmentInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = AssignmentInstruction

    public_uuid: str
    version_uuid: str
    content: str
    version_timestamp: int

    def __init__(
        self,
        content: Optional[str] = None,
        public_uuid: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)

        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
        self.content = content


class CriterionInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = CriterionInstruction

    public_uuid: str
    version_uuid: str
    content: str
    version_timestamp: int

    def __init__(
        self,
        content: Optional[str] = None,
        public_uuid: Optional[str] = None,
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        if public_uuid is None:
            public_uuid = generate_event_uuid(self.__class__.__name__)
        self.public_uuid = public_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)

        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
        self.content = content


class InvalidateInstructionEvent(ProtoPowerGraderEvent):
    key_field_name: str = "instruction_version_uuid"
    proto_type = InvalidateInstruction

    instruction_version_uuid: str
    is_assignment_instruction: bool

    def __init__(
        self,
        is_assignment_instruction: Optional[bool] = None,
        instruction_version_uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.instruction_version_uuid = instruction_version_uuid
        self.is_assignment_instruction = is_assignment_instruction


class FlowNode(ProtoWrapper):
    proto_type = FlowNodeProto

    uuid: str
    parent_uuid: str
    child_nodes: List[Self]

    def __init__(
        self,
        uuid: Optional[str] = None,
        parent_uuid: Optional[str] = None,
        child_nodes: Optional[List[Self]] = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.parent_uuid = parent_uuid
        self.child_nodes = child_nodes


class FlowLogEvent(ProtoPowerGraderEvent):
    key_field_name: str = "uuid"
    proto_type = FlowLog

    uuid: str
    name: str
    ai_grading_started_uuid: str
    root_node: FlowNode

    def __init__(
        self,
        name: Optional[str] = None,
        ai_grading_started_uuid: Optional[str] = None,
        root_node: Optional[FlowNode] = None,
        uuid: Optional[str] = None,
    ) -> None:
        super().__init__()

        if uuid is None:
            uuid = generate_event_uuid(self.__class__.__name__)
        self.uuid = uuid
        self.name = name
        self.ai_grading_started_uuid = ai_grading_started_uuid
        self.root_node = root_node
