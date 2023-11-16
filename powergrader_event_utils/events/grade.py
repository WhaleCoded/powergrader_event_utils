from typing import Dict, List
from enum import Enum
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
    EventType,
)
from powergrader_event_utils.events.proto_events.grade_pb2 import (
    CriteriaEmbedding,
    AssesmentSimilarity,
    CriteriaGrade,
    GradeIdentifier,
    GradeType as ProtoGradeType,
    StudentRequestedRegrade,
    GradingStarted,
    InstructorReview,
)
from google.protobuf.json_format import MessageToJson


class GradeType(Enum):
    AI_GRADED = 0
    FACULTY_ADJUSTED = 1
    AI_INFERRED = 2


@dataclass
class GradeIdentifiers:
    submission_id: str
    assignment_id: str
    grade_method_id: str


class CriteriaGradeEvent(PowerGraderEvent):
    def __init__(
        self,
        grade_identifier: GradeIdentifiers or str,
        rubric_criteria_id: str,
        grade_type: GradeType,
        score: int,
        assessment: str,
    ) -> None:
        """
        grade_identifier: GradeIdentifiers or str. grade_identifiers can be the id of a GradingStartedEvent or a GradeIdentifiers object.
        This allows us to not duplicate information and still allow for faculty and AI to use this event.
        """
        if assessment is None:
            assessment = ""

        if (
            not grade_identifier
            or not rubric_criteria_id
            or not grade_type
            or not score
        ):
            raise ValueError(
                "Grade identifier, rubric criteria ID, grade type, and score must be specified."
            )

        self.proto = CriteriaGrade()
        self.proto.rubric_criteria_id = rubric_criteria_id
        self.proto.type = grade_type.value
        self.proto.score = score
        self.proto.assesment = assessment

        if isinstance(grade_identifier, str):
            self.proto.grading_started_id = grade_identifier
        else:
            grade_identifier_proto = GradeIdentifier()
            grade_identifier_proto.submission_id = grade_identifier.submission_id
            grade_identifier_proto.assignment_id = grade_identifier.assignment_id
            grade_identifier_proto.grade_method_id = grade_identifier.grade_method_id

            self.proto.grade_identifier.CopyFrom(grade_identifier_proto)

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.CRITERIA_GRADE

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_grade_identifier(self) -> GradeIdentifiers or str:
        grade_identifier = getattr(self.proto, self.proto.WhichOneof("grade_id"))
        if isinstance(grade_identifier, str):
            return grade_identifier

        return GradeIdentifiers(
            grade_identifier.submission_id,
            grade_identifier.assignment_id,
            grade_identifier.grade_method_id,
        )

    def get_rubric_criteria_id(self) -> str or None:
        rubric_criteria_id = self.proto.rubric_criteria_id
        return rubric_criteria_id if rubric_criteria_id != "" else None

    def get_grade_type(self) -> GradeType:
        return GradeType(self.proto.type)

    def get_score(self) -> float:
        return self.proto.score

    def get_assessment(self) -> str or None:
        assessment = self.proto.assesment
        return assessment if assessment != "" else None

    def validate(self) -> bool:
        return bool(
            self.get_id()
            and self.get_grade_identifier()
            and self.get_rubric_criteria_id()
            and self.get_grade_type()
            and self.get_score() >= 0.0
        )

    def _package_into_proto(self) -> CriteriaGrade:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "CriteriaGradeEvent":
        criteria_grade = CriteriaGrade()
        criteria_grade.ParseFromString(event)

        new_criteria_grade_instance = cls.__new__(cls)
        new_criteria_grade_instance.proto = criteria_grade
        super(cls, new_criteria_grade_instance).__init__(
            key=criteria_grade.id,
            event_type=new_criteria_grade_instance.__class__.__name__,
        )

        if new_criteria_grade_instance.validate():
            return new_criteria_grade_instance

        return False


