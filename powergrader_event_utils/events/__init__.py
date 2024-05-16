from typing import Type
from datetime import datetime
import time

from powergrader_event_utils.events.event import (
    PowerGraderEvent,
    EventType,
    get_event_type_from_uuid,
    get_kafka_topic_name_for_event_type,
    get_kafka_topic_names_for_event_types,
    get_event_type_from_uuid,
    deserialize_powergrader_event,
)

from powergrader_event_utils.events.assignment import (
    AssignmentEvent,
    CriterionLevel,
    RubricCriterion,
    RubricEvent,
)
from powergrader_event_utils.events.course import (
    CourseEvent,
    SectionEvent,
    OrganizationEvent,
)
from powergrader_event_utils.events.flow import (
    FlowLogEvent,
    FlowNode,
)
from powergrader_event_utils.events.grade import (
    AICriterionGradeEvent,
    AICriterionGradingStartedEvent,
    Grade,
    GradingMethodEvent,
    AIInferredCriterionGradeEvent,
    InstructorCriterionGradeEvent,
    InstructorOverrideCriterionGradeEvent,
    CriterionGradeEmbeddingEvent,
    InstructorSubmissionGradeApprovalEvent,
)
from powergrader_event_utils.events.instructions import (
    InstructionInfo,
    RegisterAssignmentInstructionEvent,
    RegisterCriterionInstructionEvent,
    AssignmentInstructionEvent,
    CriterionInstructionEvent,
    InvalidateInstructionEvent,
)
from powergrader_event_utils.events.publish import (
    RegisterCoursePublicUUIDEvent,
    RegisterSectionPublicUUIDEvent,
    LMSInstructorType,
    RegisterInstructorPublicUUIDEvent,
    RegisterStudentPublicUUIDEvent,
    RegisterAssignmentPublicUUIDEvent,
    RegisterRubricPublicUUIDEvent,
    RegisterSubmissionPublicUUIDEvent,
    PublishedToLMSEvent,
    PublishedGradeToLMSEvent,
)
from powergrader_event_utils.events.rag_chunks import (
    DocumentRoot,
    Section,
    Passage,
    Chunk,
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
    ChunkOneOf,
)
from powergrader_event_utils.events.rag import (
    ScopeType,
    FileType,
    DocumentSourceEvent,
    SupportingDocumentEvent,
    DocumentType,
    DocumentChunkingStartedEvent,
    DocumentChunksEvent,
    DocumentChunkSummarizationStartedEvent,
    ChunkSummary,
    DocumentChunkSummariesEvent,
    DocumentPassageEmbeddingStartedEvent,
    Embedding,
    PassageEmbedding,
    DocumentPassageEmbeddingsEvent,
)
from powergrader_event_utils.events.relationship import (
    AssignmentAddedToCourseEvent,
    AssignmentRemovedFromCourseEvent,
    StudentAddedToSectionEvent,
    StudentRemovedFromSectionEvent,
    InstructorAddedToCourseEvent,
    InstructorRemovedFromCourseEvent,
)
from powergrader_event_utils.events.retry import (
    RetryEvent,
    DeadLetterEvent,
)
from powergrader_event_utils.events.submission import (
    FileContent,
    SubmissionFileGroupEvent,
    SubmissionEvent,
)
from powergrader_event_utils.events.user import (
    StudentEvent,
    InstructorEvent,
)

EMBEDDING_SIZE = 3072


def convert_event_type_to_event_class_type(
    event_type: EventType,
) -> Type[PowerGraderEvent]:
    class_name = event_type.value

    if event_type == EventType.NOT_SPECIFIED:
        return None

    return globals()[class_name]


def convert_proto_when_to_date_time(when: int) -> datetime:
    return datetime.fromtimestamp(when / 1000.0)


def get_miliseconds_since_epoch():
    return int(time.time_ns() / 1_000_000)
