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
        return all([self.get_public_id(), self.get_lms_id()])

    def _package_into_proto(self) -> RegisterCoursePublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> bool or "RegisterCoursePublicIDEvent":
        data = RegisterCoursePublicID()
        data.ParseFromString(event)

        if not data.public_id or not data.lms_id:
            return False

        instance = cls(data.public_id, data.lms_id)
        if instance.validate():
            return instance

        return False


class RegisterSectionPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
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
        return all([self.get_public_id(), self.get_lms_id()])

    def _package_into_proto(self) -> RegisterSectionPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSectionPublicIDEvent" or bool:
        data = RegisterSectionPublicID()
        data.ParseFromString(event)

        if not data.public_id or not data.lms_id:
            return False

        instance = cls(data.public_id, data.lms_id)
        if instance.validate():
            return instance

        return False


class RegisterInstructorPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str, user_type: str) -> None:
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
        return all([self.get_public_id(), self.get_lms_id(), self.get_user_type()])

    def _package_into_proto(self) -> RegisterInstructorPublicID:
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterInstructorPublicIDEvent" or bool:
        data = RegisterInstructorPublicID()
        data.ParseFromString(event)

        if not (data.public_id and data.lms_id and data.user_type):
            return False

        instance = cls(data.public_id, data.lms_id, data.user_type)
        if instance.validate():
            return instance

        return False


class RegisterStudentPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
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
        return all([self.get_public_id(), self.get_lms_id()])

    def _package_into_proto(self) -> RegisterStudentPublicID:
        # This method returns the protobuf message as it is.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterStudentPublicIDEvent" or bool:
        # Attempt to parse the bytes into the protobuf message.
        data = RegisterStudentPublicID()
        data.ParseFromString(event)

        # Check if the required fields are present.
        if not data.public_id or not data.lms_id:
            return False

        # Create an instance of the wrapper class if validation passes.
        instance = cls(data.public_id, data.lms_id)
        if instance.validate():
            return instance

        # Return False if data is invalid.
        return False


class RegisterAssignmentPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
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
        return all([self.get_public_id(), self.get_lms_id()])

    def _package_into_proto(self) -> RegisterAssignmentPublicID:
        # This method packages the instance variables back into the proto message.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterAssignmentPublicIDEvent" or bool:
        # Deserialize event from bytes to proto message.
        data = RegisterAssignmentPublicID()
        data.ParseFromString(event)

        # Check the deserialized data for required fields.
        if not data.public_id or not data.lms_id:
            return False

        # If deserialized data is valid, return an instance of the class.
        instance = cls(data.public_id, data.lms_id)
        if instance.validate():
            return instance

        # Return False if deserialization or validation fails.
        return False


class RegisterRubricPublicIDEvent(PowerGraderEvent):
    def __init__(self, public_id: str, lms_id: str) -> None:
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
        return all([self.get_public_id(), self.get_lms_id()])

    def _package_into_proto(self) -> RegisterRubricPublicID:
        # Return the protobuf message instance.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterRubricPublicIDEvent" or bool:
        # Parse the event data from bytes to a protobuf message.
        data = RegisterRubricPublicID()
        data.ParseFromString(event)

        # Validate the parsed data.
        if not data.public_id or not data.lms_id:
            return False

        # Instantiate the wrapper class with the parsed data if valid.
        instance = cls(data.public_id, data.lms_id)
        if instance.validate():
            return instance

        # Return False if data validation fails.
        return False


class RegisterSubmissionPublicIDEvent(PowerGraderEvent):
    def __init__(
        self, public_id: str, lms_assignment_id: str, lms_student_id: str
    ) -> None:
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
        return all(
            [
                self.get_public_id(),
                self.get_lms_assignment_id(),
                self.get_lms_student_id(),
            ]
        )

    def _package_into_proto(self) -> RegisterSubmissionPublicID:
        # Package the data back into a protobuf message.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "RegisterSubmissionPublicIDEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = RegisterSubmissionPublicID()
        data.ParseFromString(event)

        # Check the integrity of the deserialized data.
        if not (data.public_id and data.lms_assignment_id and data.lms_student_id):
            return False

        # Create and return an event instance if validation is successful.
        instance = cls(data.public_id, data.lms_assignment_id, data.lms_student_id)
        if instance.validate():
            return instance

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
        return all([self.get_public_id(), self.get_private_id()])

    def _package_into_proto(self) -> PublishedToLMS:
        # Package the data back into a protobuf message.
        return self.proto

    @classmethod
    def deserialize(cls, event: bytes) -> "PublishedToLMSEvent" or bool:
        # Deserialize the event bytes back to a protobuf message.
        data = PublishedToLMS()
        data.ParseFromString(event)

        # Check the integrity of the deserialized data.
        if not (
            data.public_id_of_published_entity and data.private_id_of_published_entity
        ):
            return False

        # Create and return an event instance if validation is successful.
        instance = cls(
            data.public_id_of_published_entity, data.private_id_of_published_entity
        )
        if instance.validate():
            return instance

        return False
