from enum import Enum
from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    EventType,
)
from powergrader_event_utils.events.proto_events.publish_pb2 import (
    RegisterCoursePublicUUID,
    RegisterSectionPublicUUID,
    RegisterInstructorPublicUUID,
    RegisterStudentPublicUUID,
    RegisterAssignmentPublicUUID,
    RegisterRubricPublicUUID,
    RegisterSubmissionPublicUUID,
    PublishedToLMS,
    PublishedGradeToLMS,
)
from powergrader_event_utils.events.utils import (
    ProtoWrapper,
    general_deserialization,
    general_proto_type_init,
)


class RegisterCoursePublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterCoursePublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(
        self, public_uuid: str, lms_id: str, organization_public_uuid: str
    ) -> None:
        general_proto_type_init(
            self,
            RegisterCoursePublicUUID,
            "public_uuid",
            public_uuid=public_uuid,
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterCoursePublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.COURSE_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterCoursePublicUUIDEvent":
        return general_deserialization(
            RegisterCoursePublicUUID, cls, event, "public_uuid"
        )


class RegisterSectionPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterSectionPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(
        self, public_uuid: str, lms_id: str, organization_public_uuid: str
    ) -> None:
        general_proto_type_init(
            self,
            RegisterSectionPublicUUID,
            "public_uuid",
            public_uuid=public_uuid,
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterSectionPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SECTION_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSectionPublicUUIDEvent":
        return general_deserialization(
            RegisterSectionPublicUUID, cls, event, "public_uuid"
        )


class LMSInstructorType(Enum):
    UNSPECIFIED = 0
    TA = 1
    FACULTY = 2


class RegisterInstructorPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterInstructorPublicUUID]
):
    public_uuid: str
    lms_id: str
    user_type: LMSInstructorType

    def __init__(
        self, public_uuid: str, lms_id: str, user_type: LMSInstructorType
    ) -> None:
        general_proto_type_init(
            self,
            RegisterInstructorPublicUUID,
            "public_uuid",
            public_uuid=public_uuid,
            lms_id=lms_id,
            user_type=user_type,
        )

    def _package_into_proto(self) -> RegisterInstructorPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterInstructorPublicUUIDEvent":
        return general_deserialization(
            RegisterInstructorPublicUUID, cls, event, "public_uuid"
        )


class RegisterStudentPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterStudentPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(
        self, public_uuid: str, lms_id: str, organization_public_uuid: str
    ) -> None:
        general_proto_type_init(
            self,
            RegisterStudentPublicUUID,
            "public_uuid",
            public_uuid=public_uuid,
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterStudentPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterStudentPublicUUIDEvent":
        return general_deserialization(
            RegisterStudentPublicUUID, cls, event, "public_uuid"
        )


class RegisterAssignmentPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterAssignmentPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(
        self, public_uuid: str, lms_id: str, organization_public_uuid: str
    ) -> None:
        general_proto_type_init(
            self,
            RegisterAssignmentPublicUUID,
            "public_uuid",
            public_uuid=public_uuid,
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterAssignmentPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterAssignmentPublicUUIDEvent":
        return general_deserialization(
            RegisterAssignmentPublicUUID, cls, event, "public_id"
        )


class RegisterRubricPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterRubricPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_uuid: str

    def __init__(self, public_uuid: str, lms_id: str, organization_uuid: str) -> None:
        general_proto_type_init(
            self,
            RegisterRubricPublicUUID,
            "public_uuid",
            public_uuid=public_uuid,
            lms_id=lms_id,
            organization_uuid=organization_uuid,
        )

    def _package_into_proto(self) -> RegisterRubricPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RUBRIC_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterRubricPublicUUIDEvent":
        return general_deserialization(
            RegisterRubricPublicUUID, cls, event, "public_id"
        )


class RegisterSubmissionPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterSubmissionPublicUUID]
):
    public_uuid: str
    lms_assignment_id: str
    lms_student_id: str
    organization_public_uuid: str

    def __init__(
        self,
        public_uuid: str,
        lms_assignment_id: str,
        lms_student_id: str,
        organization_public_uuid: str,
    ) -> None:
        general_proto_type_init(
            self,
            RegisterSubmissionPublicUUID,
            "public_uuid",
            public_uuid=public_uuid,
            lms_assignment_id=lms_assignment_id,
            lms_student_id=lms_student_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterSubmissionPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION_PUBLIC_ID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSubmissionPublicUUIDEvent":
        return general_deserialization(
            RegisterSubmissionPublicUUID, cls, event, "public_uuid"
        )


class PublishedToLMSEvent(PowerGraderEvent, ProtoWrapper[PublishedToLMS]):
    version_uuid_of_published_entity: str
    publish_timestamp: int

    def __init__(
        self,
        version_uuid_of_published_entity: str,
        publish_timestamp: int,
    ) -> None:
        general_proto_type_init(
            self,
            PublishedToLMS,
            "public_id_of_published_entity",
            version_uuid_of_published_entity=version_uuid_of_published_entity,
            publish_timestamp=publish_timestamp,
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
    instructor_review_version_uuid: str
    publish_timestamp: int

    def __init__(
        self, instructor_review_version_uuid: str, publish_timestamp: int
    ) -> None:
        general_proto_type_init(
            self,
            PublishedGradeToLMS,
            "public_submission_id",
            instructor_review_version_uuid=instructor_review_version_uuid,
            publish_timestamp=publish_timestamp,
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


if __name__ == "__main__":
    register_course_public_id = RegisterCoursePublicUUIDEvent(
        public_uuid="123",
        lms_id="123",
        organization_public_uuid="123",
    )
    print(register_course_public_id.serialize())
    print(
        RegisterCoursePublicUUIDEvent.deserialize(register_course_public_id.serialize())
    )

    register_section_public_id = RegisterSectionPublicUUIDEvent(
        public_uuid="123",
        lms_id="123",
        organization_public_uuid="123",
    )
    print(register_section_public_id.serialize())
    print(
        RegisterSectionPublicUUIDEvent.deserialize(
            register_section_public_id.serialize()
        )
    )

    register_instructor_public_id = RegisterInstructorPublicUUIDEvent(
        public_uuid="123",
        lms_id="123",
        user_type=LMSInstructorType.FACULTY,
    )
    print(register_instructor_public_id.serialize())
    print(
        RegisterInstructorPublicUUIDEvent.deserialize(
            register_instructor_public_id.serialize()
        )
    )

    register_student_public_id = RegisterStudentPublicUUIDEvent(
        public_uuid="123",
        lms_id="123",
        organization_public_uuid="123",
    )
    print(register_student_public_id.serialize())
    print(
        RegisterStudentPublicUUIDEvent.deserialize(
            register_student_public_id.serialize()
        )
    )

    register_assignment_public_id = RegisterAssignmentPublicUUIDEvent(
        public_uuid="123",
        lms_id="123",
        organization_public_uuid="123",
    )
    print(register_assignment_public_id.serialize())
    print(
        RegisterAssignmentPublicUUIDEvent.deserialize(
            register_assignment_public_id.serialize()
        )
    )

    register_rubric_public_id = RegisterRubricPublicUUIDEvent(
        public_uuid="123",
        lms_id="123",
        organization_uuid="123",
    )
    print(register_rubric_public_id.serialize())
    print(
        RegisterRubricPublicUUIDEvent.deserialize(register_rubric_public_id.serialize())
    )

    register_submission_public_id = RegisterSubmissionPublicUUIDEvent(
        public_uuid="123",
        lms_assignment_id="123",
        lms_student_id="123",
        organization_public_uuid="123",
    )
    print(register_submission_public_id.serialize())
    print(
        RegisterSubmissionPublicUUIDEvent.deserialize(
            register_submission_public_id.serialize()
        )
    )

    published_to_lms = PublishedToLMSEvent(
        version_uuid_of_published_entity="123",
        publish_timestamp=123,
    )
    print(published_to_lms.serialize())
    print(PublishedToLMSEvent.deserialize(published_to_lms.serialize()))

    published_grade_to_lms = PublishedGradeToLMSEvent(
        instructor_review_version_uuid="123",
        publish_timestamp=123,
    )
    print(published_grade_to_lms.serialize())
    print(PublishedGradeToLMSEvent.deserialize(published_grade_to_lms.serialize()))
