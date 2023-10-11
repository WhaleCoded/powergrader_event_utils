from typing import Dict, List

from powergrader_event_utils.events.base import PowerGraderEvent, generate_event_id
from powergrader_event_utils.events.proto_events.grade_pb2 import (
    CriteriaEmbedding,
    AssesmentSimilarity,
    CriteriaGrade,
    GradeType,
    StudentRequestedRegrade,
)
from google.protobuf.json_format import MessageToJson


class CriteriaGradeEvent(PowerGraderEvent):
    def __init__(
        self,
        submission_id: str,
        rubric_criteria_id: str,
        grade_type: GradeType,
        grade_method_id: str,
        score: float,
        assessment: str,
    ) -> None:
        if assessment is None:
            assessment = ""

        self.proto = CriteriaGrade()
        self.proto.submission_id = submission_id
        self.proto.rubric_criteria_id = rubric_criteria_id
        self.proto.type = grade_type
        self.proto.grade_method_id = grade_method_id
        self.proto.score = score
        self.proto.assesment = assessment

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_submission_id(self) -> str or None:
        submission_id = self.proto.submission_id
        return submission_id if submission_id != "" else None

    def get_rubric_criteria_id(self) -> str or None:
        rubric_criteria_id = self.proto.rubric_criteria_id
        return rubric_criteria_id if rubric_criteria_id != "" else None

    def get_grade_type(self) -> GradeType:
        return self.proto.type

    def get_grade_method_id(self) -> str or None:
        grade_method_id = self.proto.grade_method_id
        return grade_method_id if grade_method_id != "" else None

    def get_score(self) -> float:
        return self.proto.score

    def get_assessment(self) -> str or None:
        assessment = self.proto.assesment
        return assessment if assessment != "" else None

    def validate(self) -> bool:
        return all(
            [
                self.get_id() is not None,
                self.get_submission_id() is not None,
                self.get_rubric_criteria_id() is not None,
                self.get_grade_method_id() is not None,
                self.get_grade_type() is not None,
                isinstance(self.get_score(), float),
                self.get_assessment() is not None,
            ]
        )

    def _package_into_proto(self) -> CriteriaGrade:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "CriteriaGradeEvent":
        criteria_grade = CriteriaGrade()
        criteria_grade.ParseFromString(event)

        if criteria_grade.id == "":
            return False

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
        return all(
            [
                self.get_id() is not None,
                self.get_crit_grade_id() is not None,
                self.get_embedder_id() is not None,
                self.get_embedding() is not None,
            ]
        )

    def _package_into_proto(self) -> CriteriaEmbedding:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "CriteriaEmbeddingEvent":
        criteria_embedding = CriteriaEmbedding()
        criteria_embedding.ParseFromString(event)

        if criteria_embedding.id == "":
            return False

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

    def get_id(self) -> str or None:
        _id = self.proto.id
        return _id if _id != "" else None

    def get_simmilar_criteria_grade_ids(self) -> List[str] or None:
        simmilar_criteria_grade_ids = list(self.proto.simmilar_criteria_grade_ids)
        return simmilar_criteria_grade_ids if simmilar_criteria_grade_ids else None

    def validate(self) -> bool:
        return all(
            [
                self.get_id() is not None,
                self.get_simmilar_criteria_grade_ids() is not None,
            ]
        )

    def _package_into_proto(self) -> AssesmentSimilarity:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "AssesmentSimilarityEvent":
        assesment_similarity = AssesmentSimilarity()
        assesment_similarity.ParseFromString(event)

        if assesment_similarity.id == "":
            return False

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
        self.proto = StudentRequestedRegrade()
        self.proto.student_id = student_id
        self.proto.submission_id = submission_id
        self.proto.reasoning = reasoning
        self.proto.criteria_grades_to_reevaluate.extend(criteria_grades)

        self.proto.id = generate_event_id(self.__class__.__name__)

        super().__init__(key=self.proto.id, event_type=self.__class__.__name__)

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
        return all(
            [
                self.get_id() is not None,
                self.get_student_id() is not None,
                self.get_submission_id() is not None,
                self.get_reasoning() is not None,
                bool(self.get_criteria_grades_to_reevaluate()),
            ]
        )

    def _package_into_proto(self) -> StudentRequestedRegrade:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "StudentRequestedRegradeEvent":
        regrade_request = StudentRequestedRegrade()
        regrade_request.ParseFromString(event)

        if regrade_request.id == "":
            return False

        new_regrade_request_instance = cls.__new__(cls)
        new_regrade_request_instance.proto = regrade_request
        super(cls, new_regrade_request_instance).__init__(
            key=regrade_request.id,
            event_type=new_regrade_request_instance.__class__.__name__,
        )

        if new_regrade_request_instance.validate():
            return new_regrade_request_instance

        return False