class CriteriaEmbeddingEvent(PowerGraderEvent):
    def __init__(
        self, crit_grade_id: str, embedder_id: str, embedding: List[float]
    ) -> None:
        self.proto = CriteriaEmbedding()
        self.proto.crit_grade_id = crit_grade_id
        self.proto.embedder_id = embedder_id
        self.proto.embedding.extend(embedding)

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.CRITERIA_EMBEDDING

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_crit_grade_id(self) -> str or None:
        crit_grade_id = self.proto.crit_grade_id
        return crit_grade_id if crit_grade_id != "" else None

    def get_embedder_id(self) -> str or None:
        embedder_id = self.proto.embedder_id
        return embedder_id if embedder_id != "" else None

    def get_embedding(self) -> List[float] or None:
        embedding = list(self.proto.embedding)
        return embedding if embedding else None

    def validate(self) -> bool:
        return bool(
            self.get_id()
            and self.get_crit_grade_id()
            and self.get_embedding()
            and self.get_embedder_id()
            and len(self.get_embedding()) > 0
            and all([isinstance(x, float) for x in self.get_embedding()])
        )

    def _package_into_proto(self) -> CriteriaEmbedding:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "CriteriaEmbeddingEvent":
        criteria_embedding = CriteriaEmbedding()
        criteria_embedding.ParseFromString(event)

        new_criteria_embedding_instance = cls.__new__(cls)
        new_criteria_embedding_instance.proto = criteria_embedding
        super(cls, new_criteria_embedding_instance).__init__(
            key=criteria_embedding.id,
            event_type=new_criteria_embedding_instance.__class__.__name__,
        )

        if new_criteria_embedding_instance.validate():
            return new_criteria_embedding_instance

        return False


class AssesmentSimilarityEvent(PowerGraderEvent):
    def __init__(self, simmilar_criteria_grade_ids: List[str]) -> None:
        self.proto = AssesmentSimilarity()
        self.proto.simmilar_criteria_grade_ids.extend(simmilar_criteria_grade_ids)

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSESMENT_SIMILARITY

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_simmilar_criteria_grade_ids(self) -> List[str] or None:
        simmilar_criteria_grade_ids = list(self.proto.simmilar_criteria_grade_ids)
        return simmilar_criteria_grade_ids if simmilar_criteria_grade_ids else None

    def validate(self) -> bool:
        return bool(
            self.get_id()
            and self.get_simmilar_criteria_grade_ids()
            and len(self.get_simmilar_criteria_grade_ids()) > 0
            and all(
                [isinstance(x, str) for x in self.get_simmilar_criteria_grade_ids()]
            )
        )

    def _package_into_proto(self) -> AssesmentSimilarity:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssesmentSimilarityEvent":
        assesment_similarity = AssesmentSimilarity()
        assesment_similarity.ParseFromString(event)

        new_assesment_similarity_instance = cls.__new__(cls)
        new_assesment_similarity_instance.proto = assesment_similarity
        super(cls, new_assesment_similarity_instance).__init__(
            key=assesment_similarity.id,
            event_type=new_assesment_similarity_instance.__class__.__name__,
        )

        if new_assesment_similarity_instance.validate():
            return new_assesment_similarity_instance

        return False


class StudentRequestedRegradeEvent(PowerGraderEvent):
    def __init__(
        self,
        student_id: str,
        submission_id: str,
        reasoning: str,
        criteria_grades: List[str],
    ) -> None:
        if not student_id or not submission_id:
            raise ValueError(
                "Student ID, submission ID, and reasoning must be specified."
            )
        if len(criteria_grades) == 0:
            raise ValueError("At least one criterion must be specified.")

        self.proto = StudentRequestedRegrade()
        self.proto.student_id = student_id
        self.proto.submission_id = submission_id
        self.proto.reasoning = reasoning
        self.proto.criteria_grades_to_reevaluate.extend(criteria_grades)

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_REQUESTED_REGRADE

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_student_id(self) -> str or None:
        student_id = self.proto.student_id
        return student_id if student_id != "" else None

    def get_submission_id(self) -> str or None:
        submission_id = self.proto.submission_id
        return submission_id if submission_id != "" else None

    def get_reasoning(self) -> str or None:
        reasoning = self.proto.reasoning
        return reasoning if reasoning != "" else None

    def get_criteria_grades_to_reevaluate(self) -> List[str]:
        return list(self.proto.criteria_grades_to_reevaluate)

    def validate(self) -> bool:
        return bool(
            self.get_id()
            and self.get_student_id()
            and self.get_submission_id()
            and len(self.get_criteria_grades_to_reevaluate()) > 0
            and all(
                [isinstance(x, str) for x in self.get_criteria_grades_to_reevaluate()]
            )
        )

    def _package_into_proto(self) -> StudentRequestedRegrade:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentRequestedRegradeEvent":
        regrade_request = StudentRequestedRegrade()
        regrade_request.ParseFromString(event)

        new_regrade_request_instance = cls.__new__(cls)
        new_regrade_request_instance.proto = regrade_request
        super(cls, new_regrade_request_instance).__init__(
            key=regrade_request.id,
            event_type=new_regrade_request_instance.__class__.__name__,
        )

        if new_regrade_request_instance.validate():
            return new_regrade_request_instance

        return False


