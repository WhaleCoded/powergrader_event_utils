from typing import Dict, List
from enum import Enum
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)
from powergrader_event_utils.events.proto_events.assignment_pb2 import (
    AICriteriaGradingStarted,
    GradingMethod as GradingMethodProto,
    Grade as GradeProto,
    AICriteriaGrade,
    AIInferredCriteriaGrade,
    InstructorCriteriaGrade,
    InstructorOverrideCriteriaGrade,
    CriteriaGradeEmbedding,
    InstructorSubmissionGradeApproval,
)


@dataclass
class AICriteriaGradingStartedEvent(
    PowerGraderEvent, ProtoWrapper[AICriteriaGradingStarted]
):
    version_uuid: str
    criteria_uuid: str
    submission_version_uuid: str
    time_started: int

    def __init__(
        self,
        criteria_uuid: str,
        submission_version_uuid: str,
        time_started: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AICriteriaGradingStarted,
            id_field_to_initialize="version_uuid",
            criteria_uuid=criteria_uuid,
            submission_version_uuid=submission_version_uuid,
            time_started=time_started,
        )

    def _package_into_proto(self) -> AICriteriaGradingStarted:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "AICriteriaGradingStartedEvent":
        return general_deserialization(
            AICriteriaGradingStarted, cls, event, "version_uuid"
        )


@dataclass
class GradingMethod(PowerGraderEvent, ProtoWrapper[GradingMethodProto]):
    uuid: str
    model_name: str
    method_name: str
    git_hash: str

    def __init__(
        self,
        model_name: str,
        method_name: str,
        git_hash: str,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=GradingMethodProto,
            id_field_to_initialize="uuid",
            model_name=model_name,
            method_name=method_name,
            git_hash=git_hash,
        )

    def _package_into_proto(self) -> GradingMethodProto:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "GradingMethod":
        return general_deserialization(GradingMethodProto, cls, event, "uuid")


@dataclass
class Grade(ProtoWrapper[GradeProto]):
    score: int
    assessment: str

    def __init__(
        self,
        score: int,
        assessment: str,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=GradeProto,
            id_field_to_initialize=None,
            is_powergrader_event=False,
            score=score,
            assessment=assessment,
        )


@dataclass
class AICriteriaGradeEvent(PowerGraderEvent, ProtoWrapper[AICriteriaGrade]):
    grading_started_version_uuid: str
    criteria_uuid: str
    submission_version_uuid: str
    grading_method_uuid: str
    grade: Grade
    time_finished: int

    def __init__(
        self,
        grading_started_version_uuid: str,
        criteria_uuid: str,
        submission_version_uuid: str,
        grading_method_uuid: str,
        grade: Grade,
        time_finished: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AICriteriaGrade,
            id_field_to_initialize=None,
            grading_started_version_uuid=grading_started_version_uuid,
            criteria_uuid=criteria_uuid,
            submission_version_uuid=submission_version_uuid,
            grading_method_uuid=grading_method_uuid,
            grade=grade,
            time_finished=time_finished,
        )

    def _package_into_proto(self) -> AICriteriaGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "AICriteriaGradeEvent":
        return general_deserialization(
            AICriteriaGrade, cls, event, "grading_started_version_uuid"
        )


@dataclass
class AIInferredCriteriaGradeEvent(
    PowerGraderEvent, ProtoWrapper[AIInferredCriteriaGrade]
):
    grading_started_version_uuid: str
    criteria_uuid: str
    submission_version_uuid: str
    grading_method_uuid: str
    previous_criteria_grade_version_uuid: str
    faculty_override_criteria_grade_version_uuid: str
    grade: Grade
    time_finished: int

    def __init__(
        self,
        grading_started_version_uuid: str,
        criteria_uuid: str,
        submission_version_uuid: str,
        grading_method_uuid: str,
        previous_criteria_grade_version_uuid: str,
        faculty_override_criteria_grade_version_uuid: str,
        grade: Grade,
        time_finished: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AIInferredCriteriaGrade,
            id_field_to_initialize=None,
            grading_started_version_uuid=grading_started_version_uuid,
            criteria_uuid=criteria_uuid,
            submission_version_uuid=submission_version_uuid,
            grading_method_uuid=grading_method_uuid,
            previous_criteria_grade_version_uuid=previous_criteria_grade_version_uuid,
            faculty_override_criteria_grade_version_uuid=faculty_override_criteria_grade_version_uuid,
            grade=grade,
            time_finished=time_finished,
        )

    def _package_into_proto(self) -> AIInferredCriteriaGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "AIInferredCriteriaGradeEvent":
        return general_deserialization(
            AIInferredCriteriaGrade, cls, event, "grading_started_version_uuid"
        )


@dataclass
class InstructorCriteriaGradeEvent(
    PowerGraderEvent, ProtoWrapper[InstructorCriteriaGrade]
):
    version_uuid: str
    criteria_uuid: str
    submission_version_uuid: str
    instructor_public_uuid: str
    grade: Grade

    def __init__(
        self,
        criteria_uuid: str,
        submission_version_uuid: str,
        instructor_public_uuid: str,
        grade: Grade,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorCriteriaGrade,
            id_field_to_initialize="version_uuid",
            criteria_uuid=criteria_uuid,
            submission_version_uuid=submission_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            grade=grade,
        )

    def _package_into_proto(self) -> InstructorCriteriaGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorCriteriaGradeEvent":
        return general_deserialization(
            InstructorCriteriaGrade, cls, event, "version_uuid"
        )


