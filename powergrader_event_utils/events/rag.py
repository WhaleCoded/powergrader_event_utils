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
    SupportingDocument,
    ContentType as ContentTypeProto,
    RAGChunkingStarted,
    DocumentChunkSummarizationStarted,
    ChunkSummary as ChunkSummaryProto,
    DocumentChunkSummaries,
    DocumentPassageEmbeddingStarted,
    Embedding as EmbeddingProto,
    DocumentChunks,
    PassageEmbedding as PassageEmbeddingProto,
    DocumentPassageEmbeddings,
)
import powergrader_event_utils.events.rag_chunks as rag_chunks

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


class DocumentSourceEvent(ProtoPowerGraderEvent):
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


# TODO: Eventually, we need to have some way of specifying the scope of the document
# e.g. is this global, or specific to a course or assignment?
class SupportingDocumentEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = SupportingDocument

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


class RAGChunkingStartedEvent(ProtoPowerGraderEvent):
    key_field_name: str = "uuid"
    proto_type = RAGChunkingStarted

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


class DocumentChunksEvent(ProtoPowerGraderEvent):
    key_field_name: str = "rag_division_started_uuid"
    proto_type = DocumentChunks

    rag_chunking_started_uuid: str
    document_root: rag_chunks.DocumentRoot
    chunks: List[rag_chunks.Chunk]
    end_timestamp: int

    def __init__(
        self,
        rag_chunking_started_uuid: Optional[str] = None,
        chunks: Optional[List[rag_chunks.Chunk]] = None,
        end_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.rag_chunking_started_uuid = rag_chunking_started_uuid
        self.chunks = chunks

        if end_timestamp is None:
            end_timestamp = generate_event_timestamp()
        self.end_timestamp = end_timestamp


class DocumentChunkSummarizationStartedEvent(ProtoPowerGraderEvent):
    key_field_name: str = "divided_document_uuid"
    proto_type = DocumentChunkSummarizationStarted

    uuid: str
    document_chunks_uuid: str
    summarization_method_info: str
    start_timestamp: int

    def __init__(
        self,
        document_chunks_uuid: Optional[str] = None,
        summarization_method_info: Optional[str] = None,
        start_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.document_chunks_uuid = document_chunks_uuid
        self.summarization_method_info = summarization_method_info

        if start_timestamp is None:
            start_timestamp = generate_event_timestamp()
        self.start_timestamp = start_timestamp


class ChunkSummary(ProtoWrapper):
    proto_type = ChunkSummaryProto

    chunk_uuid: str
    version_uuid: str
    summary: str

    def __init__(
        self,
        division_uuid: Optional[str] = None,
        summary: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.division_uuid = division_uuid
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.summary = summary


class DocumentChunkSummariesEvent(ProtoPowerGraderEvent):
    key_field_name: str = "document_summarization_started_uuid"
    proto_type = DocumentChunkSummaries

    document_chunk_summarization_started_uuid: str
    summaries: List[ChunkSummary]
    end_timestamp: int

    def __init__(
        self,
        document_chunk_summarization_started_uuid: Optional[str] = None,
        summaries: Optional[List[ChunkSummary]] = None,
        end_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.document_chunk_summarization_started_uuid = (
            document_chunk_summarization_started_uuid
        )
        self.summaries = summaries

        if end_timestamp is None:
            end_timestamp = generate_event_timestamp()
        self.end_timestamp = end_timestamp


class DocumentPassageEmbeddingStartedEvent(ProtoPowerGraderEvent):
    key_field_name: str = "divided_document_uuid"
    proto_type = DocumentPassageEmbeddingStarted

    uuid: str
    document_chunks_uuid: str
    document_chunk_summaries_uuid: str
    embedding_method_info: str
    start_timestamp: int

    def __init__(
        self,
        document_chunks_uuid: Optional[str] = None,
        document_chunk_summaries_uuid: Optional[str] = None,
        embedding_method_info: Optional[str] = None,
        start_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.document_chunks_uuid = document_chunks_uuid
        self.document_chunk_summaries_uuid = document_chunk_summaries_uuid
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
        embeddings: Optional[List[Embedding]] = None,
    ) -> None:
        super().__init__()
        self.passage_uuid = passage_uuid
        self.embeddings = embeddings


class DocumentPassageEmbeddingsEvent(ProtoPowerGraderEvent):
    key_field_name: str = "document_passage_embedding_started_uuid"
    proto_type = DocumentPassageEmbeddings

    document_passage_embedding_started_uuid: str
    passage_embeddings: List[PassageEmbedding]
    end_timestamp: int

    def __init__(
        self,
        document_passage_embedding_started_uuid: Optional[str] = None,
        passage_embeddings: Optional[List[PassageEmbedding]] = None,
        end_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()

        self.document_passage_embedding_started_uuid = (
            document_passage_embedding_started_uuid
        )
        self.passage_embeddings = passage_embeddings

        if end_timestamp is None:
            end_timestamp = generate_event_timestamp()
        self.end_timestamp = end_timestamp


if __name__ == "__main__":
    example_embedding = Embedding(embedding=[1.0, 2.0, 3.0])
    document_embeddings = DocumentPassageEmbeddingsEvent(
        document_passage_embedding_started_uuid="123",
        passage_embeddings=[
            PassageEmbedding(passage_uuid="456", embeddings=[example_embedding])
        ],
    )
    print(document_embeddings)
    serialized = document_embeddings.serialize()
    print(serialized)
    print(DocumentPassageEmbeddingsEvent.deserialize(serialized))
