from typing import Dict, List

from powergrader_event_utils.events.base import (
    PowerGraderEvent,
    generate_event_id,
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
)


class RegisterCoursePublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
        if not public_id or not lms_id:
            raise ValueError("Public ID and LMS ID must be provided")

        self.proto = RegisterCoursePublicID()
        self.proto.public_id = public_id
        self.proto.lms_id = lms_id

        super().__init__(key=self.proto.public_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.COURSE_PUBLIC_ID

    def get_public_id(self) -> str:
        return self.proto.public_id

    def get_lms_id(self) -> str:
        return self.proto.lms_id

    def validate(self) -> bool:
        return bool(self.get_public_id() and self.get_lms_id())

    def _package_into_proto(self) -> RegisterCoursePublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "RegisterCoursePublicIDEvent":
        data = RegisterCoursePublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class RegisterSectionPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
        if not public_id or not lms_id:
            raise ValueError("Public ID and LMS ID must be provided")

        self.proto = RegisterSectionPublicID()
        self.proto.public_id = public_id
        self.proto.lms_id = lms_id

        super().__init__(key=self.proto.public_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SECTION_PUBLIC_ID

    def get_public_id(self) -> str:
        return self.proto.public_id

    def get_lms_id(self) -> str:
        return self.proto.lms_id

    def validate(self) -> bool:
        return bool(self.get_public_id() and self.get_lms_id())

    def _package_into_proto(self) -> RegisterSectionPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSectionPublicIDEvent" or bool:
        data = RegisterSectionPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class RegisterInstructorPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str, user_type: str) -> None:
        if not public_id or not lms_id or not user_type:
            raise ValueError("Public ID, LMS ID, and user_type must be provided")

        self.proto = RegisterInstructorPublicID()
        self.proto.public_id = public_id
        self.proto.lms_id = lms_id
        self.proto.user_type = user_type

        super().__init__(key=self.proto.public_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.INSTRUCTOR_PUBLIC_ID

    def get_public_id(self) -> str:
        return self.proto.public_id

    def get_lms_id(self) -> str:
        return self.proto.lms_id

    def get_user_type(self) -> str:
        return self.proto.user_type

    def validate(self) -> bool:
        # Additional validation for user_type can be added here if needed
        return bool(self.get_public_id() and self.get_lms_id() and self.get_user_type())

    def _package_into_proto(self) -> RegisterInstructorPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterInstructorPublicIDEvent" or bool:
        data = RegisterInstructorPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class RegisterStudentPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
        if not public_id or not lms_id:
            raise ValueError("Public ID and LMS ID must be provided")

        self.proto = RegisterStudentPublicID()
        self.proto.public_id = public_id
        self.proto.lms_id = lms_id

        super().__init__(key=self.proto.public_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.STUDENT_PUBLIC_ID

    def get_public_id(self) -> str:
        return self.proto.public_id

    def get_lms_id(self) -> str:
        return self.proto.lms_id

    def validate(self) -> bool:
        # Here, we assume that having both a public_id and lms_id means the data is valid.
        return bool(self.get_public_id() and self.get_lms_id())

    def _package_into_proto(self) -> RegisterStudentPublicID:
        # This method returns the protobuf message as it is.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterStudentPublicIDEvent" or bool:
        # Attempt to parse the bytes into the protobuf message.
        data = RegisterStudentPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class RegisterAssignmentPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
        if not public_id or not lms_id:
            raise ValueError("Public ID and LMS ID must be provided")

        self.proto = RegisterAssignmentPublicID()
        self.proto.public_id = public_id
        self.proto.lms_id = lms_id

        super().__init__(key=self.proto.public_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.ASSIGNMENT_PUBLIC_ID

    def get_public_id(self) -> str:
        return self.proto.public_id

    def get_lms_id(self) -> str:
        return self.proto.lms_id

    def validate(self) -> bool:
        # Validate that public_id and lms_id are present.
        return bool(self.get_public_id() and self.get_lms_id())

    def _package_into_proto(self) -> RegisterAssignmentPublicID:
        # This method packages the instance variables back into the proto message.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterAssignmentPublicIDEvent" or bool:
        # Deserialize event from bytes to proto message.
        data = RegisterAssignmentPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class RegisterRubricPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
        if not public_id or not lms_id:
            raise ValueError("Public ID and LMS ID must be provided")

        self.proto = RegisterRubricPublicID()
        self.proto.public_id = public_id
        self.proto.lms_id = lms_id

        super().__init__(key=self.proto.public_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.RUBRIC_PUBLIC_ID

    def get_public_id(self) -> str:
        return self.proto.public_id

    def get_lms_id(self) -> str:
        return self.proto.lms_id

    def validate(self) -> bool:
        # Check for the presence of necessary data fields.
        return bool(self.get_public_id() and self.get_lms_id())

    def _package_into_proto(self) -> RegisterRubricPublicID:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterRubricPublicIDEvent" or bool:
        # Parse the event data from bytes to a protobuf message.
        data = RegisterRubricPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class RegisterSubmissionPublicIDEvent(PowerGraderEvent):
    def __init__(
        self, public_id: str, lms_assignment_id: str, lms_student_id: str
    ) -> None:
        if not public_id or not lms_assignment_id or not lms_student_id:
            raise ValueError(
                "Public ID, LMS Assignment ID, and LMS Student ID must be provided"
            )

        self.proto = RegisterSubmissionPublicID()
        self.proto.public_id = public_id
        self.proto.lms_assignment_id = lms_assignment_id
        self.proto.lms_student_id = lms_student_id

        super().__init__(key=self.proto.public_id, event_type=self.__class__.__name__)

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.SUBMISSION_PUBLIC_ID

    def get_public_id(self) -> str:
        return self.proto.public_id

    def get_lms_assignment_id(self) -> str:
        return self.proto.lms_assignment_id

    def get_lms_student_id(self) -> str:
        return self.proto.lms_student_id

    def validate(self) -> bool:
        # Ensure all IDs are present for a valid submission.
        return bool(
            self.get_public_id()
            and self.get_lms_student_id()
            and self.get_lms_assignment_id()
        )

    def _package_into_proto(self) -> RegisterSubmissionPublicID:
        # Package the data back into a protobuf message.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSubmissionPublicIDEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = RegisterSubmissionPublicID()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False


class PublishedToLMSEvent(PowerGraderEvent):
    def __init__(
        self, public_id_of_published_entity: str, private_id_of_published_entity: str
    ) -> None:
        self.proto = PublishedToLMS()
        self.proto.public_id_of_published_entity = public_id_of_published_entity
        self.proto.private_id_of_published_entity = private_id_of_published_entity

        super().__init__(
            key=self.proto.public_id_of_published_entity,
            event_type=self.__class__.__name__,
        )

    @staticmethod
    def get_event_type() -> EventType:
        return EventType.PUBLISHED_TO_LMS

    def get_public_id(self) -> str:
        return self.proto.public_id_of_published_entity

    def get_private_id(self) -> str:
        return self.proto.private_id_of_published_entity

    def validate(self) -> bool:
        # Validate that public and private ids are present.
        return bool(self.get_public_id() and self.get_private_id())

    def _package_into_proto(self) -> PublishedToLMS:
        # Package the data back into a protobuf message.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "PublishedToLMSEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = PublishedToLMS()
        data.ParseFromString(event)

        # Create and return an event instance if validation is successful.
        new_event_instance = cls.__new__(cls)
        new_event_instance.proto = data
        super(cls, new_event_instance).__init__(
            key=data.public_id_of_published_entity,
            event_type=new_event_instance.__class__.__name__,
        )

        if new_event_instance.validate():
            return new_event_instance

        return False
