from enum import Enum
from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.publish_pb2 import (
    RegisterCoursePublicID,
    RegisterSectionPublicID,
    RegisterInstructorPublicID,
    RegisterStudentPublicID,
    RegisterAssignmentPublicID,
    RegisterRubricPublicID,
    RegisterSubmissionPublicID,
    PublishedToLMS,
    PublishedGradeToLMS,
)
from powergrader_event_utils.events.utils import ProtoWrapper, general_deserialization


class RegisterCoursePublicIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterCoursePublicID]
):
    public_id: str
    lms_id: str

    def __init__(self, public_id: str, lms_id: str) -> None:
        proto = RegisterCoursePublicID()

        if public_id is not None:
            proto.public_id = public_id

        if lms_id is not None:
            proto.lms_id = lms_id

        ProtoWrapper.__init__(self, RegisterCoursePublicID, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> RegisterCoursePublicID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.COURSE_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterCoursePublicIDEvent":
        return general_deserialization(RegisterCoursePublicID, cls, event, "public_id")


class RegisterSectionPublicIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterSectionPublicID]
):
    public_id: str
    lms_id: str

    def __init__(self, public_id: str, lms_id: str) -> None:
        proto = RegisterSectionPublicID()

        if public_id is not None:
            proto.public_id = public_id

        if lms_id is not None:
            proto.lms_id = lms_id

        ProtoWrapper.__init__(self, RegisterSectionPublicID, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> RegisterSectionPublicID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SECTION_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSectionPublicIDEvent":
        return general_deserialization(RegisterSectionPublicID, cls, event, "public_id")


class LMSInstructorType(Enum):
    UNSPECIFIED = 0
    TA = 1
    FACULTY = 2


class RegisterInstructorPublicIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterInstructorPublicID]
):
    public_id: str
    lms_id: str
    user_type: LMSInstructorType

    def __init__(
        self, public_id: str, lms_id: str, user_type: LMSInstructorType
    ) -> None:
        proto = RegisterInstructorPublicID()

        if public_id is not None:
            proto.public_id = public_id

        if lms_id is not None:
            proto.lms_id = lms_id

        if user_type is not None:
            proto.user_type = user_type.value

        ProtoWrapper.__init__(self, RegisterInstructorPublicID, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> RegisterInstructorPublicID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterInstructorPublicIDEvent":
        return general_deserialization(
            RegisterInstructorPublicID, cls, event, "public_id"
        )


class RegisterStudentPublicIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterStudentPublicID]
):
    public_id: str
    lms_id: str

    def __init__(self, public_id: str, lms_id: str) -> None:
        proto = RegisterStudentPublicID()

        if public_id is not None:
            proto.public_id = public_id

        if lms_id is not None:
            proto.lms_id = lms_id

        ProtoWrapper.__init__(self, RegisterStudentPublicID, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> RegisterStudentPublicID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterStudentPublicIDEvent":
        return general_deserialization(RegisterStudentPublicID, cls, event, "public_id")


class RegisterAssignmentPublicIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterAssignmentPublicID]
):
    public_id: str
    lms_id: str
    organization_id: str

    def __init__(self, public_id: str, lms_id: str, organization_id: str) -> None:
        proto = RegisterAssignmentPublicID()

        if public_id is not None:
            proto.public_id = public_id

        if lms_id is not None:
            proto.lms_id = lms_id

        if organization_id is not None:
            proto.organization_id = organization_id

        ProtoWrapper.__init__(self, RegisterAssignmentPublicID, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> RegisterAssignmentPublicID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterAssignmentPublicIDEvent":
        return general_deserialization(
            RegisterAssignmentPublicID, cls, event, "public_id"
        )


class RegisterRubricPublicIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterRubricPublicID]
):
    public_id: str
    lms_id: str
    organization_id: str

    def __init__(self, public_id: str, lms_id: str, organization_id: str) -> None:
        proto = RegisterRubricPublicID()

        if organization_id is not None:
            proto.organization_id = organization_id

        if public_id is not None:
            proto.public_id = public_id

        if lms_id is not None:
            proto.lms_id = lms_id

        ProtoWrapper.__init__(self, RegisterRubricPublicID, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> RegisterRubricPublicID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RUBRIC_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterRubricPublicIDEvent":
        return general_deserialization(RegisterRubricPublicID, cls, event, "public_id")


class RegisterSubmissionPublicIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterSubmissionPublicID]
):
    public_id: str
    lms_assignment_id: str
    lms_student_id: str
    organization_id: str

    def __init__(
        self,
        public_id: str,
        lms_assignment_id: str,
        lms_student_id: str,
        organization_id: str,
    ) -> None:
        proto = RegisterSubmissionPublicID()

        if organization_id is not None:
            proto.organization_id = organization_id

        if public_id is not None:
            proto.public_id = public_id

        if lms_assignment_id is not None:
            proto.lms_assignment_id = lms_assignment_id

        if lms_student_id is not None:
            proto.lms_student_id = lms_student_id

        ProtoWrapper.__init__(self, RegisterSubmissionPublicID, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> RegisterSubmissionPublicID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSubmissionPublicIDEvent":
        return general_deserialization(
            RegisterSubmissionPublicID, cls, event, "public_id"
        )


class PublishedToLMSEvent(PowerGraderEvent, ProtoWrapper[PublishedToLMS]):
    public_id_of_published_entity: str
    private_id_of_published_entity: str
    when: int

    def __init__(
        self,
        public_id_of_published_entity: str,
        private_id_of_published_entity: str,
        when: int,
    ) -> None:
        proto = PublishedToLMS()

        if when is not None:
            proto.when = when

        if public_id_of_published_entity is not None:
            proto.public_id_of_published_entity = public_id_of_published_entity

        if private_id_of_published_entity is not None:
            proto.private_id_of_published_entity = private_id_of_published_entity

        ProtoWrapper.__init__(self, PublishedToLMS, proto)
        PowerGraderEvent.__init__(
            self,
            key=proto.public_id_of_published_entity,
            event_type=self.__class__.__name__,
        )

    def _package_into_proto(self) -> PublishedToLMS:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.PUBLISHED_TO_LMS

    @classmethod
    def deserialize(cls, event: bytes) -> "PublishedToLMSEvent":
        return general_deserialization(
            PublishedToLMS, cls, event, "public_id_of_published_entity"
        )


class PublishedGradeToLMSEvent(PowerGraderEvent, ProtoWrapper[PublishedGradeToLMS]):
    public_submission_id: str
    instructor_review_id: str
    when: int

    def __init__(
        self, public_submission_id: str, instructor_review_id: str, when: int
    ) -> None:
        proto = PublishedGradeToLMS()

        if when is not None:
            proto.when = when

        if public_submission_id is not None:
            proto.public_submission_id = public_submission_id

        if instructor_review_id is not None:
            proto.instructor_review_id = instructor_review_id

        ProtoWrapper.__init__(self, PublishedGradeToLMS, proto)
        PowerGraderEvent.__init__(
            self, key=proto.public_submission_id, event_type=self.__class__.__name__
        )

    def _package_into_proto(self) -> PublishedGradeToLMS:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.PUBLISHED_GRADE_TO_LMS

    @classmethod
    def deserialize(cls, event: bytes) -> "PublishedGradeToLMSEvent":
        return general_deserialization(
            PublishedGradeToLMS, cls, event, "public_submission_id"
        )