class GradingStartedEvent(PowerGraderEvent):
    def __init__(
        self,
        submission_id: str,
        assignment_id: str,
        grade_method_id: str,
        criteria_to_be_graded: List[str],
    ) -> None:
        if not submission_id or not assignment_id or not grade_method_id:
            raise ValueError(
                "Submission ID, assignment ID, and grade method ID must be specified."
            )

        self.proto = GradingStarted()
        self.proto.id = generate_event_id(self.__class__.__name__)
        self.proto.submission_id = submission_id
        self.proto.assignment_id = assignment_id
        self.proto.grade_method_id = grade_method_id

        if len(criteria_to_be_graded) == 0:
            raise ValueError("At least one criterion must be specified.")
        for criterion in criteria_to_be_graded:
            if criterion:
                self.proto.criteria_to_be_graded.append(criterion)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.GRADING_STARTED

    def get_id(self) -> str:
        return self.proto.id

    def get_submission_id(self) -> str:
        return self.proto.submission_id

    def get_assignment_id(self) -> str:
        return self.proto.assignment_id

    def get_grade_method_id(self) -> str:
        return self.proto.grade_method_id

    def get_criteria_to_be_graded(self) -> list:
        # This method returns a list of criteria to be graded.
        return list(self.proto.criteria_to_be_graded)

    def validate(self) -> bool:
        # Validate that all identifiers and at least one grading criterion are present.
        return bool(
            self.get_id()
            and self.get_submission_id()
            and self.get_assignment_id()
            and self.get_grade_method_id()
            and len(self.get_criteria_to_be_graded()) > 0
        )

    def _package_into_proto(self) -> GradingStarted:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "GradingStartedEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = GradingStarted()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_gradeing_started = cls.__new__(cls)
        new_gradeing_started.proto = data
        super(cls, new_gradeing_started).__init__(
            key=data.id,
            event_type=new_gradeing_started.__class__.__name__,
        )

        if new_gradeing_started.validate():
            return new_gradeing_started

        return False


class InstructorReviewEvent(PowerGraderEvent):
    def __init__(
        self,
        submission_id: str,
        assignment_id: str,
        instructor_id: str,
        criteria_grade_ids: List[str],
    ) -> None:
        if not submission_id or not assignment_id or not instructor_id:
            raise ValueError(
                "Submission ID, assignment ID, and instructor ID must be specified."
            )

        if len(criteria_grade_ids) == 0:
            raise ValueError("At least one criteria grade ID must be specified.")

        self.proto = InstructorReview()
        self.proto.id = generate_event_id(self.__class__.__name__)
        self.proto.submission_id = submission_id
        self.proto.assignment_id = assignment_id
        self.proto.instructor_id = instructor_id
        for criteria_grade_id in criteria_grade_ids:
            self.proto.criteria_grade_ids.append(criteria_grade_id)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_REVIEW

    def get_id(self) -> str:
        return self.proto.id

    def get_submission_id(self) -> str or None:
        return self.proto.submission_id if self.proto.submission_id != "" else None

    def get_assignment_id(self) -> str or None:
        return self.proto.assignment_id if self.proto.assignment_id != "" else None

    def get_instructor_id(self) -> str or None:
        return self.proto.instructor_id if self.proto.instructor_id != "" else None

    def get_criteria_grade_ids(self) -> list:
        # This method returns a list of criteria grade IDs.
        return self.proto.criteria_grade_ids

    def validate(self) -> bool:
        # Validate that all identifiers and at least one criteria grade ID are present.
        return bool(
            self.get_id()
            and self.get_submission_id()
            and self.get_assignment_id()
            and self.get_instructor_id()
            and len(self.get_criteria_grade_ids()) > 0
        )

    def _package_into_proto(self) -> InstructorReview:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorReviewEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = InstructorReview()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_instructor_review = cls.__new__(cls)
        new_instructor_review.proto = data
        super(cls, new_instructor_review).__init__(
            key=data.id,
            event_type=new_instructor_review.__class__.__name__,
        )

        if new_instructor_review.validate():
            return new_instructor_review

        return False
