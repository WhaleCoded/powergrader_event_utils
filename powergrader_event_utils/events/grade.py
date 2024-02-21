from typing import List, Optional

from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
    generate_event_timestamp,
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
from powergrader_event_utils.events.proto import ProtoWrapper


class AICriterionGradingStartedEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = AICriterionGradingStarted

    version_uuid: str
    criterion_uuid: str
    submission_version_uuid: str
    time_started: int

    def __init__(
        self,
        criterion_uuid: str,
        submission_version_uuid: str,
        time_started: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.criterion_uuid = criterion_uuid
        self.submission_version_uuid = submission_version_uuid
        if time_started is None:
            time_started = generate_event_timestamp()
        self.time_started = time_started


class GradingMethodEvent(ProtoPowerGraderEvent):
    key_field_name: str = "uuid"
    proto_type = GradingMethodProto

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
        super().__init__()
        self.uuid = generate_event_uuid(self.__class__.__name__)
        self.model_name = model_name
        self.method_name = method_name
        self.git_hash = git_hash


class Grade(ProtoWrapper):
    proto_type = GradeProto

    score: int
    assessment: str

    def __init__(
        self,
        score: int,
        assessment: str,
    ) -> None:
        super().__init__()
        self.score = score
        self.assessment = assessment


class AICriterionGradeEvent(ProtoPowerGraderEvent):
    key_field_name: str = "grading_started_version_uuid"
    proto_type = AICriterionGrade

    grading_started_version_uuid: str
    grading_method_uuid: str
    grade: Grade
    time_finished: int

    def __init__(
        self,
        grading_started_version_uuid: str,
        grading_method_uuid: str,
        grade: Grade,
        time_finished: Optional[int] = None,
    ) -> None:
        if not isinstance(grade, Grade):
            raise TypeError(
                f"{self.__class__.__name__} grade must be of type Grade. Received {type(grade)}"
            )
        super().__init__()
        self.grading_started_version_uuid = grading_started_version_uuid
        self.grading_method_uuid = grading_method_uuid
        self.grade = grade
        if time_finished is None:
            time_finished = generate_event_timestamp()
        self.time_finished = time_finished


class AIInferredCriterionGradeEvent(ProtoPowerGraderEvent):
    key_field_name: str = "grading_started_version_uuid"
    proto_type = AIInferredCriterionGrade

    grading_started_version_uuid: str
    grading_method_uuid: str
    previous_criterion_grade_version_uuid: str
    faculty_override_criterion_grade_version_uuid: str
    grade: Grade
    time_finished: int

    def __init__(
        self,
        grading_started_version_uuid: str,
        grading_method_uuid: str,
        previous_criterion_grade_version_uuid: str,
        faculty_override_criterion_grade_version_uuid: str,
        grade: Grade,
        time_finished: Optional[int] = None,
    ) -> None:
        if not isinstance(grade, Grade):
            raise TypeError(
                f"{self.__class__.__name__} grade must be of type Grade. Received {type(grade)}"
            )
        super().__init__()
        self.grading_started_version_uuid = grading_started_version_uuid
        self.grading_method_uuid = grading_method_uuid
        self.previous_criterion_grade_version_uuid = (
            previous_criterion_grade_version_uuid
        )
        self.faculty_override_criterion_grade_version_uuid = (
            faculty_override_criterion_grade_version_uuid
        )
        self.grade = grade
        if time_finished is None:
            time_finished = generate_event_timestamp()
        self.time_finished = time_finished


class InstructorCriterionGradeEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = InstructorCriterionGrade

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
        if not isinstance(grade, Grade):
            raise TypeError(
                f"{self.__class__.__name__} grade must be of type Grade. Received {type(grade)}"
            )
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.criterion_uuid = criterion_uuid
        self.submission_version_uuid = submission_version_uuid
        self.instructor_public_uuid = instructor_public_uuid
        self.grade = grade


class InstructorOverrideCriterionGradeEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = InstructorOverrideCriterionGrade

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
        if not isinstance(grade, Grade):
            raise TypeError(
                f"{self.__class__.__name__} grade must be of type Grade. Received {type(grade)}"
            )
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.criterion_uuid = criterion_uuid
        self.submission_version_uuid = submission_version_uuid
        self.previous_criterion_grade_version_uuid = (
            previous_criterion_grade_version_uuid
        )
        self.instructor_public_uuid = instructor_public_uuid
        self.grade = grade


class CriterionGradeEmbeddingEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = CriterionGradeEmbedding

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
        if len(embedding) == 0:
            raise ValueError(
                f"{self.__class__.__name__} embedding must have at least one element"
            )
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.criterion_grade_version_uuid = criterion_grade_version_uuid
        self.embedder_uuid = embedder_uuid
        self.embedding = embedding


class InstructorSubmissionGradeApprovalEvent(ProtoPowerGraderEvent):
    key_field_name: str = "version_uuid"
    proto_type = InstructorSubmissionGradeApproval

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
        version_timestamp: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.version_uuid = generate_event_uuid(self.__class__.__name__)
        self.submission_version_uuid = submission_version_uuid
        self.instructor_public_uuid = instructor_public_uuid
        self.criterion_grade_version_uuids = criterion_grade_version_uuids
        if version_timestamp is None:
            version_timestamp = generate_event_timestamp()
        self.version_timestamp = version_timestamp
