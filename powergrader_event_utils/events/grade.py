from typing import Dict, List
from enum import Enum
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.grade_pb2 import (
    CriteriaGradeEmbedding,
    AssessmentSimilarity,
    CriteriaGrade,
    GradeIdentifier as GradeIdentifierProto,
    GradeType as ProtoGradeType,
    StudentRequestedRegrade,
    GradingStarted,
    InstructorReview,
)
from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


class GradingStartedEvent(PowerGraderEvent, ProtoWrapper[GradingStarted]):
    id: str
    submission_id: str
    grade_method_id: str
    criteria_to_be_graded: List[str]

    def __init__(
        self,
        submission_id: str,
        grade_method_id: str,
        criteria_to_be_graded: List[str],
    ) -> None:
        proto = GradingStarted()

        if submission_id is not None:
            proto.submission_id = submission_id

        if grade_method_id is not None:
            proto.grade_method_id = grade_method_id

        if criteria_to_be_graded:
            proto.criteria_to_be_graded.extend(criteria_to_be_graded)

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, GradingStarted, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> GradingStarted:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.GRADING_STARTED

    @classmethod
    def deserialize(cls, event: bytes) -> "GradingStartedEvent":
        return general_deserialization(GradingStarted, cls, event, "id")


class GradeType(Enum):
    UNSPECIFIED = 0
    AI_GRADED = 1
    FACULTY_ADJUSTED = 2
    AI_INFERRED = 3


@dataclass
class GradeIdentifier:
    submission_id: str
    grade_method_id: str
    previous_criteria_grade_id: str = None


class CriteriaGradeEvent(PowerGraderEvent, ProtoWrapper[CriteriaGrade]):
    id: str
    grade_id: str or ProtoWrapper[
        GradeIdentifierProto
    ]  # Assuming GradeIdentifier is a protobuf message or similar
    rubric_criteria_id: str
    type: GradeType  # Assuming GradeType is an enum or similar type
    score: int
    assessment: str

    def __init__(
        self,
        grade_id: str or GradeIdentifier,
        rubric_criteria_id: str,
        type: GradeType,
        score: int,
        assessment: str,
    ) -> None:
        proto = CriteriaGrade()

        if isinstance(grade_id, str):
            proto.grading_started_id = grade_id
        elif isinstance(grade_id, GradeIdentifier):
            grade_identifier_proto = GradeIdentifierProto()
            grade_identifier_proto.submission_id = grade_id.submission_id
            grade_identifier_proto.grade_method_id = grade_id.grade_method_id

            if grade_id.previous_criteria_grade_id is not None:
                grade_identifier_proto.previous_criteria_grade_id = (
                    grade_id.previous_criteria_grade_id
                )

            proto.grade_identifier.CopyFrom(grade_identifier_proto)

        if rubric_criteria_id is not None:
            proto.rubric_criteria_id = rubric_criteria_id

        if type is not None:
            proto.type = type.value

        if score is not None:
            proto.score = score

        if assessment is not None:
            proto.assessment = assessment

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, CriteriaGrade, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> CriteriaGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.CRITERIA_GRADE

    @classmethod
    def deserialize(cls, event: bytes) -> "CriteriaGradeEvent":
        return general_deserialization(CriteriaGrade, cls, event, "id")


class CriteriaGradeEmbeddingEvent(
    PowerGraderEvent, ProtoWrapper[CriteriaGradeEmbedding]
):
    id: str
    crit_grade_id: str
    embedder_id: str
    embedding: List[float]

    def __init__(
        self, crit_grade_id: str, embedder_id: str, embedding: List[float]
    ) -> None:
        proto = CriteriaGradeEmbedding()

        if crit_grade_id is not None:
            proto.crit_grade_id = crit_grade_id

        if embedder_id is not None:
            proto.embedder_id = embedder_id

        if embedding:
            proto.embedding.extend(embedding)

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, CriteriaGradeEmbedding, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> CriteriaGradeEmbedding:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.CRITERIA_GRADE_EMBEDDING

    @classmethod
    def deserialize(cls, event: bytes) -> "CriteriaGradeEmbeddingEvent":
        return general_deserialization(CriteriaGradeEmbedding, cls, event, "id")


class AssessmentSimilarityEvent(PowerGraderEvent, ProtoWrapper[AssessmentSimilarity]):
    id: str
    similar_criteria_grade_ids: List[str]

    def __init__(self, similar_criteria_grade_ids: List[str]) -> None:
        proto = AssessmentSimilarity()

        if similar_criteria_grade_ids:
            proto.similar_criteria_grade_ids.extend(similar_criteria_grade_ids)

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, AssessmentSimilarity, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> AssessmentSimilarity:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSESSMENT_SIMILARITY

    @classmethod
    def deserialize(cls, event: bytes) -> "AssessmentSimilarityEvent":
        return general_deserialization(AssessmentSimilarity, cls, event, "id")


class StudentRequestedRegradeEvent(
    PowerGraderEvent, ProtoWrapper[StudentRequestedRegrade]
):
    id: str
    submission_id: str
    reasoning: str
    criteria_grades_to_reevaluate: List[str]

    def __init__(
        self,
        submission_id: str,
        reasoning: str,
        criteria_grades_to_reevaluate: List[str],
    ) -> None:
        proto = StudentRequestedRegrade()

        if submission_id is not None:
            proto.submission_id = submission_id

        if reasoning is not None:
            proto.reasoning = reasoning

        if criteria_grades_to_reevaluate:
            proto.criteria_grades_to_reevaluate.extend(criteria_grades_to_reevaluate)

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, StudentRequestedRegrade, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> StudentRequestedRegrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_REQUESTED_REGRADE

    @classmethod
    def deserialize(cls, event: bytes) -> "StudentRequestedRegradeEvent":
        return general_deserialization(StudentRequestedRegrade, cls, event, "id")


class InstructorReviewEvent(PowerGraderEvent, ProtoWrapper[InstructorReview]):
    id: str
    submission_id: str
    assignment_id: str
    instructor_id: str
    time_reviewed: int
    criteria_grade_ids: List[str]

    def __init__(
        self,
        submission_id: str,
        instructor_id: str,
        time_reviewed: int,
        criteria_grade_ids: List[str],
    ) -> None:
        proto = InstructorReview()

        if submission_id is not None:
            proto.submission_id = submission_id

        if instructor_id is not None:
            proto.instructor_id = instructor_id

        if criteria_grade_ids:
            proto.criteria_grade_ids.extend(criteria_grade_ids)

        if time_reviewed is not None:
            proto.time_reviewed = time_reviewed

        proto.id = generate_event_id(self.__class__.__name__)

        ProtoWrapper.__init__(self, InstructorReview, proto)
        PowerGraderEvent.__init__(
            self, key=proto.id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> InstructorReview:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_REVIEW

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorReviewEvent":
        return general_deserialization(InstructorReview, cls, event, "id")
