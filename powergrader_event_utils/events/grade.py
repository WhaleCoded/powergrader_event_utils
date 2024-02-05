from typing import List
from dataclasses import dataclass

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.grade_pb2 import (
    AICriterionGradingStarted,
    GradingMethod as GradingMethodProto,
    Grade as GradeProto,
    AICriterionGrade,
    AIInferredCriterionGrade,
    InstructorCriterionGrade,
    InstructorOverrideCriterionGrade,
    CriterionGradeEmbedding,
    InstructorSubmissionGradeApproval,
)
from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)


@dataclass
class AICriterionGradingStartedEvent(
    PowerGraderEvent, ProtoWrapper[AICriterionGradingStarted]
):
    version_uuid: str
    criterion_uuid: str
    submission_version_uuid: str
    time_started: int

    def __init__(
        self,
        criterion_uuid: str,
        submission_version_uuid: str,
        time_started: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AICriterionGradingStarted,
            key_field_name="version_uuid",
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            time_started=time_started,
        )

    def _package_into_proto(self) -> AICriterionGradingStarted:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "AICriterionGradingStartedEvent":
        return general_deserialization(
            AICriterionGradingStarted, cls, event, "version_uuid"
        )


@dataclass
class GradingMethodEvent(PowerGraderEvent, ProtoWrapper[GradingMethodProto]):
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
            key_field_name="uuid",
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
    def deserialize(cls, event: bytes) -> "GradingMethodEvent":
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
            key_field_name=None,
            is_powergrader_event=False,
            score=score,
            assessment=assessment,
        )


@dataclass
class AICriterionGradeEvent(PowerGraderEvent, ProtoWrapper[AICriterionGrade]):
    grading_started_version_uuid: str
    criterion_uuid: str
    submission_version_uuid: str
    grading_method_uuid: str
    grade: Grade
    time_finished: int

    def __init__(
        self,
        grading_started_version_uuid: str,
        criterion_uuid: str,
        submission_version_uuid: str,
        grading_method_uuid: str,
        grade: Grade,
        time_finished: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AICriterionGrade,
            key_field_name="grading_started_version_uuid",
            grading_started_version_uuid=grading_started_version_uuid,
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            grading_method_uuid=grading_method_uuid,
            grade=grade,
            time_finished=time_finished,
        )

    def _package_into_proto(self) -> AICriterionGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "AICriterionGradeEvent":
        return general_deserialization(
            AICriterionGrade, cls, event, "grading_started_version_uuid"
        )


@dataclass
class AIInferredCriterionGradeEvent(
    PowerGraderEvent, ProtoWrapper[AIInferredCriterionGrade]
):
    grading_started_version_uuid: str
    criterion_uuid: str
    submission_version_uuid: str
    grading_method_uuid: str
    previous_criterion_grade_version_uuid: str
    faculty_override_criterion_grade_version_uuid: str
    grade: Grade
    time_finished: int

    def __init__(
        self,
        grading_started_version_uuid: str,
        criterion_uuid: str,
        submission_version_uuid: str,
        grading_method_uuid: str,
        previous_criterion_grade_version_uuid: str,
        faculty_override_criterion_grade_version_uuid: str,
        grade: Grade,
        time_finished: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=AIInferredCriterionGrade,
            key_field_name="grading_started_version_uuid",
            grading_started_version_uuid=grading_started_version_uuid,
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            grading_method_uuid=grading_method_uuid,
            previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
            faculty_override_criterion_grade_version_uuid=faculty_override_criterion_grade_version_uuid,
            grade=grade,
            time_finished=time_finished,
        )

    def _package_into_proto(self) -> AIInferredCriterionGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "AIInferredCriterionGradeEvent":
        return general_deserialization(
            AIInferredCriterionGrade, cls, event, "grading_started_version_uuid"
        )


@dataclass
class InstructorCriterionGradeEvent(
    PowerGraderEvent, ProtoWrapper[InstructorCriterionGrade]
):
    version_uuid: str
    criterion_uuid: str
    submission_version_uuid: str
    instructor_public_uuid: str
    grade: Grade

    def __init__(
        self,
        criterion_uuid: str,
        submission_version_uuid: str,
        instructor_public_uuid: str,
        grade: Grade,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorCriterionGrade,
            key_field_name="version_uuid",
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            grade=grade,
        )

    def _package_into_proto(self) -> InstructorCriterionGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorCriterionGradeEvent":
        return general_deserialization(
            InstructorCriterionGrade, cls, event, "version_uuid"
        )


@dataclass
class InstructorOverrideCriterionGradeEvent(
    PowerGraderEvent, ProtoWrapper[InstructorOverrideCriterionGrade]
):
    version_uuid: str
    criterion_uuid: str
    submission_version_uuid: str
    previous_criterion_grade_version_uuid: str
    instructor_public_uuid: str
    grade: Grade

    def __init__(
        self,
        criterion_uuid: str,
        submission_version_uuid: str,
        previous_criterion_grade_version_uuid: str,
        instructor_public_uuid: str,
        grade: Grade,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorOverrideCriterionGrade,
            key_field_name="version_uuid",
            criterion_uuid=criterion_uuid,
            submission_version_uuid=submission_version_uuid,
            previous_criterion_grade_version_uuid=previous_criterion_grade_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            grade=grade,
        )

    def _package_into_proto(self) -> InstructorOverrideCriterionGrade:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "InstructorOverrideCriterionGradeEvent":
        return general_deserialization(
            InstructorOverrideCriterionGrade, cls, event, "version_uuid"
        )