@dataclass
class InstructorOverrideCriteriaGradeEvent(
    PowerGraderEvent, ProtoWrapper[InstructorOverrideCriteriaGrade]
):
    version_uuid: str
    criteria_uuid: str
    submission_version_uuid: str
    previous_criteria_grade_version_uuid: str
    instructor_public_uuid: str
    grade: Grade

    def __init__(
        self,
        criteria_uuid: str,
        submission_version_uuid: str,
        previous_criteria_grade_version_uuid: str,
        instructor_public_uuid: str,
        grade: Grade,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorOverrideCriteriaGrade,
            id_field_to_initialize="version_uuid",
            criteria_uuid=criteria_uuid,
            submission_version_uuid=submission_version_uuid,
            previous_criteria_grade_version_uuid=previous_criteria_grade_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            grade=grade,
        )

    def _package_into_proto(self) -> InstructorOverrideCriteriaGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorOverrideCriteriaGradeEvent":
        return general_deserialization(
            InstructorOverrideCriteriaGrade, cls, event, "version_uuid"
        )


@dataclass
class CriteriaGradeEmbeddingEvent(
    PowerGraderEvent, ProtoWrapper[CriteriaGradeEmbedding]
):
    version_uuid: str
    criteria_grade_version_uuid: str
    embedder_uuid: str
    embedding: List[float]

    def __init__(
        self,
        criteria_grade_version_uuid: str,
        embedder_uuid: str,
        embedding: List[float],
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=CriteriaGradeEmbedding,
            id_field_to_initialize="version_uuid",
            criteria_grade_version_uuid=criteria_grade_version_uuid,
            embedder_uuid=embedder_uuid,
            embedding=embedding,
        )

    def _package_into_proto(self) -> CriteriaGradeEmbedding:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "CriteriaGradeEmbeddingEvent":
        return general_deserialization(
            CriteriaGradeEmbedding, cls, event, "version_uuid"
        )


@dataclass
class InstructorSubmissionGradeApprovalEvent(
    PowerGraderEvent, ProtoWrapper[InstructorSubmissionGradeApproval]
):
    version_uuid: str
    submission_version_uuid: str
    instructor_public_uuid: str
    criteria_grade_version_uuids: List[str]
    version_timestamp: int

    def __init__(
        self,
        submission_version_uuid: str,
        instructor_public_uuid: str,
        criteria_grade_version_uuids: List[str],
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorSubmissionGradeApproval,
            id_field_to_initialize="version_uuid",
            submission_version_uuid=submission_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            criteria_grade_version_uuids=criteria_grade_version_uuids,
            version_timestamp=version_timestamp,
        )

    def _package_into_proto(self) -> InstructorSubmissionGradeApproval:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorSubmissionGradeApprovalEvent":
        return general_deserialization(
            InstructorSubmissionGradeApproval, cls, event, "version_uuid"
        )


if __name__ == "__main__":
    ai_criterion_grading_started = AICriteriaGradingStartedEvent(
        criteria_uuid="123",
        submission_version_uuid="123",
        time_started=123,
    )
    print(ai_criterion_grading_started.serialize())
    print(
        AICriteriaGradingStartedEvent.deserialize(
            ai_criterion_grading_started.serialize()
        )
    )

    grading_method = GradingMethod(
        model_name="test",
        method_name="test",
        git_hash="test",
    )
    print(grading_method.serialize())
    print(GradingMethod.deserialize(grading_method.serialize()))

    grade = Grade(
        score=1,
        assessment="test",
    )

    ai_criterion_grade = AICriteriaGradeEvent(
        grading_started_version_uuid="123",
        criteria_uuid="123",
        submission_version_uuid="123",
        grading_method_uuid="123",
        grade=grade,
        time_finished=123,
    )
    print(ai_criterion_grade.serialize())
    print(AICriteriaGradeEvent.deserialize(ai_criterion_grade.serialize()))

    ai_inferred_criterion_grade = AIInferredCriteriaGradeEvent(
        grading_started_version_uuid="123",
        criteria_uuid="123",
        submission_version_uuid="123",
        grading_method_uuid="123",
        previous_criteria_grade_version_uuid="123",
        faculty_override_criteria_grade_version_uuid="123",
        grade=grade,
        time_finished=123,
    )
    print(ai_inferred_criterion_grade.serialize())
    print(
        AIInferredCriteriaGradeEvent.deserialize(
            ai_inferred_criterion_grade.serialize()
        )
    )

    instructor_criterion_grade = InstructorCriteriaGradeEvent(
        criteria_uuid="123",
        submission_version_uuid="123",
        instructor_public_uuid="123",
        grade=grade,
    )
    print(instructor_criterion_grade.serialize())
    print(
        InstructorCriteriaGradeEvent.deserialize(instructor_criterion_grade.serialize())
    )

    instructor_override_criterion_grade = InstructorOverrideCriteriaGradeEvent(
        criteria_uuid="123",
        submission_version_uuid="123",
        previous_criteria_grade_version_uuid="123",
        instructor_public_uuid="123",
        grade=grade,
    )
    print(instructor_override_criterion_grade.serialize())
    print(
        InstructorOverrideCriteriaGradeEvent.deserialize(
            instructor_override_criterion_grade.serialize()
        )
    )

    criteria_grade_embedding = CriteriaGradeEmbeddingEvent(
        criteria_grade_version_uuid="123",
        embedder_uuid="123",
        embedding=[1.0],
    )
    print(criteria_grade_embedding.serialize())
    print(CriteriaGradeEmbeddingEvent.deserialize(criteria_grade_embedding.serialize()))

    instructor_submission_grade_approval = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid="123",
        instructor_public_uuid="123",
        criteria_grade_version_uuids=["123"],
        version_timestamp=123,
    )
    print(instructor_submission_grade_approval.serialize())
    print(
        InstructorSubmissionGradeApprovalEvent.deserialize(
            instructor_submission_grade_approval.serialize()
        )
    )
