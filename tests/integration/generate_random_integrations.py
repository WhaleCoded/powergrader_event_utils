import random

from powergrader_event_utils.events import OrganizationEvent
from tests.integration.utils import generate_random_timestamp, generate_random_uuid

 "UVU",
]

INSTRUCTOR_NAMES = [
    "John Doe",
    "Mr. Bean",
    "Jane Doe",
    "Ms. Trunchbull",
    "Professor McGonagall",
    "Professor Snape",
    "Dr. Dolittle",
    "Dr. Jekyll",
    "Dr. Frankenstein",
    "Mr. Tumnus",
    "Bilbo Baggins",
    "Gandalf the Grey",
    "Gandalf the White",
    "Kaladin Stormblessed",
    "Samwise Gamgee",
    "Stanley Yelnats",
]


EMAILS = [
    "email@example.com",
    "firstname.lastname@example.com",
    "email@subdomain.example.com",
    "firstname+lastname@example.com",
    "email@123.123.123.123",
    "email@[123.123.123.123]",
    '"email"@example.com',
    "1234567890@example.com",
    "email@example-one.com",
    "_______@example.com",
    "email@example.name",
    "email@example.museum",
    "email@example.co.jp",
    "firstname-lastname@example.com",
]









def create_random_instructor(
    organization_public_uuid: str, organization_creation_timestamp: int
) -> List[Union[RegisterInstructorPublicUUIDEvent, InstructorEvent]]:
    register_event = RegisterInstructorPublicUUIDEvent(
        lms_id=generate_random_uuid,
        user_type=random.randint(1, 2),
        organization_public_uuid=organization_public_uuid,
    )
    instructor_event = InstructorEvent(
        public_uuid=register_event.public_uuid,
        name=random.choice(INSTRUCTOR_NAMES),
        email=random.choice(EMAILS),
        version_timestamp=generate_random_timestamp(),
    )
    return [register_event, instructor_event]
