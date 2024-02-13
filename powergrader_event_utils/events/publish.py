from enum import Enum
from powergrader_event_utils.events.event import (
    ProtoPowerGraderEvent,
    generate_event_uuid,
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
    LMSInstructorType as LMSInstructorTypeProto,
)
from powergrader_event_utils.events.proto import ProtoEnumWrapper, ProtoWrapper


class RegisterCoursePublicUUIDEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterCoursePublicUUID

    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        super().__init__()
        self.public_uuid = generate_event_uuid(self.__class__.__name__)
        self.lms_id = lms_id
        self.organization_public_uuid = organization_public_uuid


class RegisterSectionPublicUUIDEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterSectionPublicUUID

    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        super().__init__()
        self.public_uuid = generate_event_uuid(self.__class__.__name__)
        self.lms_id = lms_id
        self.organization_public_uuid = organization_public_uuid


class LMSInstructorType(ProtoEnumWrapper):
    proto_type = LMSInstructorTypeProto

    UNSPECIFIED = 0
    TA = 1
    FACULTY = 2


class RegisterInstructorPublicUUIDEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterInstructorPublicUUID

    public_uuid: str
    lms_id: str
    user_type: LMSInstructorType
    organization_public_uuid: str

    def __init__(
        self, lms_id: str, user_type: LMSInstructorType, organization_public_uuid: str
    ) -> None:
        super().__init__()
        if not isinstance(user_type, LMSInstructorType):
            if isinstance(user_type, int) or isinstance(user_type, str):
                try:
                    user_type = LMSInstructorType(user_type)
                except AttributeError:
                    raise ValueError(
                        f"RegisterInstructorPublicUUIDEvent user_type received invalid value {user_type}. {type(user_type)} is allowed, but only when castable to LMSInstructorType"
                    )
            else:
                raise TypeError(
                    f"RegisterInstructorPublicUUIDEvent user_type must be an LMSInstructorType member or convertable to it (int or str). Received {type(user_type)}"
                )
        self.public_uuid = generate_event_uuid(self.__class__.__name__)
        self.lms_id = lms_id
        self.user_type = user_type
        self.organization_public_uuid = organization_public_uuid


class RegisterStudentPublicUUIDEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterStudentPublicUUID

    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        super().__init__()
        self.public_uuid = generate_event_uuid(self.__class__.__name__)
        self.lms_id = lms_id
        self.organization_public_uuid = organization_public_uuid


class RegisterAssignmentPublicUUIDEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterAssignmentPublicUUID

    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        super().__init__()
        self.public_uuid = generate_event_uuid(self.__class__.__name__)
        self.lms_id = lms_id
        self.organization_public_uuid = organization_public_uuid


class RegisterRubricPublicUUIDEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterRubricPublicUUID

    public_uuid: str
    lms_id: str
    organization_public_uuid: str

    def __init__(self, lms_id: str, organization_public_uuid: str) -> None:
        super().__init__()
        self.public_uuid = generate_event_uuid(self.__class__.__name__)
        self.lms_id = lms_id
        self.organization_public_uuid = organization_public_uuid


class RegisterSubmissionPublicUUIDEvent(ProtoPowerGraderEvent):
    key_field_name: str = "public_uuid"
    proto_type = RegisterSubmissionPublicUUID

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
        super().__init__()
        self.public_uuid = generate_event_uuid(self.__class__.__name__)
        self.lms_assignment_id = lms_assignment_id
        self.lms_student_id = lms_student_id
        self.organization_public_uuid = organization_public_uuid


class PublishedToLMSEvent(ProtoPowerGraderEvent):
    key_field_name: str = "published_entity_version_uuid"
    proto_type = PublishedToLMS

    published_entity_version_uuid: str
    publish_timestamp: int

    def __init__(
        self,
        published_entity_version_uuid: str,
        publish_timestamp: int,
    ) -> None:
        super().__init__()
        self.published_entity_version_uuid = published_entity_version_uuid
        self.publish_timestamp = publish_timestamp


class PublishedGradeToLMSEvent(ProtoPowerGraderEvent):
    key_field_name: str = "instructor_grade_approval_version_uuid"
    proto_type = PublishedGradeToLMS

    instructor_grade_approval_version_uuid: str
    publish_timestamp: int

    def __init__(
        self, instructor_grade_approval_version_uuid: str, publish_timestamp: int
    ) -> None:
        super().__init__()
        self.instructor_grade_approval_version_uuid = (
            instructor_grade_approval_version_uuid
        )
        self.publish_timestamp = publish_timestamp