@dataclass
class CriterionGradeEmbeddingEvent(
    PowerGraderEvent, ProtoWrapper[CriterionGradeEmbedding]
):
    version_uuid: str
    criterion_grade_version_uuid: str
    embedder_uuid: str
    embedding: List[float]

    def __init__(
        self,
        criterion_grade_version_uuid: str,
        embedder_uuid: str,
        embedding: List[float],
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=CriterionGradeEmbedding,
            key_field_name="version_uuid",
            criterion_grade_version_uuid=criterion_grade_version_uuid,
            embedder_uuid=embedder_uuid,
            embedding=embedding,
        )

    def _package_into_proto(self) -> CriterionGradeEmbedding:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, event: bytes) -> "CriterionGradeEmbeddingEvent":
        return general_deserialization(
            CriterionGradeEmbedding, cls, event, "version_uuid"
        )


@dataclass
class InstructorSubmissionGradeApprovalEvent(
    PowerGraderEvent, ProtoWrapper[InstructorSubmissionGradeApproval]
):
    version_uuid: str
    submission_version_uuid: str
    instructor_public_uuid: str
    criterion_grade_version_uuids: List[str]
    version_timestamp: int

    def __init__(
        self,
        submission_version_uuid: str,
        instructor_public_uuid: str,
        criterion_grade_version_uuids: List[str],
        version_timestamp: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=InstructorSubmissionGradeApproval,
            key_field_name="version_uuid",
            submission_version_uuid=submission_version_uuid,
            instructor_public_uuid=instructor_public_uuid,
            criterion_grade_version_uuids=criterion_grade_version_uuids,
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
    ai_criterion_grading_started = AICriterionGradingStartedEvent(
        criterion_uuid="123",
        submission_version_uuid="123",
        time_started=123,
    )
    print(ai_criterion_grading_started.serialize())
    print(
        AICriterionGradingStartedEvent.deserialize(
            ai_criterion_grading_started.serialize()
        )
    )

    grading_method = GradingMethodEvent(
        model_name="test",
        method_name="test",
        git_hash="test",
    )
    print(grading_method.serialize())
    print(GradingMethodEvent.deserialize(grading_method.serialize()))

    grade = Grade(
        score=1,
        assessment="test",
    )

    ai_criterion_grade = AICriterionGradeEvent(
        grading_started_version_uuid="123",
        criterion_uuid="123",
        submission_version_uuid="123",
        grading_method_uuid="123",
        grade=grade,
        time_finished=123,
    )
    print(ai_criterion_grade.serialize())
    print(AICriterionGradeEvent.deserialize(ai_criterion_grade.serialize()))

    ai_inferred_criterion_grade = AIInferredCriterionGradeEvent(
        grading_started_version_uuid="123",
        criterion_uuid="123",
        submission_version_uuid="123",
        grading_method_uuid="123",
        previous_criterion_grade_version_uuid="123",
        faculty_override_criterion_grade_version_uuid="123",
        grade=grade,
        time_finished=123,
    )
    print(ai_inferred_criterion_grade.serialize())
    print(
        AIInferredCriterionGradeEvent.deserialize(
            ai_inferred_criterion_grade.serialize()
        )
    )

    instructor_criterion_grade = InstructorCriterionGradeEvent(
        criterion_uuid="123",
        submission_version_uuid="123",
        instructor_public_uuid="123",
        grade=grade,
    )
    print(instructor_criterion_grade.serialize())
    print(
        InstructorCriterionGradeEvent.deserialize(
            instructor_criterion_grade.serialize()
        )
    )

    instructor_override_criterion_grade = InstructorOverrideCriterionGradeEvent(
        criterion_uuid="123",
        submission_version_uuid="123",
        previous_criterion_grade_version_uuid="123",
        instructor_public_uuid="123",
        grade=grade,
    )
    print(instructor_override_criterion_grade.serialize())
    print(
        InstructorOverrideCriterionGradeEvent.deserialize(
            instructor_override_criterion_grade.serialize()
        )
    )

    criterion_grade_embedding = CriterionGradeEmbeddingEvent(
        criterion_grade_version_uuid="123",
        embedder_uuid="123",
        embedding=[1.0],
    )
    print(criterion_grade_embedding.serialize())
    print(
        CriterionGradeEmbeddingEvent.deserialize(criterion_grade_embedding.serialize())
    )

    instructor_submission_grade_approval = InstructorSubmissionGradeApprovalEvent(
        submission_version_uuid="123",
        instructor_public_uuid="123",
        criterion_grade_version_uuids=["123"],
        version_timestamp=123,
    )
    print(instructor_submission_grade_approval.serialize())
    print(
        InstructorSubmissionGradeApprovalEvent.deserialize(
            instructor_submission_grade_approval.serialize()
        )
    )
