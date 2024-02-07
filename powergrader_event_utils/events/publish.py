from dataclasses import dataclass
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


@dataclass
class RegisterCoursePublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterCoursePublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RegisterCoursePublicUUID,
            key_field_name="public_uuid",
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterCoursePublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.REGISTER_COURSE_PUBLIC_UUID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterCoursePublicUUIDEvent":
        return general_deserialization(
            RegisterCoursePublicUUID, cls, event, "public_uuid"
        )


@dataclass
class RegisterSectionPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterSectionPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RegisterSectionPublicUUID,
            key_field_name="public_uuid",
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterSectionPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.REGISTER_SECTION_PUBLIC_UUID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSectionPublicUUIDEvent":
        return general_deserialization(
            RegisterSectionPublicUUID, cls, event, "public_uuid"
        )


class LMSInstructorType(Enum):
    UNSPECIFIED = 0
    TA = 1
    FACULTY = 2


@dataclass
class RegisterInstructorPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterInstructorPublicUUID]
):
    public_uuid: str
    lms_id: str
    user_type: LMSInstructorType
    organization_public_uuid: str

    def __init__(
        self, lms_id: str, user_type: LMSInstructorType, organization_public_uuid: str
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RegisterInstructorPublicUUID,
            key_field_name="public_uuid",
            lms_id=lms_id,
            user_type=user_type,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterInstructorPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.REGISTER_INSTRUCTOR_PUBLIC_UUID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterInstructorPublicUUIDEvent":
        return general_deserialization(
            RegisterInstructorPublicUUID, cls, event, "public_uuid"
        )


@dataclass
class RegisterStudentPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterStudentPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RegisterStudentPublicUUID,
            key_field_name="public_uuid",
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterStudentPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.REGISTER_STUDENT_PUBLIC_UUID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterStudentPublicUUIDEvent":
        return general_deserialization(
            RegisterStudentPublicUUID, cls, event, "public_uuid"
        )


@dataclass
class RegisterAssignmentPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterAssignmentPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RegisterAssignmentPublicUUID,
            key_field_name="public_uuid",
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterAssignmentPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.REGISTER_INSTRUCTOR_PUBLIC_UUID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterAssignmentPublicUUIDEvent":
        return general_deserialization(
            RegisterAssignmentPublicUUID, cls, event, "public_uuid"
        )


@dataclass
class RegisterRubricPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterRubricPublicUUID]
):
    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RegisterRubricPublicUUID,
            key_field_name="public_uuid",
            lms_id=lms_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterRubricPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.REGISTER_RUBRIC_PUBLIC_UUID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterRubricPublicUUIDEvent":
        return general_deserialization(
            RegisterRubricPublicUUID, cls, event, "public_uuid"
        )


@dataclass
class RegisterSubmissionPublicUUIDEvent(
    PowerGraderEvent, ProtoWrapper[RegisterSubmissionPublicUUID]
):
    public_uuid: str
    lms_assignment_id: str
    lms_student_id: str
    organization_public_uuid: str

    def __init__(
        self,
        lms_assignment_id: str,
        lms_student_id: str,
        organization_public_uuid: str,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=RegisterSubmissionPublicUUID,
            key_field_name="public_uuid",
            lms_assignment_id=lms_assignment_id,
            lms_student_id=lms_student_id,
            organization_public_uuid=organization_public_uuid,
        )

    def _package_into_proto(self) -> RegisterSubmissionPublicUUID:
        return self.proto

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.REGISTER_SUBMISSION_PUBLIC_UUID

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSubmissionPublicUUIDEvent":
        return general_deserialization(
            RegisterSubmissionPublicUUID, cls, event, "public_uuid"
        )


@dataclass
class PublishedToLMSEvent(PowerGraderEvent, ProtoWrapper[PublishedToLMS]):
    version_uuid_of_published_entity: str
    publish_timestamp: int

    def __init__(
        self,
        version_uuid_of_published_entity: str,
        publish_timestamp: int,
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=PublishedToLMS,
            key_field_name="version_uuid_of_published_entity",
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
            PublishedToLMS, cls, event, "version_uuid_of_published_entity"
        )


@dataclass
class PublishedGradeToLMSEvent(PowerGraderEvent, ProtoWrapper[PublishedGradeToLMS]):
    instructor_grade_approval_version_uuid: str
    publish_timestamp: int

    def __init__(
        self, instructor_grade_approval_version_uuid: str, publish_timestamp: int
    ) -> None:
        general_proto_type_init(
            object_to_initialize=self,
            proto_type=PublishedGradeToLMS,
            key_field_name="instructor_grade_approval_version_uuid",
            instructor_grade_approval_version_uuid=instructor_grade_approval_version_uuid,
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
            PublishedGradeToLMS, cls, event, "instructor_grade_approval_version_uuid"
        )


if __name__ == "__main__":
    register_course_public_uuid = RegisterCoursePublicUUIDEvent(
        lms_id="lms_id", organization_public_uuid="organization_public_uuid"
    )
    print(register_course_public_uuid.serialize())
    print(
        RegisterCoursePublicUUIDEvent.deserialize(
            register_course_public_uuid.serialize()
        )
    )

    register_section_public_uuid = RegisterSectionPublicUUIDEvent(
        lms_id="lms_id", organization_public_uuid="organization_public_uuid"
    )
    print(register_section_public_uuid.serialize())
    print(
        RegisterSectionPublicUUIDEvent.deserialize(
            register_section_public_uuid.serialize()
        )
    )

    register_instructor_public_uuid = RegisterInstructorPublicUUIDEvent(
        lms_id="lms_id", user_type=LMSInstructorType.TA
    )
    print(register_instructor_public_uuid.serialize())
    print(
        RegisterInstructorPublicUUIDEvent.deserialize(
            register_instructor_public_uuid.serialize()
        )
    )

    register_student_public_uuid = RegisterStudentPublicUUIDEvent(
        lms_id="lms_id", organization_public_uuid="organization_public_uuid"
    )
    print(register_student_public_uuid.serialize())
    print(
        RegisterStudentPublicUUIDEvent.deserialize(
            register_student_public_uuid.serialize()
        )
    )

    register_assignment_public_uuid = RegisterAssignmentPublicUUIDEvent(
        lms_id="lms_id", organization_public_uuid="organization_public_uuid"
    )
    print(register_assignment_public_uuid.serialize())
    print(
        RegisterAssignmentPublicUUIDEvent.deserialize(
            register_assignment_public_uuid.serialize()
        )
    )

    register_rubric_public_uuid = RegisterRubricPublicUUIDEvent(
        lms_id="lms_id", organization_public_uuid="organization_public_uuid"
    )
    print(register_rubric_public_uuid.serialize())
    print(
        RegisterRubricPublicUUIDEvent.deserialize(
            register_rubric_public_uuid.serialize()
        )
    )

    register_submission_public_uuid = RegisterSubmissionPublicUUIDEvent(
        lms_assignment_id="lms_assignment_id",
        lms_student_id="lms_student_id",
        organization_public_uuid="organization_public_uuid",
    )
    print(register_submission_public_uuid.serialize())
    print(
        RegisterSubmissionPublicUUIDEvent.deserialize(
            register_submission_public_uuid.serialize()
        )
    )

    published_to_lms = PublishedToLMSEvent(
        version_uuid_of_published_entity="version_uuid_of_published_entity",
        publish_timestamp=123,
    )
    print(published_to_lms.serialize())
    print(PublishedToLMSEvent.deserialize(published_to_lms.serialize()))

    published_grade_to_lms = PublishedGradeToLMSEvent(
        instructor_grade_approval_version_uuid="instructor_grade_approval_version_uuid",
        publish_timestamp=123,
    )
    print(published_grade_to_lms.serialize())
    print(PublishedGradeToLMSEvent.deserialize(published_grade_to_lms.serialize()))
